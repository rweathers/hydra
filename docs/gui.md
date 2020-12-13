# class BaseGUI

Base class for defining the graphical user interface.

## Attributes

* `prog` - Program constants dictionary.
* `conf` - Configuration dictionary.
* `icon` - Base-64 encoded string representing the icon.
* `menu` - Dictionary defining the menu.
* `help` - List of dictionaries defining the help.
* `widgets` - Dictionary of the widget objects.
* `row` - The next row to use in the grid layout.
* `padding` - Padding to use for all widgets.
* `text_width` - Width of text boxes.
* `last_update` - Unix timestamp of last user progress update.

## Functions

### BaseGUI(master, prog, conf)

Initialize the object.

_Parameters_:

* `master` - Tk Root object.
* `prog` - Program constants dictionary.
* `conf` - Configuration dictionary.

### define_icon()

Define the icon.

### define_menu()

Define the menu.

### create_menu()

Create the menu and add it to the root window.

### open_config()

Open the configuration file.

### define_help(help)

Define the help information.

_Parameters_:

* `help` - A tk Text object.

### show_help()

Show the help window.

### show_about()

Open the about window.

### create_widgets()

Create the widgets.

### create_title(text)

Add a title label to the root window.

_Parameters_:

* `text` - Title text.

### create_entry(parent, name, text, default="", largs={}, wargs={}, lgrid={}, wgrid={})

Add an entry to the given parent.

_Parameters_:

* `parent` - A Tk frame.
* `name` - Name of the widget.
* `text` - Text for the label.
* `default` - Default value of the widget.
* `largs` - Constructor arguments for the label.
* `wargs` - Constructor arguments for the widget.
* `lgrid` - grid() arguments for the label.
* `wgrid` - grid() arguments for the widget.


### create_browse(parent, name, text, command, initialdir=None, initialfile=None, filetypes=[], default="", largs={}, wargs={}, bargs={}, lgrid={}, wgrid={}, bgrid={})

Add a file browser to the given parent.

_Parameters_:

* `parent` - A Tk frame.
* `name` - Name of the widget.
* `text` - Text for the label.
* `command` - Function callback (one of self.get_inputs, self.get_input, self.get_output or self.get_folder)
* `initialdir` - Starting directory for the file dialog.
* `initialfile` - Starting filename for the file dialog.
* `filetypes` - List of allowed file types.
* `default` - Default value of the widget.
* `largs` - Constructor arguments for the label.
* `wargs` - Constructor arguments for the widget.
* `bargs` - Constructor arguments for the browse button.
* `lgrid` - grid() arguments for the label.
* `wgrid` - grid() arguments for the widget.
* `bgrid` - grid() arguments for the browse button.

### create_combobox(parent, name, text, values, default=None, largs={}, wargs={}, lgrid={}, wgrid={})

Add a combobox to the given parent.

_Parameters_:

* `parent` - A Tk frame.
* `name` - Name of the widget.
* `text` - Text for the label.
* `values` - List of values to use.
* `default` - Default value of the widget.
* `largs` - Constructor arguments for the label.
* `wargs` - Constructor arguments for the widget.
* `lgrid` - grid() arguments for the label.
* `wgrid` - grid() arguments for the widget.


### create_listbox(parent, name, text, values, selectmode=tk.EXTENDED, largs={}, wargs={}, lgrid={}, wgrid={})

Add a listbox to the given parent.

_Parameters_:

* `parent` - A Tk frame.
* `name` - Name of the widget.
* `text` - Text for the label.
* `values` - List of values to use.
* `selectmode` - Listbox selectmode argument.
* `largs` - Constructor arguments for the label.
* `wargs` - Constructor arguments for the widget.
* `lgrid` - grid() arguments for the label.
* `wgrid` - grid() arguments for the widget.

### create_text(parent, name, text, height=10, wrap="none", default="", largs={}, wargs={}, lgrid={}, wgrid={})

Add a text to the given parent.

