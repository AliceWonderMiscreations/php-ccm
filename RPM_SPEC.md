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

* `pkginstalldir`  
Should be defined to the a vendor/package directory within the `%{basedir}`

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
    %define pkginstalldir %{basedir}/local/%{pkgvendor}/%{pkgname}
    %else
    Name: php-ccm-%{pkgvendor}-%{pkgname}
    %define pkginstalldir %{basedir}/stable/%{pkgvendor}/%{pkgname}
    %endif

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

1. _Security Patch Release_  
  This is defined in the `%{pkgsecurityv}` macro.

2. __Hard-coded dist tag__

3. __Tweak Version__  
  This is defined in the `%{pkgtweakv}` macro.

4. Optional Other

A dot will separate those portions, as is standard.

### Security Patch Release

This will be a base 10 integer. When a security patch is applied to a version
of the package, this gets bumped up by one.

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

### Tweak Version

This should be a base 10 integer and should be incremented whenever the spec
file is tweaked for a new build. Whenever the Security Patch Release is
incremented, the Tweak Version should be reset to 0.

This should be defined in the `%{pkgtweakv}` macro.

### Optional Other

Usually this will not be used. Where it can be used is for things like the git
checkout revision or when a system administrator wants to customize a spec file
for his or her personal modifications.

The 'Optional Other' will ordinarily not make any difference when RPM compares
packages to see which is newer, so when changing to a different git checkout
revision, the `pkgtweakv` should be incrememted.

This should be defined in the `%{pkgoptother}` macro.

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

When specifying the version of PHP required, using

    Requires: php(language) >= x.y

Generally is the best way to do it on RHEL/Fedora systems. I *hope* that the
PHP packaging for other RPM based distributions use that provides syntax as
well but I do not know.

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

## Spec File Requires Tag

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
    %define pkginstalldir %{basedir}/local/%{pkgvendor}/%{pkgname}
    %else
    Name: php-ccm-%{pkgvendor}-%{pkgname}
    %define pkginstalldir %{basedir}/stable/%{pkgvendor}/%{pkgname}
    %endif

With the exception of documentation files and shell utilities, everything should
be installed within the defined `%{pkginstalldir}` macro.

Okay I am seriously thinking about adding a `/Library` or `/Application` between
the `%{basedir}` and the `{/local|/stable|/devel}` part of the macro definition
but I have not done that yet. The idea being reusable code would go into
Library for the `phpinclude` path, and applications (like Roundcube) would go
into the Application directory so their stuff does not end up in the global
`phpinclude` path.

Anyway, the point is everything needs to be packaged *inside* the php-ccm
`%{basedir}` macro which is `%{_datadir}/ccm` (`/usr/share/ccm`)

The `ccm` will likely change to something else when I have decided upon a
better name, `ccm` is just the working name for developing this idea.

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

### Subpackages

Initially I am not creating any subpackages but in the future, things like the
`tests` sub-directories that are necessary to run the code should be split out
into subpackages.







Write more
