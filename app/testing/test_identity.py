import unittest
from unittest.mock import patch, Mock, MagicMock
import identity
from freezegun import freeze_time

@patch("identity.raise_for_status", MagicMock())
@patch("identity.requests")
@patch("identity.IDENTITY_URL", "identity")
@patch("identity.TOKEN_USER", "username")
@patch("identity.TOKEN_PASS", "password")
class TestBlob(unittest.TestCase):
    
	@freeze_time("2023-01-01 00:00:00")
	def test_get_token(self, mock_requests):
		mock_requests.request.return_value.json.return_value = {
			"access_token": "token",
			"expires_in": 60
		}
		resp = identity.get_token()
		self.assertEqual("token", resp)
		args, kwargs = mock_requests.request.call_args
		self.assertIn("POST", args)
		self.assertIn("identity/oauth/token", args)
		self.assertEqual(("username", "password"), kwargs['auth'])
		self.assertEqual({'grant_type': 'client_credentials'}, kwargs['data'])