_Parameters_:

* `parent` - A Tk frame.
* `name` - Name of the widget.
* `text` - Text for the label.
* `height` - Height in number of lines.
* `wrap` - Text wrap argument.
* `default` - Default value of the widget.
* `largs` - Constructor arguments for the label.
* `wargs` - Constructor arguments for the widget.
* `lgrid` - grid() arguments for the label.
* `wgrid` - grid() arguments for the widget.

### create_checkbox(parent, name, text, default=0, wargs={}, wgrid={})

Add a checkbox to the given parent.

_Parameters_:

* `parent` - A Tk frame.
* `name` - Name of the widget.
* `text` - Text for the label.
* `default` - Default value of the widget.
* `wargs` - Constructor arguments for the widget.
* `wgrid` - grid() arguments for the widget.

### create_button(parent, name, text, command, bargs={}, bgrid={})

Add a button to the given parent.

_Parameters_:

* `parent` - A Tk frame.
* `name` - Name of the widget.
* `text` - Text for the widget.
* `command` - Function to call when clicked.
* `bargs` - Constructor arguments for the button.
* `bgrid` - grid() arguments for the button.

### create_notebook(parent, name, nargs={})

Add a notebook to the given parent.

_Parameters_:

* `parent` - A Tk frame.
* `name` - Name of the widget.
* `nargs` - Constructor arguments for the notebook.

### notebook_tab_changed(event)

Tab changed event callback for the notebook.

_Parameters_:

* `event` - Tk event object.

### create_tab(parent, text)

Add a tab to the given notebook.

_Parameters_:

* `parent` - A notebook.
* `text` - Text to display on tab.

### create_progress()

Add a progress label to the root window.

### enable_widgets()

Enable all widgets.

### disable_widgets()

Disable all widgets.

### hide_widget(name)

Hide the given widget.

_Parameters_:

* `name` - Name of the widget to hide.

### show_widget(name)

Show the given widget.

_Parameters_:

* `name` - Name of the widget to hide.

### get_input(widget, initialdir, initialfile, filetypes)

Show the open file (singular) dialog.

_Parameters_:

* `widget` - Widget in which to save the user's selection.
* `initialdir` - Starting directory for the file dialog.
* `initialfile` - Starting filename for the file dialog.
* `filetypes` - List of allowed file types.

### get_inputs(widget, initialdir, initialfile, filetypes)

Show the open files (plural) dialog.

_Parameters_:

* `widget` - Widget in which to save the user's selection.
* `initialdir` - Starting directory for the file dialog.
* `initialfile` - Starting filename for the file dialog.
* `filetypes` - List of allowed file types.

### get_output(widget, initialdir, initialfile, filetypes)

Show the save file dialog.

_Parameters_:

* `widget` - Widget in which to save the user's selection.
* `initialdir` - Starting directory for the file dialog.
* `initialfile` - Starting filename for the file dialog.
* `filetypes` - List of allowed file types.

### get_folder(widget, initialdir, ignored1=None, ignored2=None)

Show the open folder dialog.

_Parameters_:

* `widget` - Widget in which to save the user's selection.
* `initialdir` - Starting directory for the file dialog.
* `ignored1` - Stub parameter just to be compatible with the other file dialog functions.
* `ignored2` - Stub parameter just to be compatible with the other file dialog functions.

### center(window)

Center the given window.

_Parameters_:

* `window` - TK frame.

### set_icon(window)

Set the icon for the given window.

_Parameters_:

* `window` - TK frame.

### start()

Start the GUI.

### set_progress(text, started=None, processed=None, total=None)

Set the progress text.

_Parameters_:

* `text` - Progress text.
* `started` - Unix timestamp of when the program started.
* `processed` - Counter of processed items.
* `total` - Total number of items to process.

### get_action(inputs)

Return the BaseAction subclass to use.

_Parameters_:

* `inputs` - User input dictionary.

### action()

Validate the user's input and perform the action.
