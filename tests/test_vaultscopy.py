#testing VaultScope.py
import unittest
from VAULTSCOPE.VaultScope import is_valid_url, safe_open, assess_risk

class TestVaultScope(unittest.TestCase):
    def test_is_valid_url(self):
        self.assertTrue(is_valid_url("https://example.com"))
        self.assertFalse(is_valid_url("ftp://example.com"))
        self.assertFalse(is_valid_url("example.com"))

    def test_safe_open(self): 
        #assuming 'data/test.txt' exists and is safe
        self.assertRaises(ValueError, safe_open, "../unsafe.txt")
        self.assertRaises(FileNotFoundError, safe_open, "nonexistent.txt")
        self.assertRaises(ValueError, safe_open, "data/../unsafe.txt")

    def test_assess_risk(self):
        self.assertEqual(assess_risk(['saved cards', 'card number']), "High")
        self.assertEqual(assess_risk(['payment', 'billing']), "Medium")
        self.assertEqual(assess_risk([]), "Low")

    if __name__ == "__main__":
        unittest.main()

                        