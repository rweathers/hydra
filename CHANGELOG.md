# Change Log

## 0.1.0-alpha (2017-10-08)

Initial release.

## 0.1.1-alpha (2017-12-24)

Removed localize_ functions, os.path.normpath should be used instead.

## 0.1.2-alpha (2017-12-24)

Added support for multiple usage commands, separated by \n.

## 0.1.3-alpha (2018-02-11)

Fixed CLI to pass all config values to actions.

Added program constants dictionary to BaseConfiguration.

## 0.2.0-alpha (2019-02-08)

Added BaseAction.execute.

Added BaseCLI.create_usage and deprecated program["usage"].

Added BaseGUI.create_icon and deprecated program["icon-*"].

## 0.3.0-alpha (2020-12-13)

Added support for top-level and nested menu commands.

Added support for a dictionary in GUI.menu.

Deprecated support for lists of tuples in GUI.menu.

## 0.4.0-beta (2021-03-07)

Removed deprecated features.

Made Action progress optional.

## 0.5.0-beta (2021-03-20)

Added double-click event to entires to open the specified path.

## 0.5.1-beta (2021-03-27)

Forced display of the 100% success message in the GUI version.

## 0.6.0-beta (2021-04-03)

Made BaseConfiguration subclass optional.

Made only one of BaseCLI or BaseGUI subclasses required.

Made the file/folder dialogs retain last used folder.

## 1.0.0rc1 (2021-10-03)

Added error checking for invalid return values from get_action.

Added error checking for duplicate widget names.

Renamed the package (not the module). If upgrading uninstall the existing package first.

## 1.0.0rc2 (2022-10-18)

Removed workaround for old Windows bug.

## 1.0.0 (2024-02-16)

No changes from RC2.

## 1.1.0 (2024-05-05)

Added user message and input callbacks to Action.
Added interface field to Action to identify if the program is running as a gui or cli.
