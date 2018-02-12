%define pkgvendor sabre
%define pkgname xml

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
Version:	2.1.0
Release:	0.ccm.0
BuildArch:	noarch
Summary:	An XML library that you may not hate

Group:		php/libraries
License:	BSD-3-Clause
URL:		http://sabre.io/xml/
Source0:	%{pkgname}-%{version}.tar.gz

#checksums
Source20:	%{pkgvendor}-%{pkgname}-%{version}.sha256

#BuildRequires:	
Requires:	php >= 7.0
Requires:	php-ccm(sabre/uri) >= 1.0
Requires:	php-ccm(sabre/uri) < 3.0.0
Requires:	php-xmlwriter
Requires:	php-xmlreader
Requires:	php-dom
Requires:	libxml2 >= 2.6.20

Provides:	php-ccm(%{pkgvendor}/%{pkgname}) = %{version}

%description
If you are writing or consuming API's in PHP, chances are that you need to work
with XML. In some cases you may even prefer it.

You may have started with SimpleXML and after a while switched to using the DOM
after realizing SimpleXML is really not that simple if you strictly use xml
namespaces everywhere.

For writing XML, you may have found that using the DOM requires far too much
code, or you may simply generate your XML by echoing strings, knowing that
it may not be the best idea.

sabre/xml hopes to solve your issues, by wrapping XMLReader and XMLWriter, and
providing standard design patterns around:

 * Quickly generating XML based on simple array structures,
 * Providing a super simple XML-to-object mapping,
 * Re-usability of parsers.



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
mkdir -p %{buildroot}%{pkginstalldir}/bin


%files
%defattr(-,root,root,-)
%license LICENSE
%doc CHANGELOG.md README.md LICENSE composer.json
%{pkginstalldir}



%changelog
* Sun Feb 11 2018 Alice Wonder <buildmaster@librelamp.com> - 2.1.0-0.ccm.0
- Initial spec file
