RPM Spec File Standard
======================

This standard is still in the process of being created. It will go through
changes as needed, initially by me, and then hopefully be reviewed by other
contributing packagers once I have something that actually works for the
packages in an initial demo release.

Everything here is also subject to change if and when the project gets some
other packagers who have issues with what is in this specification.

## php-ccm macro definitions

The following macros need to be defined in the RPM spec file, generally at the
top.

* `pkgvendor`  
The vendor of what is being packaged, e.g. `sabre`. This should _always_ be lower case.

* `pkgname`  
The name of what is being packaged, e.g. `xml`. This should _always_ be lower case.

* `pkgversion`  
The version of the package as it would be defined in a `composer.json` file

* `pkgtweakv`  
Base 10 number incremented when tweaks are made to the spec file

* `pkgsecurityv`  
Base 10 number incremented when a security patch is added to the spec file

* `basedir`  
Should always be set to `%{_datadir}/ccm`

* `_defaultdocdir`  
Should always be set to `%{basedir}/doc`

* `branch`  
This is set to the branch that the package is being built for, which will be
either `local` or `stable` or `devel`. Generally the branch is defined by
whether or not the `_local_build` build time macro is defined.

* `pkginstalldir`  
Should be defined to the a vendor/package directory within the `%{branch}` and
is a first level sub-directory of the either `libraries` or `applications`.

* `ccmaddpkg`  
Should be defined as `/usr/share/ccm/bin/addComposerPackage`

* `ccmdelpkg`  
Should be defined as `/usr/share/ccm/bin/delComposerPackage`

### The lower case thing

The `pkgvendor` and `pkgname` macros define directories on the file system.
There are three types of file systems:

1. Case Sensitive (and thus also case preserving) - Most modern UN\*X file
systems fit this type, but not all do.

2. Case Insensitive but Case Preserving - A few UN\*X file systems fit this
type, HFS+ that is sometimes used with Mac OS X is an example.

3. Case Insensitive. Not sure any modern UN\*X file systems use them but the
FAT32 file system historically used on Windows is an example.

To make things ‘just work’ the named of directories on UN\*X systems usually
are just simply always lower case. They do not have to be, but that is how it
has been done for years.

This is why I prefer the directory names for the vendor and package names to be
lower case.

Within the package directory itself, what the developer chose to do should be
preserved so the lower case UN\*X tradition is not enforced beyond that level.

## Naming of the Spec File Scheme

Generally RPM spec files should have the same name as the package they build.
However since each package will be named `php-ccm-vendor-package` I think it
is better to drop the `php-ccm-` from the beginning of the spec file especially
since the `ccm` part is likely to change to something longer in length.

RPM spec files are never installed as part of the package anyway, users do not
see them unless they have legitimate cause to need to edit them. The shorter
length makes it easier to deal with for those who are creating the packages.

## Spec File Name Tag

Two macros are defined at the beginning of the spec file: `pkgvendor` and
`pkgname`.

This should almost always be defined within the following `%if` block:

    %if 0%{?_local_build}
    Name: php-ccm-%{pkgvendor}-%{pkgname}-local
    %define branch local
    %else
    Name: php-ccm-%{pkgvendor}-%{pkgname}
    %define branch stable
    %endif
    %define pkginstalldir %{basedir}/%{branch}/libraries/%{pkgvendor}/%{pkgname}

In the cases where a package is being built for the development branch, then
the none local build should append `-devel` to the `Name` tag and the macro
defining the `pkginstalldir` should use `/devel` in place of `/stable`.

## Spec File Version Tag

Most of the time this should just be defined to the `%{pkgversion}` macro:

    Version: %{pkgversion}

I really *really* hope we can avoid versions that are not standard groups of
base 10 integers delimited by periods.

Unfortunately sometimes package creators will add a letter or the with `pre`
to the end of the version number. As a packager I effing hate it when they
do that.

In the case of a pre-release, the release tag should begin with a `0.` and at
the very end of the release tag, there should be a `git.CheckoutString` where
`CheckoutString` is the git checkout in the pre-release.

When a stable version is released and/or when a security patch is applied, then
the first number in the release tag would be incremented.

With respect release versions that have a letter as part of the version number
(e.g. openssl 1.0.1g) I *suspect* the best thing to do is leave it as part of
the version tag, but the scheme used by the developer would have to be looked
at.

This should be defined in the `%{pkgversion}` macro.

## Spec File Release Tag

