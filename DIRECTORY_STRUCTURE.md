Directory Structure
===================

With the exception of license files that will be packaged with the package
manager `%license` macro (or equivalent), all files in a package MUST be
installed within `/usr/share/ccm` and MUST be architecture independent.

Within the `/usr/share/ccm` directory will be the following top level
directories:

* `bin/`  
  Shell scripts needed to do things.  

* `doc/`
  Package documentation  

* `jsondb/`  
  JSON databases that may be needed (e.g. for security update alerts)

* `stable/`  
  Packages that are upstream release versions.

* `local/`  
  Specific versions of packages that may not be the latest version.

* `devel/`  
  Packages that are not part of a stable release

* `custom/`  
  For custom packages the system administrator wants that are not part of the
  CCM project, e.g. local classes used in local applications that benefit from
  the autoloading.

* `pear/`  
  For an optional PEAR package tree.

Packages __MUST NOT__ place files within the `custom/` or `pear/` and must only
put files within `local/` when a build macro is defined.

## Directory structure within `{local/|stable/|devel/|custom/}` branches

Withing those branches, there will be a `libraries/` and an `applications/`
directory. I am tempted to also add a `framework/` directory but that *may*
not actually be necessary.

The `libraries/` directory is for re-usable code that can loaded on demand by
any application, and the `applications/` directory is for applications.

## Directory structure within the `libraries/` directory

Within the `libraries/` directory, all first level child directories __MUST__
be named for the vendor that maintains the library and match the string used
for the vendor by Composer. They __MUST__ be lower case.

Within the specific vendor directories, each library will have its own
directory containing the actual PHP class files.

All classes __MUST__ use a namespace two levels deep that __SHOULD__ match the
Vendor/Product scheme specified in PSR-4.

A library __SHOULD NOT__ have its own autoloader.

## Directory structure within the `applications/` directory

A set policy for this is a little more lax since the CCM autoloader does not
need to know how to find stuff there, applications should have their own
autoload script that makes use of the CCM autoloader and takes care of loading
classes specific to the application.

There will be an `etc/` directory for application specific configuration files,
including configuration files that need to be copied elsewhere (e.g, for the
apache daemon).
