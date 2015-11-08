# Define Constants
%define name geoshape
%define version 1.5
%define release 0.1.beta%{?dist}
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}

Name:             %{name}
Version:          %{version}
Release:          %{release}
Summary:          Geospatial capabilities for Security, Humanitarian Assistance, Partner Engagement
Group:            Applications/Engineering
License:          GPLv2
Source0:          geoshape
Source1:          geoshape.requirements.txt
Source2:          geoshape.supervisord.conf
Source3:          geoshape.init
Source4:          geoshape.mapstory.conf
Source5:          geoshape.proxy.conf
Source6:          geoshape.README
Source7:          geoshape.local_settings.py
Source8:          geoshape.robots.txt
Packager:         Daniel Berry <dberry@boundlessgeo.com>
Requires(pre):    /usr/sbin/useradd
Requires(pre):    /usr/bin/getent
Requires(pre):    bash
Requires(postun): /usr/sbin/userdel
Requires(postun): bash
BuildRequires:    python27
BuildRequires:    python27-virtualenv
BuildRequires:    gdal-devel = 1.11.2
BuildRequires:    proj-devel
BuildRequires:    postgresql93-devel
BuildRequires:    libxslt-devel
BuildRequires:    pcre-devel
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    git
Requires:         python27
Requires:         python27-virtualenv
Requires:         gdal = 1.11.2
Requires:         postgresql93
Requires:         postgresql93-server
Requires:         postgis21-postgresql93
Requires:         proj
Requires:         httpd
Requires:         libxslt
Requires:         %{name}-geoserver >= %{version}-%{release}
AutoReqProv:      no
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GeoShape is designed to enable collaboration on geospatial information between mission partners in connected and disconnected operations. GeoSHAPE has been built utilizing open source software and open standards to make it available for partners and to maximize interoperability. 

%package geoserver
Summary:       A version of GeoServer that is enhanced and designed for use with GeoShape %{version}.
Group:         Development/Libraries
BuildRequires: unzip
Requires:      %{name} = %{version}-%{release}
Requires:      tomcat
Requires:      java-1.7.0-openjdk
Conflicts:     geoserver
Patch0:        mapstory.web.xml.patch
Patch1:        mapstory.context.xml.patch
BuildArch:     noarch

%description geoserver
GeoServer is built with the geoserver-geonode-ext, which extends GeoServer
with certain JSON, REST, and security capabilites specifically for GeoShape %{version}-%{release}.

%prep
unzip $RPM_SOURCE_DIR/geoserver.war -d $RPM_SOURCE_DIR/geoserver
pushd $RPM_SOURCE_DIR/geoserver

%patch0 -p1
%patch1 -p1

popd

%build

%install

%pre

%post

%preun

%postun

%clean 
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files

%changelog
* Sun Nov 8 2015 Daniel Berry <dberry@boundlessgeo.com> 1.5-0.1.beta
- add comments
