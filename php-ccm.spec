# Spec file for the CCM root

%define basedir %{_datadir}/ccm
%define _defaultdocdir %{basedir}/doc

Name:		php-ccm
Version:	0.0.0
Release:	0.ccm.0
BuildArch:	noarch
Summary:	Directory structure and tools for PHP class libraries

Group:		foo/bar
License:	MIT
URL:		https://github.com/AliceWonderMiscreations/php-ccm
Source0:	php-ccm-master.zip

#BuildRequires:	
Requires:	php(language) >= 5.3.0

%description
This is an experimental package repository for PHP libraries.
Incomplete at this point in time.


%prep
%setup -q -n php-ccm-master


%build


%install
mkdir -p %{buildroot}%{basedir}
mkdir -p %{buildroot}%{basedir}/{bin,doc,jsondb,pear}
mkdir -p %{buildroot}%{basedir}/custom
mkdir -p %{buildroot}%{basedir}/local/{libraries,applications}
mkdir -p %{buildroot}%{basedir}/stable/{libraries,applications}
mkdir -p %{buildroot}%{basedir}/devel/{libraries,applications}
install -m644 ClassLoader.php %{buildroot}%{basedir}


%files
%license LICENSE.md
%doc LICENSE.md AUTOLOADER.md DIRECTORY_STRUCTURE.md LOGO.jpg LOGO.jpg.txt README.md RPM_SPEC.md
%{basedir}




%changelog

