# Placeholder for app/repositories/base.py
from typing import Generic, Type, TypeVar, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from fastapi import HTTPException, status
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from app.db.base_class import Base

# Declare a generic type variable for models and schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def get(self, id: int) -> Optional[ModelType]:
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} with id {id} not found",
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching the data."
            )

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.get(id)  # Reuse the get method, already handles exceptions

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        try:
            return self.db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching the data."
            )

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        try:
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A conflict occurred while inserting the data. This might be due to a duplicate entry or other integrity constraints."
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while inserting the data."
            )

    def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        try:
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A conflict occurred while updating the data. This might be due to a duplicate entry or other integrity constraints."
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the data."
            )

    def remove(self, id: int) -> ModelType:
        obj = self.get(id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} with id {id} not found",
            )
        try:
            self.db.delete(obj)
            self.db.commit()
            return obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the data."
            )
