import unittest
from unittest.mock import MagicMock, patch
from utils.honeypot_check import check_honeypot

class TestCheckHoneypot(unittest.TestCase):
    def setUp(self):
        self.mock_token = MagicMock()
        self.wallet_address = "0x1234567890abcdef1234567890abcdef12345678"

    def test_owner_renounced_and_balanceof_callable(self):
        # Mock owner() call
        self.mock_token.functions.owner.return_value.call.return_value = "0x0000000000000000000000000000000000000000"
        # Mock balanceOf call
        self.mock_token.functions.balanceOf.return_value.call.return_value = 100

        result = check_honeypot(self.mock_token, self.wallet_address)
        self.assertTrue(result)

    def test_owner_not_renounced(self):
        self.mock_token.functions.owner.return_value.call.return_value = "0xABC"
        result = check_honeypot(self.mock_token, self.wallet_address)
        self.assertFalse(result)

    def test_owner_method_missing(self):
        # Raise exception for owner()
        self.mock_token.functions.owner.return_value.call.side_effect = Exception("Method not found")
        self.mock_token.functions.balanceOf.return_value.call.return_value = 50

        result = check_honeypot(self.mock_token, self.wallet_address)
        self.assertTrue(result)  # Because balanceOf works, and owner() was skipped

    def test_balanceof_not_callable(self):
        self.mock_token.functions.owner.return_value.call.return_value = "0x0000000000000000000000000000000000000000"
        self.mock_token.functions.balanceOf.return_value.call.side_effect = Exception("Failed call")

        result = check_honeypot(self.mock_token, self.wallet_address)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
