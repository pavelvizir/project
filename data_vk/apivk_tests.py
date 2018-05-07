from data_vk.apivk import *
import unittest


# my_user_id = 486369485
friend_user_id = 5967930
class TestVkAPi(unittest.TestCase):

    def test_get_dialogs(self):
        dialogs = get_dialogs()
        self.assertIsNotNone(dialogs)
        self.assertTrue(type(dialogs['items']) is list)
        self.assertTrue(type(dialogs['count']) is int)
        print(dialogs)

    def test_get_history(self):
        history = get_all_history(friend_user_id)
        print(history)
