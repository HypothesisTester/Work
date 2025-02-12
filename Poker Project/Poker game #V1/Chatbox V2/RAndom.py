import unittest
from client import process_message_for_emojis, is_message_too_long, is_sending_too_quickly
import time

class TestClient(unittest.TestCase):

    def test_emoji_conversion(self):
        self.assertEqual(process_message_for_emojis("Hello :smile:"), "Hello 😄")
        self.assertEqual(process_message_for_emojis("Goodbye :wave:"), "Goodbye 👋")

    def test_message_length(self):
        self.assertTrue(is_message_too_long("a" * 201))
        self.assertFalse(is_message_too_long("a" * 200))

    def test_rate_limiting(self):
        # Resetting the last_message_time to simulate the time lapse
        client.last_message_time = time.time() - 1
        self.assertFalse(is_sending_too_quickly())  # Should be fine since 1 second has passed
        self.assertTrue(is_sending_too_quickly())   # Immediately sending another should be too quick
        time.sleep(1)
        self.assertFalse(is_sending_too_quickly())  # After 1 second, should be fine again

if __name__ == "__main__":
    unittest.main()

import unittest
from client import process_message_for_emojis, is_message_too_long, is_sending_too_quickly
import time

class TestClient(unittest.TestCase):

    def test_emoji_conversion(self):
        self.assertEqual(process_message_for_emojis("Hello :smile:"), "Hello 😄")
        self.assertEqual(process_message_for_emojis("Goodbye :wave:"), "Goodbye 👋")

    def test_message_length(self):
        self.assertTrue(is_message_too_long("a" * 201))
        self.assertFalse(is_message_too_long("a" * 200))

    def test_rate_limiting(self):
        # Resetting the last_message_time to simulate the time lapse
        client.last_message_time = time.time() - 1
        self.assertFalse(is_sending_too_quickly())  # Should be fine since 1 second has passed
        self.assertTrue(is_sending_too_quickly())   # Immediately sending another should be too quick
        time.sleep(1)
        self.assertFalse(is_sending_too_quickly())  # After 1 second, should be fine again

if __name__ == "__main__":
    unittest.main()
