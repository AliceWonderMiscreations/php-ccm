Composer Class Manager (CCM)
============================

This project is not ready for public consumption.

What this is about, there are several things about Composer that I do not like
from the perspective of a system administrator.

The Problems I Am Trying To Solve
---------------------------------

### The Trust Issue

When installing something via Composer, it brings in numerous packages from
many different sources. These packages are not authenticated against
cryptography signatures I have chosen to trust, and that scares me. I prefer
actual package management (like RPM) where the packages must be signed by a
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
install software via Composer that ends up pulling in 20+ other libraries,
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

The Fedora / EPEL Solution
--------------------------

Fedora / EPEL already implements a solution to this problem, with packages
maintained largely by the legendary Remi Collet.

They package Composer packages as globally installed RPM packages. Since I use
CentOS with the EPEL package repository, I should just be able to use those
packages, right?

Wrong. The issue is CentOS ships with PHP 5.6.x and I have upgraded my PHP to
PHP 7.1.x. As a result not all of the versions packaged in EPEL will work for
me.

I'm also not using the software collections to get a newer LAMP stack, I am
building my LAMP stack against LibreSSL. Thus if they package any of the
Composer packages for the Software Collections, I do not have access to them.

So the existing Fedora / EPEL solution is not right for me, and I imagine it is
not right for some others too.

Also my packaging solution is a slightly different philosophy from that of Remi
Collet. Not better, just different.

The CCM Solution to the Problem
-------------------------------

What I want to create is a solution for UN\*X operating systems with arch
independent libraries within a specific structure of /usr/share on the
filesystem.

I do not know if that is the appropriate place on MacOs / OS X or not, nor what
package manager would be used on that platform to manage them, but that
platform is generally a *development* platform rather than a *production*
platform, developers can just use Composer itself and I suspect most of them
will continue to do so.

What I want is the ability to `rsync` the install directory from one platform
to a completely different platform and have it "just work" as long as the
version of PHP is the same. I am not saying that is a good idea, just that
that is why I want to be capable of doing.

It may actually be a good to not run this project on the production system but
simply `rsync` from a test platform to the development when things work as they
are intended, but that is a choice for the system administrator to make.

There are generally three different major versions of PHP supported by the PHP
developers at any given time. At present, there are actually four as the PHP
5.6 branch has been given a little extra life, though I think it is actually
only getting security fixes and not bug fixes.

I want to support packages for all PHP supported versions, in different trees,
as sometimes the library version of dependency packages is restricted to
specific versions of PHP.

Since RHEL/CentOS is a very common server platform, it should be a goal to
support the version of PHP that ships with the most recent version of RHEL even
if that version is not technically supported by upstream PHP.

Right now I am only concerned about PHP 7.1 as that is the version of PHP
currently being used in the [LibreLAMP](https://librelamp.com/) project I both
maintain and use.

The package tree for CCM will be within something /usr/share/ccm and other than
license files, all files will be installed into that directory, no files will
be installed outside that directory. That is to avoid package conflicts with any
packages installed by the operating system vendor packages and to allow rsync
from a test server to the production server.

Within the package tree, there will be four different available branches:

* local
* stable
* devel
* custom

The purpose of the `stable` branch is to contain the most recent *released*
version of a library with Composer install that works in the specified version
of PHP.

The purpose of the `local` branch is to contain older versions of a package that
may be needed by a particular application or library.

The purpose of the `devel` branch is to contain development versions that are
not yet released as final packages.

The purpose of the `custom` branch is to allow installation of class libraries
and applications that are not generally released to the public through
Composer.

Web applications can then specify what order they want the autoloader to search
through the branches to find the class that is needed.

The CCM package repository itself will only include packages for the stable
branch but the git will include RPM spec files for the development branch and
will continue to maintain specific versions of spec files that are older than
what is in the stable branch for a specific version of a dependence as well as
matching source RPMs for the older version.

So if vendor foo has stable version of package bar at version 2.4.7 but the web
application imaginemail needs version 2.2.x, to install version 2.2.x the
system administrator can run:

    rpmbuild -D '_local_build 1' --rebuild php-ccm-foo-bar-2.2.7-3.ccm.17.src.rpm

The result will be: `php-ccm-foo-bar-local-2.2.7-3.ccm.17.noarch.rpm`

The system administrator can install that and the files will go in the local
branch, it will not conflict with a new version in the stable branch. Then as
long as imaginemail is configured to search the local branch for classes
*before* the stable branch, it will work.

The search order can be configured on a per-web application basis without
needing to change the `phpinclude` path.

### Security Patch Notification

Especially since the local and devel branches will not be part of the package
repositories, there needs to be a mechanism by which the system administrator
is notified that there is a security update for a version of a package they
have installed.

There should be a local database within the tree, jsonld is *probably* good
enough, that for each package installed contains branch, vendor, package,
version, and security realease. This can be updated by the pre/post scriptlets
in the RPM spec files.

A cron script installed in `/etc/cron.daily` will once a day check for newer
versions within the stable branch and newer securuty releases for each version
within all three brances.

This will obviously require some server infrastructure for the script run by
cron to check against.

## Non RPM-based Operating Systems

Right now I am only creating RPM spec files. There should however also be a
repository for Debian packages.

A package manager independent of the operating system may not be a bad idea,
it would be sweet if there was an independent package manager that is not RPM
but can install/update/remove noarch RPM packages. Maybe something could be
written in Python that does that???

