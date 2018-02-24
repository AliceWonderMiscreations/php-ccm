#This is an example spec file

%define pkgvendor psr
%define pkgname simplecache

%define pkgversion 1.0.0
# Increment below by one when tweaking the spec file but the version has not
#  changed and the security patch release has not changed
%define pkgtweakv 1

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
%define ccmaddpkg /usr/share/ccm/bin/addComposerPackage
%define ccmdelpkg /usr/share/ccm/bin/delComposerPackage

%if 0%{?_local_build}
Name:           php-ccm-%{pkgvendor}-%{pkgname}-local
%define branch local
%else
Name:           php-ccm-%{pkgvendor}-%{pkgname}
%define branch stable
%endif
%define pkginstalldir %{basedir}/%{branch}/libraries/%{pkgvendor}/%{pkgname}

Version:        %{pkgversion}
Release:        %{pkgsecurityv}.ccm.%{pkgtweakv}%{?pkgoptother}
BuildArch:      noarch
Summary:        Common interfaces for simple caching

Group:		php/interfaces
License:        MIT
URL:            https://www.php-fig.org/psr/psr-16/
#https://github.com/php-fig/simple-cache/releases
Source0:        simple-cache-%{version}.tar.gz

#checksums
Source20:       %{pkgvendor}-%{pkgname}-%{version}.sha256

Patch0:         simple-cache-1.0.0-add-closing-tags.patch

Requires: php-ccm-filesystem
Requires:       php(language) >= 5.3.0
Requires(post): %{_bindir}/php
Requires(post): %{ccmaddpkg}
Requires(postun): %{_bindir}/php
Requires(postun): %{ccmdelpkg}

Provides:       php-ccm(%{pkgvendor}/%{pkgname}) = %{pkgversion}
Provides:       php-ccm(psr/simple-cache) = %{pkgversion}

%description
This packages provides the PSR-16 Common Interface for Caching Libraries.

Caching is a common way to improve the performance of any project, making
caching libraries one of the most common features of many frameworks and
libraries. Interoperability at this level means libraries can drop their
own caching implementations and easily rely on the one given to them by the
framework, or another dedicated cache library.

PSR-6 solves this problem already, but in a rather formal and verbose way for
what the most simple use cases need. This simpler approach aims to build a
standardized streamlined interface for common cases. It is independent of
PSR-6 but has been designed to make compatibility with PSR-6 as straightforward
as possible.

%prep
( cd %_sourcedir; sha256sum -c %{SOURCE20} )

%setup -q -n simple-cache-%{version}
find . -type f -print |while read file; do
  chmod 644 ${file}
done

%build

%install
mkdir -p %{buildroot}%{pkginstalldir}
mv src/* %{buildroot}%{pkginstalldir}/

%post
%{ccmaddpkg} %{branch} %{pkgvendor} %{pkgname} %{pkgversion} %{pkgsecurityv} %{pkgtweakv} || :

%postun
if [ "$1" -eq 0 ]; then
    %{ccmdelpkg} %{branch} %{pkgvendor} %{pkgname} || :
fi

%files
%defattr(-,root,root,-)
%license LICENSE.md
%doc README.md LICENSE.md composer.json
%dir %{basedir}/%{branch}/libraries/%{pkgvendor}
%{pkginstalldir}



%changelog
* Sat Feb 24 2018 Alice Wonder <buildmaster@librelamp.com> - 1.0.0-0.ccm.1
- Initial spec file
