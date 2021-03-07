#! /usr/bin/python3

from hydra import progress
from example import Action

last_update = 0

def test1():
	print("Running Test 1 ... ", end="", flush=True)
	
	inputs = {"greeting":"Hello", "name":"World"}
	action = Action(inputs)
	message = action.execute()
	
	if message == "Hello World!":
		print("PASS")
	else:
		print("FAIL")

def main():
	try:
		test1()
	except Exception as e:
		import traceback
		print("ERROR: " + str(e))
		print(traceback.format_exc())

if __name__ == "__main__": main()
