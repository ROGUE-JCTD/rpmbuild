# Define Constants
%define name geoshape-geoserver
%define realname geoserver
%define geoshape_ver 1.7.11
%define version 2.6
%define release 3%{?dist}
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name:          %{name}
Version:       %{version}
Release:       %{release}
Summary:       A version of GeoServer that is enhanced and designed for use with GeoSHAPE %{geoshape_ver}.
Group:         Development/Libraries
License:       GPLv2
BuildRequires: unzip
Requires:      %{name} = %{version}-%{release}
Requires:      tomcat
Conflicts:     geoserver
Source0:       geoserver.war
Source1:       geoserver_data-geogig_od3.zip
Source2:       geogig.config
Patch0:        web.xml.patch
Patch1:        context.xml.patch
BuildArch:     noarch

%description
GeoServer is built with the geoserver-geonode-ext, which extends GeoServer
with certain JSON, REST, and security capabilites specifically for GeoSHAPE.

%prep
[ -d $RPM_SOURCE_DIR/geoserver ] && rm -rf $RPM_SOURCE_DIR/geoserver
[ -d $RPM_SOURCE_DIR/data ] && rm -rf $RPM_SOURCE_DIR/data
unzip $RPM_SOURCE_DIR/geoserver.war -d $RPM_SOURCE_DIR/geoserver
unzip $RPM_SOURCE_DIR/geoserver_data-geogig_od3.zip -d $RPM_SOURCE_DIR/data
pushd $RPM_SOURCE_DIR/geoserver

%patch0 -p1
%patch1 -p1

popd

%build

%install
WEBAPPS=$RPM_BUILD_ROOT%{_localstatedir}/lib/tomcat/webapps
GS=$RPM_SOURCE_DIR/geoserver
DATA=$RPM_BUILD_ROOT%{_localstatedir}/lib/geoserver_data
GEOSHAPE_DATA=$RPM_SOURCE_DIR/data
mkdir -p $WEBAPPS
cp -rp $GS $WEBAPPS
if [ ! -d $DATA ]; then
  mkdir -p $DATA
  cp -R $GEOSHAPE_DATA/* $DATA
fi
sed -i.bak "s|http://localhost|https://localhost|g" $DATA/security/auth/geonodeAuthProvider/config.xml
install -m 644 %{SOURCE2} $DATA/geogig/.geogigconfig

%pre

%post
if [ $1 -eq 1 ] ; then
  # add Java specific options
  echo '# Next line added for geonode service' >> %{_sysconfdir}/tomcat/tomcat.conf
  echo 'JAVA_OPTS="-Xmx1024m -XX:MaxPermSize=256m -Duser.home=/var/lib/geoserver_data/geogig"' >> %{_sysconfdir}/tomcat/tomcat.conf
fi

%preun
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat stop > /dev/null 2>&1
  rm -fr %{_localstatedir}/lib/tomcat/webapps/geoserver
fi

%postun
if [ $1 -eq 1 ] ; then
  /sbin/service tomcat condrestart >/dev/null 2>&1
fi

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}
[ -d $RPM_SOURCE_DIR/geoserver ] && rm -rf $RPM_SOURCE_DIR/geoserver
[ -d $RPM_SOURCE_DIR/data ] && rm -rf $RPM_SOURCE_DIR/data

%files
%defattr(-,root,root,-)
%attr(-,tomcat,tomcat) %{_localstatedir}/lib/tomcat/webapps/geoserver
%attr(775,tomcat,tomcat) %{_localstatedir}/lib/geoserver_data
%attr(755,tomcat,tomcat) %{_localstatedir}/lib/geoserver_data/file-service-store

%changelog
* Mon Jan 04 2016 BerryDaniel <dberry@boundlessgeo.com> [2.6-3]
- fixed typo in replacing http with https

* Tue Dec 08 2015 BerryDaniel <dberry@boundlessgeo.com> [2.6-2]
- Add https to config.xml for geonode

* Tue Dec 08 2015 BerryDaniel <dberry@boundlessgeo.com> [2.6-1]
- Updated to 2.6