I propose the following specification *always* be used for the Release tag:

1. __Security Patch Release__  
  This is defined in the `%{pkgsecurityv}` macro.

2. __Hard-coded dist tag__

3. __Tweak Version__  
  This is defined in the `%{pkgtweakv}` macro.

4. __Optional Other__

A dot will separate those portions, as is standard.

Using that standard, the spec file `Release` tag would be defined as such:

    Release: %{pkgsecurityv}.ccm.%{pkgtweakv}%{?pkgoptother}

As long as the `%{pkgsecurity}` or `%{pkgtweakv}` integers are always
incremented when an updated spec file with the same `Version` is built, the
`%{?pkgoptother}` macro is strictly informational and will not impact how RPM
determines if a package is the newer version.

### Security Patch Release

This will be a non-negative base 10 integer. When a security patch is applied
to a version of the package, this gets incremented by one.

For preview releases it will start at `0` and for official releases that did
not have a preview release it will start at `1`.

When a spec file switches from a preview release to an official release, it
will also be bumped up by one (e.g. from `0` to `1` if there were no needed
security updates to the preview release)

This should be defined in the `%{pkgsecurityv}` macro.

### Hard-coded dist tag

Right now this is `ccm` but when the official name of this project is chosen it
will change. The purpose of this, these packages are suppose to be distribution
and even operating system neutral. Distribution specific portions of the RPM
release tag should never be needed.

However, it should not be left out, it should be easy to determine where a
package installed on a system came from by looking at the release tag.

I really want to avoid situations where an installed package differs based upon
the version of PHP it is intended to be used with.

### Tweak Version

This should be a non-negative base 10 integer and should be incremented whenever
the spec file is tweaked for a new build. Whenever the Security Patch Release is
incremented, the Tweak Version should be reset to 0.

This should be defined in the `%{pkgtweakv}` macro.

### Optional Other

Usually this will not be used. Where it can be used is for things like the git
checkout revision or when a system administrator wants to customize a spec file
for his or her personal modifications.

The 'Optional Other' will ordinarily not make any difference when RPM compares
packages to see which is newer, so when changing to a different git checkout
revision, the `pkgtweakv` should be incrememted.

This should be defined in the `%{pkgoptother}` macro if defined at all.

#### Git Checkout Version

This is a very long string. Only the first seven characters should be used. The
first seven characters is what github ordinarily displays next to a release
download.

## Spec File Group Tag

This tag really is only useful when browsing available packages. The 'official'
groups are rather worthless, way to vague.

How to effectively group packages is something that needs to be thought about.

## Spec File License Tag

This should always match the contents of the `license` tag in the
`composer.json` file *and* should match what is installed in the package using
the `%license` macro.

## Spec File Buildarch Tag

This should _always_ be set to `noarch` - binary packages should not be
managed by this package repository.

## Spec File URL Tag

This should always match the `homepage` tag in the `composer.json` file.

## Spec File Summary Tag

In *most* cases this should match the contents of the `description` tag in the
`composer.json` file. The name of the package generally does not belong in that
tag, and sometimes what is in the `composer.json` file is too long for a
summery in an RPM spec file.

## Spec File Description Tag

Whenever the creator of the upstream package has gone through the trouble of
writing a proper description at the package homepage, that generally should be
used.

The description should wrap at 80 characters and generally should only use
ASCII characters.

Translations would be nice.

## Spec File Requires Tag

All packages should require the `php-ccm-filesystem` package:

    Requires: php-ccm-filesystem

When specifying the version of PHP required, using

    Requires: php(language) >= x.y

Generally that is the best way to do it on RHEL/Fedora systems. I *hope* that
the PHP packaging for other RPM based distributions use that provides syntax as
well but I do not know.

The spec file should require the scriptlets needed for the `%post` and
`%postun` maintenance of the JSON database:

    Requires(post): %{_bindir}/php
    Requires(post): %{ccmaddpkg}
    Requires(postun): %{_bindir}/php
    Requires(postun): %{ccmdelpkg}

Similar `Requires` syntax should be used for features of PHP that often require
a module to be installed. For example, the `sabre/xml` `composer.json` file
specifies that it needs:

    "require" : {
        "php" : ">=7.0",
        "ext-xmlwriter" : "*",
        "ext-xmlreader" : "*",
        "ext-dom" : "*",
        "lib-libxml" : ">=2.6.20",
        "sabre/uri" : ">=1.0,<3.0.0"
    },

