# php-ccm
Composer Class Manager

This project is not ready for public consumption and when it is, the name will
change.

What this is about, there are several things about Composer that I do not like
from the perspective of a system administrator.

## The Problem I Am Trying To Solve

### The Trust Issue

When installing something via Composure, it brings in numerous packages from
many different sources. These packages are not authenticated against
cryptography signatures I have chosen to trust, and that scares me. I prefer
actual package management (like RPM) where I the packages must be signed by a
source I have specifically chosen to trust to package the the dependency.

### Dependency Maintenance Issue

When Package A depends upon Library B, Package A chooses what versions of
library B it wants to use. If Library B is not the latest, the developer of the
library may not be porting security fixes to the version that Package A has
specified in its dependencies.

This can result in vulnerabilities. With a package maintainer between the
developer and the end user, the package maintainer can backport security fixes
in cases where the developer did not.

### Code Quality Issue

I suspect that a large number if not the majority of frequently used libraries
that are in the Composer ecosystem have developers who try to practice safe
coding practices. However this certainly is not always the case, and when you
install software via composure that ends up pulling in 20+ other libraries,
there is a good chance some of them have poor quality code that will cause
problems.

With dedicated package maintainers, some of those poor quality coding problems
can be caught and fixed.

### Static Library Issue

In some Linux distributions (e.g. Fedora) packages that static link against
external libraries are very often forbidden from the distribution package
repository. There has to be a damn good reason for an exception to made.

The reason is security. If, say, mod\_ssl links againsy libssl.a instead of
libssl.so.\* and a security hole is found and patched in libssl, mod\_ssl will
still be vulnerable unless it is recompiled.

It is much better for mod\_ssl to dynamink link against libssl\.so.\* so that
once the globally installed library is patched, mod\_ssl is no longer
vulnerable.

Composer likes to put dependencies inside the project directory. That has the
same issues static linking has. If the dependencies are globally installed,
then one package update secures every web application that uses it.
