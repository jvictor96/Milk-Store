import datetime
from sqlmodel import Session, func, select
from repositories.mappers.batch_mapper import BatchMapper
from repositories.schemas.batch_entity import BatchEntity
from domain.schemas.batch import Batch
from domain.ports.batch_repository_port import BatchRepositoryPort
from typing import Optional
from .postgres_connection import engine

class BatchesAdapter(BatchRepositoryPort):
    
    def get_batch_by_id(self, id: str) -> Optional[Batch]:
        with Session(engine) as session:
            stmt = select(BatchEntity).where(BatchEntity.batch_code == id)
            result = session.exec(stmt)
            return result.first()
    
    def get_active_batches(self) -> list[Batch]:
        with Session(engine) as session:
            stmt = select(BatchEntity).where(
                func.date(BatchEntity.expiry_date) > func.date(datetime.datetime.now())).where(
                BatchEntity.deleted_at == None).where(
                BatchEntity.consumed < BatchEntity.volume_liters)
            result = session.exec(stmt)
            batches = [BatchMapper.to_domain(batch) for batch in result.all()]
            session.commit()
        return batches
        
    
    def get_active_batches_until_date(self, date: datetime.datetime) -> list[Batch]:
        with Session(engine) as session:
            stmt = select(BatchEntity).where(
                func.date(BatchEntity.expiry_date) > func.date(datetime.datetime.now())).where(
                BatchEntity.expiry_date < date).where(
                BatchEntity.deleted_at == None).where(
                BatchEntity.consumed < BatchEntity.volume_liters)
            result = session.exec(stmt)
            batches = [BatchMapper.to_domain(batch) for batch in result.all()]
            session.commit()
        return batches
    
    def post_batch(self, batch: Batch) -> Batch:
        batch_entity = BatchMapper.to_entity(batch)
        with Session(engine) as session:
            session.add(batch_entity)
            batch = BatchMapper.to_domain(batch_entity)
            session.commit()
        return batch

    def update_batch(self, batch_id: str, batch: Batch) -> Batch:
        with Session(engine) as session:
            batch_entity = session.get(BatchEntity, batch_id)
            BatchMapper.merge(batch_entity, batch)
            batch = BatchMapper.to_domain(batch_entity)
            session.commit()
        return batch