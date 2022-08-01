from django.test import TestCase, Client
from django.urls import reverse  


class IndexpageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        c = Client()  
        response = c.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        c = Client()  
        response = c.get(reverse("index"))
        self.assertTemplateUsed(response, "auctions/index.html")
