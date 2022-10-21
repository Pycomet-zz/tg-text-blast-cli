import unittest
from utils import TextVerifiedApi, TelegramApi

print("Running Tests")




class TestTelegramApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.api = TelegramApi()
        cls.api.start

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.stop

    def test_create_account(self):
        result = self.api.create_account("TestingNewBie")
        print(result)
        self.assertEqual(result['session'], str)

if __name__ == '__main__':
    unittest.main()