%define pkgvendor patchwork
%define pkgname jsqueeze

%define pkgversion 2.0.5
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
%define branchbase %{basedir}/local/libraries
%else
Name:		php-ccm-%{pkgvendor}-%{pkgname}
%define branchbase %{basedir}/stable/libraries
%endif
%define pkginstalldir %{branchbase}/%{pkgvendor}/%{pkgname}

Version:	%{pkgversion}
Release:	%{pkgsecurityv}.ccm.%{pkgtweakv}%{?pkgoptother}
BuildArch:	noarch
Summary:	Efficient JavaScript minification in PHP

Group:		php/libraries
License:	Apache-2.0 or GPL-2.0
URL:		https://github.com/tchwork/jsqueeze
Source0:	%{pkgname}-%{version}.tar.gz

#checksums
Source20:	%{pkgvendor}-%{pkgname}-%{version}.sha256

#BuildRequires:	
Requires:	php(language) >= 5.3.0

Provides:	php-ccm(%{pkgvendor}/%{pkgname}) = %{pkgversion}

%description
JSqueeze shrinks / compresses / minifies / mangles Javascript code.

It's a single PHP class that has been developed, maintained and thoroughly
tested since 2003 on major JavaScript frameworks (e.g. jQuery).

JSqueeze operates on any parse error free JavaScript code, even when semi-colons
are missing.

In term of compression ratio, it compares to YUI Compressor and UglifyJS.

%prep
( cd %_sourcedir; sha256sum -c %{SOURCE20} )

%setup -q -n %{pkgname}-%{version}
find . -type f -print |while read file; do
  chmod 644 ${file}
done

%build

%install
mkdir -p %{buildroot}%{pkginstalldir}
mv src/* %{buildroot}%{pkginstalldir}/


%files
%defattr(-,root,root,-)
%license LICENSE.ASL20 LICENSE.GPLv2
%doc README.md LICENSE.ASL20 LICENSE.GPLv2 composer.json
%dir %{branchbase}/%{pkgvendor}
%{pkginstalldir}



%changelog
* Sat Feb 17 2018 Alice Wonder <buildmaster@librelamp.com> - 1.2.3-1.ccm.1
- Initial spec file.
