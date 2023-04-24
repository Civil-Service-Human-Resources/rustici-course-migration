from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session
from models.ELearningMigration import ELearningMigration
from models.Base import Base
from config import get_database_connection, LOG_DB_TRANSACTIONS
from log import logger

__db = get_database_connection()
engine = None

def get_engine():
	return create_engine(__db, echo=LOG_DB_TRANSACTIONS)

def setup():
	logger.info("Beginning setup")
	Base.metadata.create_all(get_engine())
	logger.info("Setup complete")

def get_all_migrations():
	with Session(get_engine(), expire_on_commit=False) as session:
		stmt = select(ELearningMigration)
		migrations = session.scalars(stmt).all()
		session.expunge_all()
		return migrations

def get_migration(module_id):
	with Session(get_engine(), expire_on_commit=False) as session:
		stmt = (select(ELearningMigration)
	  			.where(ELearningMigration.module_id == module_id))
		migration = session.scalar(stmt)
		session.expunge_all()
		return migration

def get_migrations(module_ids: list[str]):
	with Session(get_engine(), expire_on_commit=False) as session:
		stmt = (select(ELearningMigration)
	  			.where(ELearningMigration.module_id.in_(module_ids)))
		migrations = session.scalars(stmt).all()
		session.expunge_all()
		return migrations

def save_migration(migration: ELearningMigration):
	with Session(get_engine(), expire_on_commit=False) as session:
		session.add(migration)
		session.commit()