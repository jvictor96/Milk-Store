import datetime
from sqlmodel import Session, select
from repositories.mappers.batch_mapper import BatchMapper
from repositories.schemas.batch_entity import BatchEntity
from domain.schemas.batch import Batch
from domain.ports.batch_repository_port import BatchRepositoryPort
from typing import Optional
from .postgres_connection import engine

class BatchesPostgresAdapter(BatchRepositoryPort):
    
    def get_batch_by_id(self, id: str) -> Optional[Batch]:
        with Session(engine) as session:
            stmt = select(BatchEntity).where(BatchEntity.batch_code == id)
            result = session.exec(stmt)
        return result.first
    
    def get_active_batches(self) -> list[Batch]:
        with Session(engine) as session:
            stmt = select(BatchEntity).where(
                BatchEntity.expiry_date > datetime.datetime.now and 
                BatchEntity.deleted_at == None and 
                BatchEntity.consumed < BatchEntity.volume_liters)
            result = session.exec(stmt)
        return result.all
        
    
    def get_active_batches_until_date(self, date: datetime.datetime) -> list[Batch]:
        with Session(engine) as session:
            stmt = select(BatchEntity).where(
                BatchEntity.expiry_date > datetime.datetime.now and 
                BatchEntity.expiry_date < date and 
                BatchEntity.deleted_at == None and 
                BatchEntity.consumed < BatchEntity.volume_liters)
            result = session.exec(stmt)
        return result.all
    
    def post_batch(self, batch: Batch) -> Batch:
        batch_entity = BatchMapper.to_entity(batch)
        with Session(engine) as session:
            session.add(batch_entity)
            session.commit()
            session.refresh(batch_entity)
        return BatchMapper.to_domain(batch_entity)

    def update_batch(self, batch: Batch) -> Batch:
        batch_entity = BatchMapper.to_entity(batch)
        with Session(engine) as session:
            session.add(batch_entity)
            session.commit()
            session.refresh(batch_entity)
        return BatchMapper.to_domain(batch_entity)