# Placeholder for app/db/base_class.py
# app/db/base_class.py

from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Automatically generate __tablename__ if not provided
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
