import unittest
from unittest.mock import patch, Mock, MagicMock
from models.ELearningMigration import ELearningMigration
import service

@patch("service.save_migration")
class TestBlob(unittest.TestCase):

	def __get_migration(self):
		return ELearningMigration(course_id="course_id", module_id="module_id",
			    zip_file_name="zip.zip", existing_media_id="existing_id",
				media_id="media_id", manifest_file="manifest.xml",
				rustici_course_id="course_id.module_id")
    
	@patch("service.delete_course")
	def test_delete_from_rustici(self, delete_course, save_migration):
		migration = self.__get_migration()
		service.delete_course_from_rustici(migration)
		delete_course.assert_called_once_with("course_id", "module_id")
		args, kwargs = save_migration.call_args
		self.assertIsNone(args[0].rustici_course_id)

	@patch("service.delete_elearning")
	@patch("service.update_media_id_for_module")
	def test_reset_migration_to_catalogue(self, update_media_id_for_module, delete_elearning, save_migration):
		migration = self.__get_migration()
		service.reset_migration_to_catalogue(migration)
		delete_elearning.assert_called_once_with("course_id", "media_id")
		update_media_id_for_module.assert_called_once_with("course_id", "module_id", "existing_id")
		args, kwargs = save_migration.call_args
		self.assertIsNone(args[0].media_id)
		self.assertIsNone(args[0].manifest_file)
		self.assertIsNone(args[0].existing_media_id)

	@patch("service.load_zip_file")
	@patch("service.upload_file")
	@patch("service.update_media_id_for_module_and_get_existing")
	def test_migrate_to_catalogue(self, update_media_id_for_module_and_get_existing,
			       upload_file, load_zip_file, save_migration):
		migration = self.__get_migration()
		migration.media_id = None
		migration.existing_media_id = None
		load_zip_file.return_value = "zipFile"
		upload_file.return_value = "media_id"
		update_media_id_for_module_and_get_existing.return_value = "existing_id"

		service.migrate_to_catalogue(migration)
		load_zip_file.assert_called_once_with("zip.zip")
		upload_file.assert_called_once_with("course_id", "zipFile")
		update_media_id_for_module_and_get_existing.assert_called_once_with("course_id", "module_id", "media_id")
		args, kwargs = save_migration.call_args
		self.assertEqual("media_id", args[0].media_id)
		self.assertEqual("existing_id", args[0].existing_media_id)

	@patch("service.get_manifest_for_zip")
	def test_get_and_save_manifest(self, get_manifest_for_zip, save_migration):
		migration = self.__get_migration()
		migration.manifest_file = None
		get_manifest_for_zip.return_value = "manifest.xml"
		service.get_and_save_manifest(migration)
		get_manifest_for_zip.assert_called_once_with("media_id")
		args, kwargs = save_migration.call_args
		self.assertEqual("manifest.xml", args[0].manifest_file)

	@patch("service.upload_course")
	def test_get_and_save_manifest(self, upload_course, save_migration):
		migration = self.__get_migration()
		migration.rustici_course_id = None
		upload_course.return_value = "course_id.module_id"
		service.upload_course_to_rustici(migration)
		upload_course.assert_called_once_with("course_id", "module_id", "media_id", "manifest.xml")
		args, kwargs = save_migration.call_args
		self.assertEqual("course_id.module_id", args[0].rustici_course_id)