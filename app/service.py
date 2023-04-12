from learning_catalogue import upload_file
from blob import load_zip_file, delete_elearning, does_zip_exist
from database import get_migrations, save_migration, get_all_migrations
from elasticsearch import get_manifest_for_zip, update_media_id_for_module_and_get_existing, update_media_id_for_module
from rustici import upload_course, delete_course
from models.ELearningMigration import ELearningMigration
from models.ResetOpts import ResetOpts
from log import logger

def check_all(check_zip: bool):
	check(get_all_migrations(), check_zip)

def check_selected(module_ids: list[str], check_zip: bool):
	check(get_migrations(module_ids), check_zip)

def check(migrations: list[ELearningMigration], check_zip: bool):
	logger.info(f"Checking {len(migrations)} modules:")
	output=[]
	for migration in migrations:
		if check_zip:
			zip_output = "Zip exists in blob storage." if does_zip_exist(migration.zip_file_name) else "zip DOES NOT EXIST in blob storage."
			output.append(f"{migration.get_course_module_id()} | {migration.zip_file_name}.zip | {zip_output}")
		else:
			output.append(str(migration))
	logger.info("\n\n".join([str(out) for out in output]))

def migrate_all():
	logger.info("Migrating all modules")
	migrations = get_all_migrations()
	if migrations:
		migrate(migrations)
	else:
		logger.info("No migrations found")

def migrate_selected(module_ids: list[str]):
	logger.info(f"Attempting to migrate the following modules: " + ", ".join(module_ids))
	migrations = get_migrations(module_ids)
	migrate(migrations)

def migrate(migrations: list[ELearningMigration]):
	errors = []
	for migration in migrations:
		try:
			logger.info(f"Migrating {migration.get_course_module_id()} (zip: '{migration.zip_file_name}')")
			if not migration.media_id:
				migration = migrate_to_catalogue(migration)
			else:
				logger.info(f"Migration {migration.get_course_module_id()} already has a media ID ({migration.media_id}). Skipping catalogue migration.")
			if not migration.manifest_file:
				migration = get_and_save_manifest(migration)
			else:
				logger.info(f"Migration {migration.get_course_module_id()} already has a manifest file ({migration.manifest_file}). Skipping manifest search.")
			if not migration.rustici_course_id:
				upload_course_to_rustici(migration)
			else:
				logger.info(f"Migration {migration.get_course_module_id()} already has a Rustici course ID ({migration.rustici_course_id}). Skipping Rustici course upload.")
			logger.info("Successfully migrated E-Learning")
		except Exception as e:
			logger.warn("Migration failed, storing details")
			errors.append(f"FAILED MIGRATION {migration.get_course_module_id()}: {str(e)}")
	if errors:
		logger.error("There were errors processing some migrations:\n" + "\n".join(errors))

def reset_selected(module_ids: list[str], options: ResetOpts):
	logger.info("Attempting to reset the following modules: " + ", ".join(module_ids))
	migrations = get_migrations(module_ids)
	reset(migrations, options)

def reset(migrations: list[ELearningMigration], reset_options: ResetOpts):
	errors = []
	for migration in migrations:
		try:
			if migration.rustici_course_id:
				logger.info(f"Deleting migration {migration.get_course_module_id()} from Rustici Engine")
				delete_course_from_rustici(migration)
			else:
				logger.info("Migration marked for deletion from Rustici but migration does not have a rustici course ID")

			if reset_options.reset_zip_upload:
				if migration.media_id:
					logger.info(f"Resetting blob storage upload and media ID")
					reset_migration_to_catalogue(migration)
				else:
					logger.info("Blob reset parameter passed in for migration but migration does not have a media ID")
			else:
				logger.info("Reset zip upload flag was not passed, skipping")
		except Exception as e:
			logger.warn("Migration failed, storing details")
			errors.append(f"FAILED MIGRATION {migration.get_course_module_id()}: {str(e)}")
	if errors:
		logger.error("There were errors processing some migrations:\n" + "\n".join(errors))

def delete_course_from_rustici(migration: ELearningMigration):
	delete_course(migration.course_id, migration.module_id)
	migration.rustici_course_id = None
	save_migration(migration)
	logger.info(f"Successfully deleted migration {migration.get_course_module_id()} from Rustici Engine")

def reset_migration_to_catalogue(migration: ELearningMigration):
	logger.info("Deleting e-learning from blob storage")
	delete_elearning(migration.course_id, migration.media_id)
	logger.info("Setting media ID back to previous value")
	update_media_id_for_module(migration.course_id, migration.module_id, migration.existing_media_id)
	migration.media_id = None
	migration.manifest_file = None
	migration.existing_media_id = None
	save_migration(migration)
	logger.info(f"Successfully reset catalogue migration for {migration.get_course_module_id()}")

def migrate_to_catalogue(migration: ELearningMigration):
	logger.info(f"Downloading '{migration.zip_file_name}'")
	zip_file = load_zip_file(migration.zip_file_name)
	logger.info(f"Uploading '{migration.zip_file_name}'")
	media_id = upload_file(migration.course_id, zip_file)
	migration.media_id = media_id
	existing_media_id = update_media_id_for_module_and_get_existing(migration.course_id, migration.module_id, migration.media_id)
	migration.existing_media_id = existing_media_id
	save_migration(migration)
	logger.info(f"Migration {migration.get_course_module_id()} sucessfully migrated to course catalogue. Media ID: {media_id}")
	return migration

def get_and_save_manifest(migration: ELearningMigration):
	logger.info(f"Getting manifest for media ID {migration.media_id}")
	manifest_file = get_manifest_for_zip(migration.media_id)
	migration.manifest_file = manifest_file
	save_migration(migration)
	logger.info(f"Successfully fetched manifest for migration {migration.get_course_module_id()}. Manifest file: {manifest_file}")
	return migration

def upload_course_to_rustici(migration: ELearningMigration):
	logger.info(f"Uploading e-learning to Rustici Engine")
	rustici_course_id = upload_course(migration.course_id, migration.module_id, migration.media_id, migration.manifest_file)
	migration.rustici_course_id = rustici_course_id
	save_migration(migration)
	logger.info(f"Migration {migration.get_course_module_id()} successfully uploaded to Rustici Engine. Rustici course ID: {rustici_course_id}")
