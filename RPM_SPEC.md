RPM Spec File Standard
======================

This standard is still in the process of being created. It will go through
changes as needed, initially by me, and then hopefully be reviewed by other
contributing packagers once I have something that actually works for the
packages in an initial demo release.

Everything here is also subject to change if and when the project gets some
other packagers who have issues with what is in this specification.

## Naming of the Spec File Scheme

Generally RPM spec files should have the same name as the package they build.
However since each package will be named `php-ccm-vendor-package` I think it
is better to drop the `php-ccm-` from the beginning of the spec file especially
since the `ccm` part is likely to change to something longer in length.

RPM spec files are never installed as part of the package anyway, users do not
see them unless they have legitimate cause to need to edit them. The shorter
length makes it easier to deal with for those who are creating the packages.

## Spec File Name Scheme

Two macros are defined at the beginning of the spec file: `pkgvendor` and
`pkgname`.

These should be set to correspong to how Composer references the package
(as `pkgvendor`/`pkgname`) and should be lower case.

## Spec File Version Scheme

I really *really* hope we can avoid versions that are not standard groups of
base 10 integers delimited by periods.

Unfortunately sometimes package creators will add a letter or the worf `pre`
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

1. Security Patch Release
2. Hard-coded dist tag
3. Tweak Version
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

## TODO

Write more
