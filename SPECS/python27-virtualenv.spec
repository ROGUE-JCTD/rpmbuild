%define name python27-virtualenv
%define version 13.1.0
%define release 1%{?dist}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Summary: Virtual Python Environment builder.
Name: %{name}
Version: %{version}
Release: %{release}
Source: virtualenv-%{version}.tar.gz
License: MIT
Group: Development/Libraries
Packager: Daniel Berry <dberry@boundlessgeo.com>
BuildRequires: python27 python27-setuptools
Requires: python27 python27-setuptools
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch

%description
A tool to create isolated Python environments.

%define _unpackaged_files_terminate_build 0

%prep

%setup -n virtualenv-%{version} -n virtualenv-%{version}

%build
   python2.7 setup.py build

%install
   python2.7 setup.py install --prefix=/usr/local --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
   rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Tue Dec 08 2015 BerryDaniel <dberry@boundlessgeo.com> [13.1.0-1]
- Updated to 13.1.0
