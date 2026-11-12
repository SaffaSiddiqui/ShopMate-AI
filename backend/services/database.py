import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List


class Database:
    """Small SQLite persistence layer for ShopMate's local store data."""

    TABLES = {
        "products": "sku",
        "orders": "id",
        "customers": "phone",
        "sales_7d": "day",
        "sales_30d": "day",
    }

    def __init__(self) -> None:
        default_path = Path(__file__).resolve().parents[1] / "shopmate.db"
        self.path = Path(os.environ.get("SHOPMATE_DATABASE_PATH", default_path))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self._connect() as connection:
            for table in self.TABLES:
                connection.execute(
                    f"""CREATE TABLE IF NOT EXISTS {table} (
                        record_key TEXT PRIMARY KEY,
                        position INTEGER NOT NULL,
                        payload TEXT NOT NULL
                    )"""
                )

    def seed_if_empty(self, seed_data: Dict[str, List[Dict[str, Any]]]) -> None:
        with self._connect() as connection:
            for table, records in seed_data.items():
                count = connection.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()[0]
                if count == 0:
                    self._replace_records(connection, table, records)

    @staticmethod
    def _replace_records(
        connection: sqlite3.Connection,
        table: str,
        records: Iterable[Dict[str, Any]],
    ) -> None:
        key_field = Database.TABLES[table]
        connection.execute(f"DELETE FROM {table}")
        connection.executemany(
            f"INSERT INTO {table} (record_key, position, payload) VALUES (?, ?, ?)",
            [
                (str(record[key_field]), position, json.dumps(record, ensure_ascii=False))
                for position, record in enumerate(records)
            ],
        )

    def reset(self, seed_data: Dict[str, List[Dict[str, Any]]]) -> None:
        with self._connect() as connection:
            for table, records in seed_data.items():
                self._replace_records(connection, table, records)

    def get_all(self, table: str) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                f"SELECT payload FROM {table} ORDER BY position, rowid"
            ).fetchall()
        return [json.loads(row["payload"]) for row in rows]

    def add(
        self,
        table: str,
        record: Dict[str, Any],
        prepend: bool = False,
    ) -> None:
        key_field = self.TABLES[table]
        with self._connect() as connection:
            position = 0
            if prepend:
                connection.execute(f"UPDATE {table} SET position = position + 1")
            else:
                position = connection.execute(
                    f"SELECT COALESCE(MAX(position), -1) + 1 FROM {table}"
                ).fetchone()[0]
            connection.execute(
                f"INSERT INTO {table} (record_key, position, payload) VALUES (?, ?, ?)",
                (
                    str(record[key_field]),
                    position,
                    json.dumps(record, ensure_ascii=False),
                ),
            )

    def create_order_with_stock(
        self,
        order: Dict[str, Any],
        sku: str,
        quantity: int,
    ) -> None:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT payload FROM products WHERE record_key = ?", (sku,)
            ).fetchone()
            if row is None:
                raise KeyError(f"No product found for SKU {sku}")

            product = json.loads(row["payload"])
            if product["stock"] < quantity:
                raise ValueError(f"Only {product['stock']} units are available")

            product["stock"] -= quantity
            connection.execute(
                "UPDATE products SET payload = ? WHERE record_key = ?",
                (json.dumps(product, ensure_ascii=False), sku),
            )
            connection.execute("UPDATE orders SET position = position + 1")
            connection.execute(
                "INSERT INTO orders (record_key, position, payload) VALUES (?, ?, ?)",
                (
                    order["id"],
                    0,
                    json.dumps(order, ensure_ascii=False),
                ),
            )

    def delete_order_and_restore_stock(self, order_id: str) -> Dict[str, Any]:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT payload FROM orders WHERE record_key = ?", (order_id,)
            ).fetchone()
            if row is None:
                raise KeyError(f"No order found for ID {order_id}")

            order = json.loads(row["payload"])
            sku = order.get("product_sku")
            quantity = order.get("quantity")
            if sku and quantity and order.get("status") != "Cancelled":
                product_row = connection.execute(
                    "SELECT payload FROM products WHERE record_key = ?", (sku,)
                ).fetchone()
                if product_row is not None:
                    product = json.loads(product_row["payload"])
                    product["stock"] += quantity
                    connection.execute(
                        "UPDATE products SET payload = ? WHERE record_key = ?",
                        (json.dumps(product, ensure_ascii=False), sku),
                    )

            connection.execute("DELETE FROM orders WHERE record_key = ?", (order_id,))
        return order

    def update_order_status(
        self,
        order_id: str,
        order: Dict[str, Any],
        new_status: str,
    ) -> None:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            if order.get("product_sku") and order.get("quantity"):
                product_row = connection.execute(
                    "SELECT payload FROM products WHERE record_key = ?",
                    (order["product_sku"],),
                ).fetchone()
                if product_row is None:
                    raise KeyError(f"No product found for SKU {order['product_sku']}")

                product = json.loads(product_row["payload"])
                was_cancelled = order.get("status") == "Cancelled"
                is_cancelled = new_status == "Cancelled"
                if not was_cancelled and is_cancelled:
                    product["stock"] += order["quantity"]
                elif was_cancelled and not is_cancelled:
                    if product["stock"] < order["quantity"]:
                        raise ValueError(f"Only {product['stock']} units are available")
                    product["stock"] -= order["quantity"]
                connection.execute(
                    "UPDATE products SET payload = ? WHERE record_key = ?",
                    (json.dumps(product, ensure_ascii=False), order["product_sku"]),
                )

            order["status"] = new_status
            connection.execute(
                "UPDATE orders SET payload = ? WHERE record_key = ?",
                (json.dumps(order, ensure_ascii=False), order_id),
            )

    def update(self, table: str, key: str, record: Dict[str, Any]) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                f"UPDATE {table} SET payload = ? WHERE record_key = ?",
                (json.dumps(record, ensure_ascii=False), key),
            )
            if cursor.rowcount == 0:
                raise KeyError(f"No {table} record found for {key}")

    def delete(self, table: str, key: str) -> None:
        with self._connect() as connection:
            connection.execute(f"DELETE FROM {table} WHERE record_key = ?", (key,))


database = Database()
