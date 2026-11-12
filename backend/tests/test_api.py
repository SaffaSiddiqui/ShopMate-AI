"""Test runner proxy for ShopMate AI backend tests."""
from backend.tests.run_tests import run_tests

def test_all_endpoints():
    run_tests()

if __name__ == "__main__":
    run_tests()
