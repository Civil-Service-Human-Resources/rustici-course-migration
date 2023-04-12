import unittest
from unittest.mock import patch, Mock, MagicMock
import learning_catalogue

@patch("learning_catalogue.raise_for_status", MagicMock())
@patch("learning_catalogue.get_token", MagicMock(return_value="token"))
@patch("learning_catalogue.LEARNING_CATALOGUE_URL", "learning_catalogue")
@patch("learning_catalogue.requests")
class TestBlob(unittest.TestCase):
    
	def test_upload_file(self, mock_requests):
		mock_file = Mock()
		mock_file.filename = "filename"
		mock_file.data = b"data"
		mock_requests.request.return_value.headers = {'Location': "url/mediaId"}
		resp = learning_catalogue.upload_file("course_id", mock_file)
		self.assertEqual("mediaId", resp)

		args, kwargs = mock_requests.request.call_args
		self.assertIn("POST", args)
		self.assertIn("learning_catalogue/media?container=course_id", args)
		self.assertEqual({"Authorization": "Bearer token"}, kwargs['headers'])
		
		file = kwargs['files'][0]
		self.assertEqual("file", file[0])
		self.assertEqual("filename", file[1][0])
		self.assertEqual(b"data", file[1][1])
		self.assertEqual("application/zip", file[1][2])