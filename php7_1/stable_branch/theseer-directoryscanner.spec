%define pkgvendor theseer
%define pkgname directoryscanner

%define pkgversion 1.3.2
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
Name: php-ccm-%{pkgvendor}-%{pkgname}-local
%define branch local
%else
Name: php-ccm-%{pkgvendor}-%{pkgname}
%define branch stable
%endif
%define pkginstalldir %{basedir}/%{branch}/libraries/%{pkgvendor}/%{pkgname}

Version: %{pkgversion}
Release: %{pkgsecurityv}.ccm.%{pkgtweakv}%{?pkgoptother}
BuildArch: noarch
Summary: A recursive directory scanner and filter

Group: php/libraries
License: BSD-2-Clause
URL: https://github.com/theseer/DirectoryScanner
Source0: DirectoryScanner-%{version}.tar.gz

#checksums
Source20:	%{pkgvendor}-%{pkgname}-%{version}.sha256

Patch0: TheSeer-DirectoryScanner-1.3.2-autoload.patch

Requires: php-ccm-filesystem
Requires: php(language) >= 5.3.1
Requires(post): %{_bindir}/php
Requires(post): %{ccmaddpkg}
Requires(postun): %{_bindir}/php
Requires(postun): %{ccmdelpkg}

Provides: php-ccm(%{pkgvendor}/%{pkgname}) = %{pkgversion}

%description
This package needs an actual description written before release 1.ccm.1

%prep
( cd %_sourcedir; sha256sum -c %{SOURCE20} )

%setup -q -n DirectoryScanner-%{version}
%patch0 -p1
find . -type f -print |while read file; do
  chmod 644 ${file}
done

%build

%install
mkdir -p %{buildroot}%{pkginstalldir}
install -m644 src/directoryscanner.php     %{buildroot}%{pkginstalldir}/DirectoryScanner.php
install -m644 src/exception.php            %{buildroot}%{pkginstalldir}/Exception.php
install -m644 src/filesonlyfilter.php      %{buildroot}%{pkginstalldir}/FilesOnlyFilterIterator.php
install -m644 src/includeexcludefilter.php %{buildroot}%{pkginstalldir}/IncludeExcludeFilterIterator.php
install -m644 src/phpfilter.php            %{buildroot}%{pkginstalldir}/PHPFilterIterator.php

%post
%{ccmaddpkg} %{branch} %{pkgvendor} %{pkgname} %{pkgversion} %{pkgsecurityv} %{pkgtweakv} || :

%postun
if [ "$1" -eq 0 ]; then
    %{ccmdelpkg} %{branch} %{pkgvendor} %{pkgname} || :
fi

%files
%defattr(-,root,root,-)
%license LICENSE
%doc build.xml composer.json dist.php package.xml pear.sh phpcs.xml phpunit.xml.dist samples
%dir %{basedir}/%{branch}/libraries/%{pkgvendor}
%{pkginstalldir}



%changelog
* Fri Feb 23 2018 Alice Wonder <buildmaster@librelamp.com> - 1.3.2-0.ccm.1
- port to new spec file specification
- Add post/postun scriptlets
- Fix filename structure for our autoloader

* Tue Feb 13 2018 Alice Wonder <buildmaster@librelamp.com> - 1.3.2-0.ccm.0
- Initial spec file.
