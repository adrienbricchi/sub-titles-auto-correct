# How to contribute

Hey, that's nice of you, thanks.


## Testing

  * Every tests are in `Tests/test_{package_name}_{tested_file_name}.py`, avoiding sub-folders to ease continuous integration.
  * Every method from the original file should be reported in tests, in the same order, and the same code regions.
  * Consider testing every setters and getters into a single test method, apply the same strategy with other trivial methods.
  * Aim for a 100% code coverage.

## Coding conventions

Using the [official python recommendations](https://www.python.org/dev/peps/pep-0008/), with a few tweaks and complements :

  * 120 characters lines. The punch cards' 80 char limit seems outdated since wide screens.
  * 2 blank lines after imports and between each function.
  * 35 lines max per function, to avoid scrolling. Split it in private/static methods if you're exceeding.
  * The more code in easily testable static methods, the better.

Code regions are encouraged, in the following order:
  * Constructor(s)
  * Setters / getters
  * Static methods
  * Private methods
  * Inherited methods (one region per parent class inheritance)
  * Inner classes

Thanks,
