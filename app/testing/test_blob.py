import unittest
from unittest.mock import patch, Mock
import blob

class TestBlob(unittest.TestCase):
    
	@patch('blob.zip_service')
	def test_zip_exists(self, mock_zip_service):
		mock_zip_service.list_blob_names.return_value = ["blob1","blob2"]
		self.assertFalse(blob.does_zip_exist("blob3"))
		self.assertTrue(blob.does_zip_exist("blob1"))

	@patch('blob.zip_service')
	def test_load_zip_file(self, mock_zip_service):
		mock_zip_service.download_blob.return_value.readall.return_value = b"bytes"
		resp = blob.load_zip_file("zip_file")
		self.assertEqual(resp.filename, "zip_file")
		self.assertEqual(resp.data, b"bytes")
	
	@patch('blob.elearning_service')
	def test_delete_elearning(self, mock_elearning_service):
		mock_elearning_service.list_blobs.return_value = [Mock(), Mock()]
		blob.delete_elearning("course_id", "media_id")
		mock_elearning_service.list_blobs.assert_called_once_with("course_id/media_id")
		self.assertEqual(mock_elearning_service.delete_blob.call_count, 2)