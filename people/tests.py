from django.test import TestCase

from .models import User

class UserModelTest(TestCase):
    def test_model_should_not_be_abstract(self):
        self.assertFalse(User.Meta.abstract)

