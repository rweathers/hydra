#! /usr/bin/python3

from hydra import progress
from example import Action

last_update = 0

def test1():
	inputs = {"greeting":"Hello", "name":"World"}
	
	action = Action(inputs, output_progress)
	action.standardize()
	action.validate()
	message = action.action()
	output_progress("")
	
	if message != "Hello World!":
		print("TEST 1 FAILED")
	else:
		print("Test 1 Passed")
		
def output_progress(text, started=None, processed=None, total=None):
	global last_update
	
	p = progress(last_update, text, started, processed, total)
	if p is not None:
		last_update = p[0]
		print(p[1].ljust(80)[0:80-1] + "\r", end="", flush=True)

def main():
	try:
		test1()
	except Exception as e:
		import traceback
		print("ERROR: " + str(e))
		print(traceback.format_exc())

if __name__ == "__main__": main()
