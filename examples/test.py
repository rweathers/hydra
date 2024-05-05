#! /usr/bin/python3

import unittest
from example import program, Configuration, Action

class TestAction(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.conf = Configuration(program).conf
	
	def test_validation(self):
		inputs = {"greeting":"", "name":""}
		with self.assertRaisesRegex(ValueError, "^Greeting required\nName required$"):
			Action({**self.conf, **inputs}, interface="test").execute()
	
	def test_greeting(self):
		inputs = {"greeting":"Hello", "name":"World"}
		message = Action({**self.conf, **inputs}, interface="test").execute()
		self.assertEqual(message, "Hello World!")

if __name__ == '__main__': unittest.main()
