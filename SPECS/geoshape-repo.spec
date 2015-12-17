# Define Constants
%define name geoshape-repo
%define version 0.0.1
%define release 0.1beta%{?dist}
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name: %{name}
Version: %{version}
Release: %{release}
License: GPLv2
Summary: GeoSHAPE Repository Configuration Files
Packager: Daniel Berry <dberry@boundlessgeo.com>
Group: System Environment/Base
URL: http://geoshape.org/
Source0: GeoSHAPE.repo
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
This package installs the 'GeoSHAPE.repo'
repository files.

%prep
%setup -c -T

%build

%install
rm -rf %{buildroot}

# yum
install -Dpm 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/GeoSHAPE.repo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
