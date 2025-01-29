# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse

class ParseXMLTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_xxe(self):
        malicious_xml = """<?xml version="1.0"?>
        <!DOCTYPE root [
        <!ENTITY xxe SYSTEM "file:///etc/passwd">
        ]>
        <root>&xxe;</root>"""

        response = self.client.post('/parse_xml/', {'xml': malicious_xml})
        self.assertNotIn("root", response.content.decode())

class CommentXSSTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_xss(self):
        malicious_comment = "<script>alert('XSS')</script>"
        response = self.client.get(f'/comment?comment={malicious_comment}')
        self.assertNotIn(malicious_comment, response.content.decode())