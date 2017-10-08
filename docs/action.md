# class BaseAction

Base class for defining actions.

## Attributes

* `inputs` - User input dictionary.
* `progress` - Callback function for user progress updates.

## Functions

### BaseAction(inputs, progress)

Initialize the object.

_Paramaters_:

* `inputs` - User input dictionary.
* `progress` - Callback function for user progress updates.

### standardize()

Standardize the user's inputs.

### validate()

Raise an exception if any of the user's inputs are invalid.

### action()

Perform the task and return a message for the user.

### expand(field)

Convert a CSV string into a list of filenames and expand wildcard filenames.

_Paramaters_:

* `field` - Field name to modify.

### open(filename, mode="r", encoding="utf-8")

Return sys.stdin (for filename == "STDIN"), sys.stdout (for filename == "STDIN") or a file handle.

_Paramaters_:

* `filename` - "STDIN", "STDOUT" or a filename.
* `mode` - File open mode.
* `encoding` - File encoding.
