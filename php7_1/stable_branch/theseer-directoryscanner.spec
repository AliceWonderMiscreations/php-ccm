%define pkgvendor theseer
%define pkgname directoryscanner

%define pkgversion 1.3.2
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
Summary:	A recursive directory scanner and filter

Group:		php/libraries
License:	BSD-2-Clause
URL:		https://github.com/theseer/DirectoryScanner
Source0:	DirectoryScanner-%{version}.tar.gz

#checksums
Source20:	%{pkgvendor}-%{pkgname}-%{version}.sha256

#BuildRequires:	
Requires:	php(language) >= 5.3.1

Provides:	php-ccm(%{pkgvendor}/%{pkgname}) = %{pkgversion}

%description
This package needs an actual description written before release 1.ccm.1

%prep
( cd %_sourcedir; sha256sum -c %{SOURCE20} )

%setup -q -n DirectoryScanner-%{version}
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
%license LICENSE
%doc build.xml composer.json dist.php package.xml pear.sh phpcs.xml phpunit.xml.dist samples
%{pkginstalldir}



%changelog
* Tue Feb 13 2018 Alice Wonder <buildmaster@librelamp.com> - 1.2.3-0.ccm.0
- Initial spec file.