To translate intp an RPM spec file:

    Requires: php(language) >= 7.0
    Requires: php(xmlwrites)
    Requires: php(xmlreader)
    Requires: php(dom)
    Requires: libxml2 >= 2.6.20
    Requires: php-ccm(sabre/uri) >= 1.0
    Requires: php-ccm(sabre/uri) < 3.0.0

Generally speaking, at least in the RHEL/Fedora world, when a `composer.json`
file specifies it requires `ext-whatever` the RPM for the appropriate extension
that provides that feature will specify `Provides: php(whatever)` so the RPM
spec file for the library can use `Requires: php(whatever)` and it will cause
the needed module to be installed, if necessary, by yum or DNF or whatever the
user is doing to pull in RPM dependencies.

I am a little less clear on what is meant by `"lib-libxml" : ">=2.6.20"` and
how to best handle that in the context of RPM.

I *believe* it means that `sabre/xml` uses features only available if the PHP
xml module was compiled against libxml2 >= 2.6.20. Composer can find that out
by looking at the `LIBXML_DOTTED_VERSION` but that information does not appear
to be available withing the RPM database of what the `php-xml` RPM package
provides.

Requiring `libxml2 >= 2.6.20` *probably* is the best we can do. Hopefully other
RPM based distributions use a compatible name or virtual provides for that
library.

For script library requirements like `sabre/uri` our RPM spec file should make
sure it is available within the `php-ccm` namespace, or out autoloader may not
be able to find it.

### PEAR Dependency Notes

The RPM spec file should not `Requires:` PEAR packages. Many system
administrators prefer to use the command line `pear` utility to manage PEAR
libraries on their system.

When packaging a library or application that depends upon PEAR packages, a file
called PEAR_REQUIREMENTS.txt should be created listing the required and
suggested PEAR dependencies, along with version notes, and be packaged with the
`%doc` macro. That will allow system administrators to install them.

The autoloader for PEAR packages will try to autoload PEAR modules that are
installed within the `phpinclude` path first, and when that fails, it will try
to find them in the following directories:

1. `/usr/share/ccm/pear`
2. `/usr/local/share/pear`
3. `/usr/share/pear`

In the future I hope to provide a utility that will allow a system
administrator to run a command that will install any needed PEAR modules inside
the `/usr/share/ccm/pear` directory for system administrators who would prefer
to keep PEAR modules needed for the CCM ecosystem inside the CCM ecosystem.

Such a utility would scan the `composer.json` files within the
`/usr/share/ccm/doc` directory to find what is needed and then offer to use the
system `/usr/bin/pear` utility to fetch what is needed and install them.

This project will not package PEAR modules.

## Spec File Provides Tag

Every spec file should have

    Provides: php-ccm(%{pkgvendor}/%{pkgname}) = %{pkgversion}

That way packages that depend upon it in the CCM ecosystem can pull it in, apps
that require specific versions can make sure the right version exists, etc.

Source File Management
======================

As far as packages in the CCM ecosystem are concerned, there are two kinds of
source files:

* Sources provided by an upstream provider
* Sources maintained in the CCM github project

For the first type, I am not fond of changing the name of the source as it was
distributed by the upstream vendor. However using the upstream vendor name can
result in collisions where different packages have source files that have the
same file name but are different.

For this reason, a `sha256sum` checksum file needs to created that contains
each of the first type of source (usually there will only be one file in it).

This is important because it allows the `rpmbuild` command to make sure it has
the correct source during the `%prep` section of the build process.

Whenever possible, a `.tar.{gz|bz2|xz}` version is preferable to a `.zip`
version of the source.

For the second type of source, the kind maintained in the php-ccm github
repository, the source files need to be named using the vendor followed by a
dash followed by the name of the project followed by a dash followed by the
version number where it was first used followed by a dash followed by the rest
of the filename.

These second type of source files do not need their name changed to reflect a
new version every time the version of the package is updated, that only needs
to happen when updating the source itself.

## The Checksum File

The checksum file should be specified as `Source20` in the RPM spec file,
unless your spec file needs more than 20 other source files, in which you are
probably doing something wrong.

Examples of what these files look like are in the `sha256sum` directory of the
php-ccm project github repository.

They are simply named `vendor-package-version.sha256` and are a standard
checksum file created with the `sha256sum` command-line utility.

## Patches

When patches are needed, the patch file should be maintained in the php-ccm
package repository and the patch filename should include the vendor, package
name, and version that it applies to, followed by a brief description of the
patch.

