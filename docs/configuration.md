# class BaseConfiguration

Base class for loading and validating configuration files.

## Attributes

* `filename` - Path to a configuration file.
* `prog` - Program constants dictionary.
* `conf` - Dictionary storing the option/value pairs. 

## Functions

### BaseConfiguration(prog)

Initialize the object.

_Parameters_:

* `prog` - Program constants dictionary.

### load()

Load the configuration file into `self.conf`.

### validate()

Raise an exception if any configuration value are invalid.
