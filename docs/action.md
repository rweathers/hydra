# class BaseAction

Base class for defining actions.

## Attributes

* `inputs` - User input dictionary.
* `progress` - Callback function for user progress updates.

## Functions

### BaseAction(inputs, progress=None)

Initialize the object.

_Parameters_:

* `inputs` - User input dictionary.
* `progress` - Callback function for user progress updates.

### standardize()

Standardize the user's inputs.

### validate()

Raise an exception if any of the user's inputs are invalid.

### action()

Perform the task and return a message for the user.

### execute()

Call standardize, validate and action. Return the result from action.

### expand(field)

Convert a CSV string into a list of filenames and expand wildcard filenames.

_Parameters_:

* `field` - Field name to modify.

### open(filename, mode="r", encoding="utf-8")

Return sys.stdin (for filename == "STDIN"), sys.stdout (for filename == "STDIN") or a file handle.

_Parameters_:

* `filename` - "STDIN", "STDOUT" or a filename.
* `mode` - File open mode.
* `encoding` - File encoding.
