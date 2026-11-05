import unittest
from auditor import audit
class Tests(unittest.TestCase):
    def test_pass(self):
        self.assertTrue(audit("Hello world",{"min_chars":5,"required_terms":["world"]})["passed"])
    def test_missing(self):
        self.assertEqual(audit("Hello",{"required_terms":["world"]})["issues"],["missing:world"])
    def test_banned(self):
        self.assertEqual(audit("Secret",{"banned_terms":["secret"]})["issues"],["banned:secret"])
    def test_url(self):
        self.assertIn("url_present",audit("https://example.com",{"no_urls":True})["issues"])
    def test_invalid_rule(self):
        with self.assertRaises(ValueError): audit("hi",{"min_chars":-1})
    def test_max(self):
        self.assertIn("too_long",audit("hello",{"max_chars":2})["issues"])
if __name__=="__main__": unittest.main()
