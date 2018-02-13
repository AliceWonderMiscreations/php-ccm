%define pkgvendor zetacomponents
%define pkgname base

%define pkgversion 1.9.1
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
Summary:	Base package for zetacomponents

Group:		php/libraries
License:	Apache-2.0
URL:		https://github.com/zetacomponents
Source0:	Base-%{version}.tar.gz

#checksums
# https://github.com/zetacomponents/Base/commit/489e20235989ddc97fdd793af31ac803972454f1
Source20:	%{pkgvendor}-%{pkgname}-%{version}.sha256

#BuildRequires:	
Requires:	php

Provides:	php-ccm(%{pkgvendor}/%{pkgname}) = %{version}

%description
description goes here


%prep
( cd %_sourcedir; sha256sum -c %{SOURCE20} )

%setup -q -n Base-%{version}
find . -type f -print |while read file; do
  chmod 644 ${file}
done

%build

%install
mkdir -p %{buildroot}%{pkginstalldir}
mv src %{buildroot}%{pkginstalldir}/
mv tests %{buildroot}%{pkginstalldir}/


%files
%defattr(-,root,root,-)
%license LICENSE.txt
%doc ChangeLog LICENSE.txt CREDITS DESCRIPTION design docs phpunit.xml.dist review-1.5.txt composer.json
%{pkginstalldir}



%changelog
* Sun Feb 11 2018 Alice Wonder <buildmaster@librelamp.com> - 1.9.1-0.ccm.0
- Initial spec file
