%define pkgvendor sabre
%define pkgname uri

%define pkgversion 2.1.0
# Increment below by one when tweaking the spec file but the version has not
#  changed and the security patch release has not changed
%define pkgtweakv 0

# Increment below by one when applying a security patch to the current version
#  or when switching from pre-release to official release of a version.
# Reset to 1 if updating the version (or 0 if updating to a pre-release of
#  a new version)
%define pkgsecurityv 0

# When there is a need for additional information in the release tag, uncomment
#  below to define it. The definition of this macro should always start with a
#  dot.
#  %%define pkgoptother .whatever

# Do not change these
%define basedir %{_datadir}/ccm
%define _defaultdocdir %{basedir}/doc

%if 0%{?_local_build}
Name:		php-ccm-%{pkgvendor}-%{pkgname}-local
%define pkginstalldir %{basedir}/local/%{pkgvendor}/%{pkgname}
%else
Name:		php-ccm-%{pkgvendor}-%{pkgname}
%define pkginstalldir %{basedir}/stable/%{pkgvendor}/%{pkgname}
%endif
Version:	%{pkgversion}
Release:	%{pkgsecurityv}.ccm.%{pkgtweakv}%{?pkgoptother}
BuildArch:	noarch
Summary:	Functions for making sense out of URIs

Group:		php/libraries
License:	BSD-3-Clause
URL:		http://sabre.io/uri/
Source0:	%{pkgname}-%{version}.tar.gz

#checksums
Source20:	%{pkgvendor}-%{pkgname}-%{version}.sha256

#BuildRequires:	
Requires:	php >= 7.0

Provides:	php-ccm(%{pkgvendor}/%{pkgname}) = %{version}

%description
sabre/uri is a lightweight library that provides several functions for working
with URIs, staying true to the rules of RFC3986.

Partially inspired by Node.js URL library, and created to solve real problems in
PHP applications. 100\% unit-tested and many tests are based on examples from
RFC3986.

The library provides the following functions:

 * resolve to resolve relative urls.
 * normalize to aid in comparing urls.
 * parse, which works like PHP's parse_url.
 * build to do the exact opposite of parse.
 * split to easily get the 'dirname' and 'basename' of a URL without all the
   problems those two functions have.



%prep
( cd %_sourcedir; sha256sum -c %{SOURCE20} )

%setup -q -n %{pkgname}-%{version}
find . -type f -print |while read file; do
  chmod 644 ${file}
done

%build

%install
mkdir -p %{buildroot}%{pkginstalldir}
mv lib %{buildroot}%{pkginstalldir}/
mv tests %{buildroot}%{pkginstalldir}/


%files
%defattr(-,root,root,-)
%license LICENSE
%doc CHANGELOG.md README.md LICENSE composer.json
%{pkginstalldir}



%changelog
* Sun Feb 11 2018 Alice Wonder <buildmaster@librelamp.com> - 2.1.0-0.ccm.0
- Initial spec file
