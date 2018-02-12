%define pkgvendor zetacomponents
%define pkgname consoletools

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
Version:	1.7
Release:	0.ccm.0
BuildArch:	noarch
Summary:	Classes for the console

Group:		php/libraries
License:	Apache-2.0
URL:		https://github.com/zetacomponents
Source0:	ConsoleTools-%{version}.tar.gz

#checksums
# https://github.com/zetacomponents/ConsoleTools/commit/30d67e9d04f458ac8cae4c49e50f81061460ff2c
Source20:	%{pkgvendor}-%{pkgname}-%{version}.sha256

#BuildRequires:	
Requires:	php
Requires:	php-ccm(zetacomponents/base) >= 1.8
Requires:	php-ccm(zetacomponents/base) < 2.0

Provides:	php-ccm(%{pkgvendor}/%{pkgname}) = %{version}

%description
A set of classes to do different actions with the console (also called shell).
It can render a progress bar, tables and a status bar and contains a class for
parsing command line options.


%prep
( cd %_sourcedir; sha256sum -c %{SOURCE20} )

%setup -q -n ConsoleTools-%{version}
find . -type f -print |while read file; do
  chmod 644 ${file}
done
mv NOTICE LICENSE

%build

%install
mkdir -p %{buildroot}%{pkginstalldir}
mv src %{buildroot}%{pkginstalldir}/
mv tests %{buildroot}%{pkginstalldir}/


%files
%defattr(-,root,root,-)
%license LICENSE
%doc ChangeLog LICENSE CREDITS DESCRIPTION design docs phpunit.xml.dist review-1.4.txt review-1.6.txt review.txt TODO composer.json
%{pkginstalldir}



%changelog
* Sun Feb 11 2018 Alice Wonder <buildmaster@librelamp.com> - 1.7-0.ccm.0
- Initial spec file
