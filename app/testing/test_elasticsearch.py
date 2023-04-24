import unittest
from unittest.mock import patch, Mock, MagicMock
import elasticsearch

@patch("elasticsearch.raise_for_status", MagicMock())
@patch("elasticsearch.requests")
@patch("elasticsearch.ELASTIC_URL", "elastic")
@patch("elasticsearch.ELASTIC_USERNAME", "username")
@patch("elasticsearch.ELASTIC_PASSWORD", "password")
class TestBlob(unittest.TestCase):

    def setUp(self) -> None:
        elasticsearch.CACHE = {}
        return super().setUp()
    
    def test_get_manifest(self, mock_requests):
        mock_response = Mock()
        mock_response.json.return_value = {
            "_source": {
                "metadata": {
                    "elearning_manifest": "MANIFEST.xml"
                }
            }
        }
        mock_requests.request.return_value = mock_response
        resp = elasticsearch.get_manifest_for_zip("media_id")
        self.assertEqual(resp, "MANIFEST.xml")

    def test_update_media_id(self, mock_requests):
        get_course_response = Mock()
        get_course_response.json.return_value = {
            "_source": {
                "modules": [
                    {
                        "id": "module_id",
                        "mediaId": "existing_media_id"
                    }
                ]
            }
        }
        mock_requests.request.side_effect = [get_course_response, Mock()]

        elasticsearch.update_media_id_for_module("course_id", "module_id", "new_media_id")
        args, kwargs = mock_requests.request.call_args
        self.assertIn('POST', args)
        self.assertEqual(kwargs['url'], "elastic/courses/_update/course_id")
        self.assertEqual(kwargs['json'], {
                "doc": {
                    "modules": [
                        {
                            "id": "module_id",
                            "mediaId": "new_media_id"
                        }
                    ]
                }
            })
        self.assertEqual(kwargs['auth'], ("username", "password"))

    def test_update_media_id_and_get_existing(self, mock_requests):
        get_course_response = Mock()
        get_course_response.json.return_value = {
            "_source": {
                "modules": [
                    {
                        "id": "module_id",
                        "mediaId": "existing_media_id"
                    }
                ]
            }
        }
        mock_requests.request.side_effect = [get_course_response, Mock()]

        resp = elasticsearch.update_media_id_for_module_and_get_existing("course_id", "module_id", "new_media_id")
        args, kwargs = mock_requests.request.call_args
        self.assertIn('POST', args)
        self.assertEqual(kwargs['url'], "elastic/courses/_update/course_id")
        self.assertEqual(kwargs['json'], {
                "doc": {
                    "modules": [
                        {
                            "id": "module_id",
                            "mediaId": "new_media_id"
                        }
                    ]
                }
            })
        self.assertEqual(kwargs['auth'], ("username", "password"))
        self.assertEqual(resp, "existing_media_id")
    