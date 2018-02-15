BROKEN PACKAGES
===============

List of packages installable by composer that would be a major undertaking to
package here.

## Zetacomponents/Base

The problem:

* None of the classes are namespaced

* Adding namespace declarations would break it, its `ezcBase` class (defined
in `base.php`) basically has its own autoloader for loading the class files
that are used elsewhere within zetacomponents.

* It has not been updated in six years. It is abandonware and that poses
potential security issues. In fairness, there have been occassional tweaks, to
things like fix PHP 7.x issues (the code was written for PHP 5) but it has
basically been dead development wise.

It is my recommendation that libraries and applications that use it be patched
to not use it unless it gets a major update and starts using a namespace.
