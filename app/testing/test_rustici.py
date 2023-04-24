import unittest
from unittest.mock import patch, Mock, MagicMock
import rustici

@patch("rustici.raise_for_status", MagicMock())
@patch("rustici.requests")
@patch("rustici.RUSTICI_API_URL", "rustici/api")
@patch("rustici.RUSTICI_CDN_URL", "rustici/cdn")
@patch("rustici.RUSTICI_USERNAME", "username")
@patch("rustici.RUSTICI_PASSWORD", "password")
@patch("rustici.RUSTICI_TENTANT", "tenant")
class TestBlob(unittest.TestCase):

	def test_upload_course(self, mock_requests):
		resp = rustici.upload_course("course_id", "module_id", "media_id", "manifest.xml")
		self.assertEqual("course_id.module_id", resp)
		args, kwargs = mock_requests.request.call_args
		self.assertIn("POST", args)
		self.assertEqual("rustici/api/courses?courseId=course_id.module_id", kwargs['url'])
		self.assertEqual({"engineTenantName": "tenant"}, kwargs['headers'])
		self.assertEqual(("username", "password"), kwargs['auth'])
		self.assertEqual({
			"referenceRequest": {
				"webPathToCourse": "rustici/cdn/course_id/media_id",
				"url": "rustici/cdn/course_id/media_id/manifest.xml"
			}
		}, kwargs['json'])