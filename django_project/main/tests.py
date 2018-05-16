from django.test import TestCase

# Create your tests here.

from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

# Define this after the ModelTestCase
from main.models import Data


class testPostgresFullTextSearch(TransactionTestCase):
    fixtures = ['Data.json']
from main.models import Data


class testPostgresFullTextSearch(TransactionTestCase):
    fixtures = ['Data.json']
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables.
        Data.objects.create(PID=1,
                            CID=1,
                            psource="text",
                            csource="text",
                            typedoc="text",
                            metadata="text",
                            data_main="text",
                            additional_data="text")
        self.client = APIClient()

    """
    def test_fulltextsearch(self):
        response = self.client.get("/main/search?search=text")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #TODO распасить и проверить response.content

