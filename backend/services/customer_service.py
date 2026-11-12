from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from backend.services.store_data import store
from backend.models.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    @staticmethod
    def _extract_initials(name: str) -> str:
        parts = name.strip().split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        elif parts:
            return parts[0][:2].upper()
        return "CU"

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        city: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        results = list(store.customers)

        if search and isinstance(search, str):
            q = search.lower().strip()
            results = [
                c for c in results
                if q in c["name"].lower() or q in c["phone"].lower() or q in c["city"].lower()
            ]

        if city and isinstance(city, str):
            results = [c for c in results if c["city"].lower() == city.lower().strip()]

        return results

    @staticmethod
    def get_by_phone(phone: str) -> Dict[str, Any]:
        clean_target = phone.replace(" ", "").replace("-", "")
        for c in store.customers:
            clean_phone = c["phone"].replace(" ", "").replace("-", "")
            if clean_phone == clean_target:
                return c

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with phone '{phone}' not found",
        )

    @staticmethod
    def create(data: CustomerCreate) -> Dict[str, Any]:
        clean_new = data.phone.replace(" ", "").replace("-", "")
        for c in store.customers:
            if c["phone"].replace(" ", "").replace("-", "") == clean_new:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Customer with phone '{data.phone}' already exists",
                )

        cust_dict = data.model_dump()
        if not cust_dict.get("initials"):
            cust_dict["initials"] = CustomerService._extract_initials(cust_dict["name"])

        store.add_customer(cust_dict)
        return cust_dict

    @staticmethod
    def update(phone: str, data: CustomerUpdate) -> Dict[str, Any]:
        customer = CustomerService.get_by_phone(phone)
        update_fields = data.model_dump(exclude_unset=True)

        for key, value in update_fields.items():
            if value is not None:
                customer[key] = value

        if "name" in update_fields and not customer.get("initials"):
            customer["initials"] = CustomerService._extract_initials(customer["name"])

        store.update_customer(customer)
        return customer

    @staticmethod
    def delete(phone: str) -> Dict[str, Any]:
        customer = CustomerService.get_by_phone(phone)
        store.delete_customer(customer["phone"])
        return customer