If the patch fixes a security issue that has a CVE database number, the CVE
number should be part of the patch file.

It will likely take some doing, but in the case of security fixes, they really
should be backported to every version of the package maintained withing the
php-ccm ecosystem.

Some users may have applications installed that require older versions of a
particular dependency that do not receive vendor updates anymore.

## The `%prep` section of the RPM spec file

This section of the RPM spec file is executed before the source is unpacked.
This is where the checksum file is checked, and that section of the spec file
will usually look like this:

    %prep
    ( cd %_sourcedir; sha256sum -c %{SOURCE20} )

In the event the checksum fails, the `rpmbuild` command will exit and the
package will not build, allowing the builder to fetch the proper source file.

## The `%setup` section of the RPM spec file

Usually with git managed source repositories this is not necessary, but it is
a good idea to make sure the permissions are always sane on the files:

    %setup -q -n %{pkgname}-%{version}
      find . -type f -print |while read file; do
      chmod 644 ${file}
    done

When a file needs different permissions, they can be asigned in the `%files`
section of the RPM spec file.

## The `%build` section of the RPM spec file

Generally there is nothing to do here.

## The `%install` section of the RPM spec file

The spec file will define the following macros:

    %define basedir %{_datadir}/ccm
    %define _defaultdocdir %{basedir}/doc
    
    %if 0%{?_local_build}
    Name: php-ccm-%{pkgvendor}-%{pkgname}-local
    %define branchbase %{basedir}/local/libraries
    %else
    Name: php-ccm-%{pkgvendor}-%{pkgname}
    %define branchbase %{basedir}/stable/libraries
    %endif
    %define pkginstalldir %{branchbase}/%{pkgvendor}/%{pkgname}

With the exception of documentation files and shell utilities, everything should
be installed within the defined `%{pkginstalldir}` macro.

The `ccm` will likely change to something else when I have decided upon a
better name, `ccm` is just the working name for developing this idea.

### The `lib` or `src` directory

The layout used by Composer, the top level of a package has the `README`,
`LICENSE`, etc. that we package separately. Within the top level, there usually
is a `tests` directory that has no place on a production server, and either a
`lib` or `src` directory that has the actual class files.

Those class files are what we are interested in packaging, and they should be
installed directly into the `pkginstalldir` directory so that the CCM
`\AliceWonderMiscreations\CCM\ClassLoader` class can easily find them without
needing to worry about the `composer.json` defined directory within the package
directory that actually has the classes we need.

The Autoloader is a lot simpler without needing to worry about whether the
class files are in `lib/` or `src/` or `whatever/`. I understand the need to do
it when there is also a `vendor/` directory with dependencies, but that is
exactly what this project was created to avoid.

### Developer Files

Developer files such as the `tests` directory should not be installed. Those
who have need of the development environment for a package should just use
Composer itself to get what they need.

## The `%post` section of the RPM spec file

It is important that the package be added to the JSON database:

    %post
    %{ccmaddpkg} %{branch} %{pkgvendor} %{pkgname} %{pkgversion} %{pkgsecurityv} %{pkgtweakv} || :
    
## The `%postun` section of the RPM spec file

It is important that the package be removed from the JSON database on package deletion:

    %postun
    if [ "$1" -eq 0 ]; then
        %{ccmdelpkg} %{branch} %{pkgvendor} %{pkgname} || :
    fi

Since RPM will run the `%postun` script on package update (the old version is
being removed) the `if then` clause makes sure it is only deleted from the JSON
database when it is not being replaced by a different version.

## The `%files` section of the RPM spec file

The first line of this section should be 

    %defattr(-,root,root,-)

The tells the `rpmbuild` command to use the same permissions as the files
themselves, but make them owned by the `root` user. As the vast majority of the
files will have `644` permissions, this means any injection vulnerabilities in
a web application must escalate privileges before they can overwrite anything
within the package.

The second line should define the package license using the `%license` macro,
e.g.

    %license LICENSE

The third line should package documentation using the `%doc` macro, e.g.

    %doc CHANGELOG.md README.md LICENSE composer.json

It _MUST_ also include the licende and the `composer.json` file.

The RPM package should own the vendor directory. This way when all packages
from a particular vendor have been removed, the vendor directory will also be
removed:

    %dir %{branchbase}/%{pkgvendor}

Finally the RPM package should own the package directory and everything that is
inside it:

    %{pkginstalldir}

## Subpackages

This will be covered when needed.


