# Functions

### hydra.progress(last_update, text, started=None, processed=None, total=None)

Return progress text with optional time elapsed and estimated time to complete.

_Paramaters_:

* `text` - Progress text.
* `started` - Unix timestamp of when the program started.
* `processed` - Counter of processed items.
* `total` - Total number of items to process.

### hydra.localize_dir(path)

Return the given path with directory separator characters converted to the local os character and with one appened to the end.

### hydra.localize_file(filename)

Return the given filename with directory separator characters converted to the local os character.

### hydra.setdefaults(primary, secondary)

Return a dictionary with the values of primary and secondary merged, with primary taking precedence over secondary.

_Paramaters_:

* `primary` - The primary dictionary.
* `secondary` - The secondary dictionary.

### hydra.error_output(ex, error_path)

Write error details to a file.

_Paramaters_:

* `ex` - An exception object.
* `error_path` - Error filename.

### hydra.main(prog, configuration_class, cli_class, gui_class)

Run the program.

_Paramaters_:

* `prog` - Program constants dictionary.
* `configuration_class` - A BaseConfiguration subclass.
* `cli_class` - A BaseCI subclass.
* `gui_class` - A BaseGUI subclass.
