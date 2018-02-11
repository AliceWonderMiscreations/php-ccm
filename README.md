# php-ccm
Composer Class Manager

This project is not ready for public consumption and when it is, the name will
change.

What this is about, there are several things about Composer that I do not like
from the perspective of a system administrator.

## The Trust Issue

When installing something via Composure, it brings in numerous packages from
many different sources. These packages are not authenticated against
cryptography signatures I have chosen to trust, and that scares me. I prefer
actual package management (like RPM) where I the packages must be signed by a
source I have specifically chosen to trust to package the the dependency.

## Dependency Maintenance Issue

When Package A depends upon Library B, Package A chooses what versions of
library B it wants to use. If Library B is not the latest, the developer of the
library may not be porting security fixes to the version that Package A has
specified in its dependencies.

This can result in vulnerabilities. With a package maintainer between the
developer and the end user, the package maintainer can backport security fixes
in cases where the developer did not.

## Code Quality Issue

I suspect that a large number if not the majority of frequently used libraries
that are in the Composer ecosystem have developers who try to practice safe
coding practices. However this certainly is not always the case, and when you
install software via composure that ends up pulling in 20+ other libraries,
there is a good chance some of them have poor quality code that will cause
problems.

With dedicated package maintainers, some of those poor quality coding problems
can be caught and fixed.
