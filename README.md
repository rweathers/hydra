# Hydra

Hydra is a framework for developing hybrid CLI/GUI programs in Python. It is a lightweight wrapper around Tk and is pure Python, with no external dependencies.

## Installation

Download the latest wheel from the [release](release) folder and install with PIP:

```pip install hydra-0.4.0b0-py3-none-any.whl```

## Usage

To use Hydra, you must define:

* A program constants dictionary
* At least one subclass of `BaseAction`
* A subclass of `BaseConfiguration`
* A subclass of `BaseCLI`
* A subclass of `BaseGUI`

Then call the `main()` function. See below for a minimal layout.

```python
from hydra import *

program = {
	# Define program constants
}

class Action(BaseAction):
	def standarize(self):
		# Standardize the user's inputs.

	def validate(self):
		# Raise an exception if any of the user's inputs are invalid.

	def action(self):
		# Perform the task and return a message for the user.

class Configuration(BaseConfiguration):
	def validate(self):
		# Raise an exception if any configuration values are invalid.

class CLI(BaseCLI):
	def define_arguments(self):
		# Define the command line arguments.

	def define_usage(self):
		# Define the command line usage.

	def get_action(self, inputs):
		return Action

class GUI(BaseGUI):
	def define_icon(self):
		# Define the icon.

	def define_menu(self):
		# Define the menu.

	def define_help(self, help):
		# Define the help information.

	def create_widgets(self):
		# Create the widgets.

	def get_action(self, inputs):
		return Action

if __name__ == "__main__": main(program, Configuration, CLI, GUI)
```

See [examples/example.py](examples/example.py) for a functional starter template with specific requirements. Also see the other [examples](examples) and everything in the [docs](docs) folder.
