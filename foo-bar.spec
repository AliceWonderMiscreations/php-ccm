#This is an example spec file

%define pkgvendor foo
%define pkgname bar

%define pkgversion 1.2.3
# Increment below by one when tweaking the spec file but the version has not
#  changed and the security patch release has not changed
%define pkgtweakv 1

# Increment below by one when applying a security patch to the current version
#  or when switching from pre-release to official release of a version.
# Reset to 1 if updating the version (or 0 if updating to a pre-release of
#  a new version)
%define pkgsecurityv 1

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
Summary:	A sampl RPM spec file

Group:		php/libraries
License:	BSD-3-Clause
URL:		https://github.com/AliceWonderMiscreations/php-ccm
Source0:	%{pkgname}-%{version}.tar.gz

#checksums
Source20:	%{pkgvendor}-%{pkgname}-%{version}.sha256

#BuildRequires:	
Requires:	php(language) >= 7.1
Requires:	php-ccm(sabre/uri) >= 1.0
Requires:	php-ccm(sabre/uri) < 3.0.0
Requires:	php-ccm(zetacomponents/consoletools) >= 1.6
Requires:	php-ccm(zetacomponents/consoletooks) < 2.0
Requires:	php-dom

Provides:	php-ccm(%{pkgvendor}/%{pkgname}) = %{pkgversion}

%description
If you are writing an RPM spec file for a library that can be installed with
a composer.json file, this spec file may serve as a good template to start
from.

Be sure to read the RPM_SPEC.md file, which should explain why things in this
spec file are done the way that they are done.

The RPM_SPEC.md file should probably be considered authoritative.

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
* Sun Feb 13 2018 Alice Wonder <buildmaster@librelamp.com> - 1.2.3-1.ccm.1
- Initial spec file
