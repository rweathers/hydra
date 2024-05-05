# class BaseCLI

Base class for defining the command line interface.

## Attributes

* `prog` - Program constants dictionary.
* `conf` - Configuration dictionary.
* `arguments` - Command line arguments (sys.argv).
* `usage` - Command line usage.
* `last_update` - Unix timestamp of last user progress update.
* `twidth` - terminal width.
* `inputs` - User input dictionary.

## Functions

### BaseCLI(prog, conf, argv)

Initialize the object.

_Parameters_:

* `prog` - Program constants dictionary.
* `conf` - Configuration dictionary.
* `argv` - Command line arguments (sys.argv).

### define_arguments()

Define the command line arguments.

### define_usage()

Define the command line usage.

### parse_arguments(argv)

Parse the command line arguments and return them in a dictionary.

_Parameters_:

* `argv` - Command line arguments (sys.argv).

### print_help()

Print the help information to standard out.

### print_version()

Print the program name and version.

### print_license()

Print the program's license information.

### output_progress(text, started=None, processed=None, total=None)

Print progress information to standard out.

_Parameters_:

* `text` - Progress text.
* `started` - Unix timestamp of when the program started.
* `processed` - Counter of processed items.
* `total` - Total number of items to process.

### user_message(message)

Show a message to the user.

_Paramaters_:

* `message` - Message text.

### user_warning(message)

Show a warning message to the user.

_Paramaters_:

* `message` - Message text.

### user_error(message)

Show an error message to the user.

_Paramaters_:

* `message` - Message text.

### user_confirm(message, include_cancel=False)

Ask the user for confirmation and return True, False or None.

_Paramaters_:

* `message` - Message text.
* `include_cancel` - Flag to enable the cancel option.

### user_input(message, default="")

Ask the user for a value and return it.

_Paramaters_:

* `message` - Message text.
* `default` - A default value.

### get_action(inputs)

Return the BaseAction subclass to use.

_Parameters_:

* `inputs` - User input dictionary.

### action()

Validate the user's input and perform the action.
