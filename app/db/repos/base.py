from abc import ABC
from datetime import datetime
from typing import Generic, List, TypeVar

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

ModelType = TypeVar("ModelType")


class BaseRepo(ABC, Generic[ModelType]):

    model_type: ModelType
    order_by: str  # Column name to order by

    def __init__(self, session: AsyncSession):
        self.session = session

    def dict_encoder(self, dict_to_encode: dict) -> dict:
        """
        Convert any datetime values in a dictionary to ISO format.
        """
        for k, v in dict_to_encode.items():
            if isinstance(v, datetime):
                dict_to_encode[
                    k
                ] = v.isoformat()  # convert datetime object to ISO format
            elif isinstance(v, dict):
                dict_to_encode[k] = self.dict_encoder(
                    v
                )  # traverse nested dictionary
        return dict_to_encode

    async def _add_obj(self, model: ModelType) -> ModelType:
        for c in model.__table__.columns:
            if (
                isinstance(c.type, JSONB)
                and getattr(model, c.name) is not None
            ):
                try:
                    flag_modified(model, c.name)
                except KeyError:
                    ...
        self.session.add(model)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise SQLAlchemyError(f"Integrity error: {e}") from e
        else:
            await self.session.refresh(model)
            return model

    async def list(self, offset: int = 0, limit: int = 20) -> list[ModelType]:
        query = select(self.model_type).order_by(self.order_by)
        query = query.offset(offset).limit(limit)
        records = await self.session.execute(query)
        models = records.scalars().all()
        return models  # noqa

    async def retrieve(self, id: int) -> ModelType:
        query = select(self.model_type).filter(self.model_type.id == id)
        records = await self.session.execute(query)
        try:
            model = records.scalars().one()
        except NoResultFound:
            raise SQLAlchemyError(
                f"{self.model_type.__name__} with id={id} does not exist"
            )
        return model

    async def create(self, model: ModelType, *args, **kwargs) -> ModelType:
        return await self._add_obj(model)

    async def update(self, model: ModelType, *args, **kwargs) -> ModelType:
        return await self._add_obj(model)

    async def delete(self, id: int) -> None:
        query = delete(self.model_type).where(self.model_type.id == id)
        try:
            await self.session.execute(query)
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise SQLAlchemyError(f"Integrity error: {e}") from e

    async def count(self, *args, **kwargs) -> int:
        query = select(func.count()).select_from(
            select(self.model_type).subquery()
        )
        records = await self.session.execute(query)
        count = records.scalar_one()
        return count

    async def bulk_delete(
        self, ids: List[int], sync_session: bool = False
    ) -> None:
        if not ids:
            return
        execution_options = {"synchronize_session": sync_session}
        query = delete(self.model_type).filter(self.model_type.id.in_(ids))
        try:
            await self.session.execute(
                query, execution_options=execution_options
            )
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise SQLAlchemyError(f"Integrity error: {e}") from e

    async def bulk_insert(self, values_data: List[dict]) -> None:
        if not values_data:
            return
        query = insert(self.model_type)
        await self.session.execute(query, values_data)

    async def bulk_update(
        self, values_data: List[dict], sync_session: bool = False
    ) -> None:
        if not values_data:
            return
        execution_options = {"synchronize_session": sync_session}
        query = update(self.model_type)
        try:
            await self.session.execute(
                query, values_data, execution_options=execution_options
            )
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise SQLAlchemyError(f"Integrity error: {e}") from e
