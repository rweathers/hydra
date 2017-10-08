# class BaseConfiguration

Base class for loading and validating configuration files.

## Attributes

* `filename` - Path to a configuration file.
* `conf` - Dictionary storing the option/value pairs. 

## Functions

### BaseConfiguration(filename)

Initialize the object.

_Paramaters_:

* `filename` - Path to a configuration file.

### load()

Load the configuration file into `self.conf`.

### validate()

Raise an exception if any configuration value are invalid.
