import unittest
from unittest.mock import MagicMock, patch
import json
import srun_login_pro as srun

class TestSRUNAuthenticator(unittest.TestCase):

    def setUp(self):
        self.cfg = srun.SrunConfig(username="test_user", password="test_password")
        self.client = srun.SrunClient(self.cfg)

    def test_base64_encoding(self):
        test_str = "hello world"
        encoded = self.client._get_base64(test_str, srun.SrunAuthContext.ALPHA)
        self.assertTrue(all(c in srun.SrunAuthContext.ALPHA or c == '=' for c in encoded))
        self.assertEqual(encoded, self.client._get_base64(test_str, srun.SrunAuthContext.ALPHA))

    def test_md5_hmac(self):
        password = "test_password"
        token = "test_token"
        hmd5 = hrun_md5 = srun.hmac.new(token.encode(), password.encode(), srun.hashlib.md5).hexdigest()
        self.assertEqual(len(hrun_md5), 32)

    def test_xencode_logic(self):
        msg = "test_data"
        token = "test_token"
        encoded = self.client._xencode(msg, token)
        self.assertTrue(len(encoded) > 0)

    @patch('requests.Session.get')
    def test_authenticate_flow_success(self, mock_get):
        # Mocking multiple calls in sequence
        resp1 = MagicMock()
        resp1.status_code = 200
        resp1.text = 'jQuery123({"client_ip":"1.2.3.4"})'
        
        resp2 = MagicMock()
        resp2.status_code = 200
        resp2.text = 'jQuery456({"challenge":"mock_token"})'
        
        resp3 = MagicMock()
        resp3.status_code = 200
        resp3.text = 'jQuery789({"res":"ok", "login_ok": true})'
        
        mock_get.side_effect = [resp1, resp2, resp3]
        
        success = self.client.authenticate()
        self.assertTrue(success)

    def test_is_connected_baidu(self):
        with patch.object(self.client.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            self.assertTrue(self.client.is_connected())

if __name__ == '__main__':
    unittest.main()
