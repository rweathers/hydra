#! /usr/bin/python3

from example import program, Configuration, Action

def test1(inputs):
	print("Running Test 1 ... ", end="", flush=True)
	
	inputs.update({"greeting":"Hello", "name":"World"})
	action = Action(inputs)
	message = action.execute()
	
	if message == "Hello World!":
		print("PASS")
	else:
		print("FAIL")

def main():
	try:
		conf = Configuration(program)
		test1(conf.conf)
	except Exception as e:
		import traceback
		print("\n\n{}".format(traceback.format_exc()))

if __name__ == "__main__": main()
