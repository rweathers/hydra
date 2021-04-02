# Functions

### hydra.progress(last_update, text, started=None, processed=None, total=None)

Return progress text with optional time elapsed and estimated time to complete.

_Parameters_:

* `text` - Progress text.
* `started` - Unix timestamp of when the program started.
* `processed` - Counter of processed items.
* `total` - Total number of items to process.

### hydra.setdefaults(primary, secondary)

Return a dictionary with the values of primary and secondary merged, with primary taking precedence over secondary.

_Parameters_:

* `primary` - The primary dictionary.
* `secondary` - The secondary dictionary.

### hydra.error_output(ex, error_path)

Write error details to a file.

_Parameters_:

* `ex` - An exception object.
* `error_path` - Error filename.

### hydra.main(prog, configuration_class, cli_class, gui_class)

Run the program.

_Parameters_:

* `prog` - Program constants dictionary.
* `configuration_class` - A BaseConfiguration subclass or None.
* `cli_class` - A BaseCI subclass or None.
* `gui_class` - A BaseGUI subclass or None.
