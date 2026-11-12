from typing import List, Optional, Annotated
from fastapi import APIRouter, Query, status
from backend.models.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from backend.services.customer_service import CustomerService

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("", response_model=List[CustomerResponse])
def get_customers(
    search: Annotated[Optional[str], Query(description="Search by name, phone, or city")] = None,
    city: Annotated[Optional[str], Query(description="Filter by city")] = None,
):
    """Retrieve all customers with optional search and city filters."""
    return CustomerService.get_all(search=search, city=city)


@router.get("/{phone}", response_model=CustomerResponse)
def get_customer(phone: str):
    """Retrieve customer by phone number."""
    return CustomerService.get_by_phone(phone)


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate):
    """Register a new customer."""
    return CustomerService.create(customer)


@router.put("/{phone}", response_model=CustomerResponse)
def update_customer(phone: str, update_data: CustomerUpdate):
    """Update customer details."""
    return CustomerService.update(phone, update_data)


@router.delete("/{phone}", response_model=CustomerResponse)
def delete_customer(phone: str):
    """Delete a customer record."""
    return CustomerService.delete(phone)
