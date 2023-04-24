from models.Base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer

class ELearningMigration(Base):
	__tablename__ = "migrations"
    
	id = mapped_column(Integer, primary_key=True)
	course_id = mapped_column(String(40), nullable=False)
	module_id = mapped_column(String(40), nullable=False)
	zip_file_name = mapped_column(String(400), nullable=False)
	existing_media_id = mapped_column(String(40), nullable=True)
	media_id = mapped_column(String(40), nullable=True)
	manifest_file = mapped_column(String(50), nullable=True)
	rustici_course_id = mapped_column(String(50), nullable=True)

	def is_migrated(self):
		return bool(self.rustici_course_id)
	
	def get_course_module_id(self):
		return f"{self.course_id} / {self.module_id}"

	def __repr__(self):
		return f"course_id: '{self.course_id}' | module_id: '{self.module_id}' | zip_file_name: '{self.zip_file_name}' | existing_media_id: '{self.existing_media_id}' | media_id: '{self.media_id}' | manifest_file: '{self.manifest_file}' | rustici_course_id: '{self.rustici_course_id}'"