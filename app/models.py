"""
Pydantic models for representing and validating expense data.

Includes base fields shared between request and response schemas,
input validation, and structures used for API create/read operations.
"""

from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ExpenseBase(BaseModel):
    """
    Base schema for expense entities.

    Attributes:
        title (str): Name of the expense.
        amount (float): Monetary value; must be positive.
        category (Optional[str]): Optional category label.
    """

    title: str = Field(..., min_length=1, description="Expense title must not be empty.")
    amount: float = Field(..., gt=0, description="Amount must be a positive number.")
    category: Optional[str] = Field(default=None, max_length=50, description="Optional expense category.")


class ExpenseCreate(ExpenseBase):
    """
    Schema used when creating a new expense entry.

    Attributes:
        date (datetime): Date and time when the expense occurred.
    """

    date: Optional[datetime] = None

    @field_validator("date", mode="before")
    def set_current_datetime_if_missing(cls, value):
        """
        Assign the current datetime if no date value is provided.

        Args:
            value (datetime | None): Incoming date value.

        Returns:
            datetime: Valid datetime.
        """
        return value or datetime.now()


class Expense(ExpenseBase):
    """
    Response schema representing a stored expense entry.

    Attributes:
        id (int): Unique identifier.
        date (date): Date of the expense.
    """

    id: int
    date: date