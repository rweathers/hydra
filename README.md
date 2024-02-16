# Hydra

Hydra is a framework for developing hybrid CLI/GUI programs in Python. It is a lightweight wrapper around Tk and is pure Python, with no external dependencies.

## Installation

Install latest version with PIP:

```pip install hydra-ui```

Or, download the latest wheel from the [release](release) folder and install with PIP:

```pip install hydra_ui-1.0.0-py3-none-any.whl```

NOTE: If you are upgrading from a previous version, do so one release at a time and read the [change log](CHANGELOG.md).

## Usage

To use Hydra, you must define:

* A program constants dictionary
* A subclass of `BaseConfiguration` if using a config file
* At least one subclass of `BaseAction`
* A subclass of `BaseCLI` and/or `BaseGUI`

Then call the `main()` function. See below for a minimal layout.

```python
from hydra import *

program = {
	# Define program constants
}

class Configuration(BaseConfiguration):
	def validate(self):
		# Raise an exception if any configuration values are invalid.

class Action(BaseAction):
	def standarize(self):
		# Standardize the user's inputs.

	def validate(self):
		# Raise an exception if any of the user's inputs are invalid.

	def action(self):
		# Perform the task and return a message for the user.

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
