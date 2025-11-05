from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, date

# 🔹 Общая база для всех моделей
class ExpenseBase(BaseModel):
    title: str = Field(..., min_length=1, description="Название расхода не может быть пустым")
    amount: float = Field(..., gt=0, description="Сумма должна быть положительной")
    category: Optional[str] = Field(default=None, max_length=50, description="Категория расхода")

# 🔹 Модель для создания (POST)
class ExpenseCreate(ExpenseBase):
    date: Optional[datetime] = None

    @field_validator("date", mode="before")
    def validate_date(cls, v):
        """Если дата не указана — ставим текущую."""
        if v is None:
            return datetime.now()
        return v

# 🔹 Модель для чтения (GET / ответов)
class Expense(ExpenseBase):
    id: int
    date: date
