# Define Constants
%define name geoshape
%define version 1.5.1
%define release 0.1.beta%{?dist}
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name:             %{name}
Version:          %{version}
Release:          %{release}
Summary:          Geospatial capabilities for Security, Humanitarian Assistance, Partner Engagement
Group:            Applications/Engineering
License:          GPLv2
Source1:          GeoNode-2.4.tar.gz
Source2:          supervisord.conf
Source3:          %{name}.init
Source4:          %{name}.conf
Source5:          proxy.conf
Source6:          local_settings.py
Source7:          robots.txt
Source8:          %{name}-config
Source9:          file-service.war
Source10:         geogig-cli-app-1.0.zip
Packager:         Daniel Berry <dberry@boundlessgeo.com>
Requires(pre):    /usr/sbin/useradd
Requires(pre):    /usr/bin/getent
Requires(pre):    bash
Requires(postun): /usr/sbin/userdel
Requires(postun): bash
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    make
BuildRequires:    expat-devel
BuildRequires:    db4-devel
BuildRequires:    gdbm-devel
BuildRequires:    sqlite-devel
BuildRequires:    readline-devel
BuildRequires:    zlib-devel
BuildRequires:    bzip2-devel
BuildRequires:    openssl-devel
BuildRequires:    tk-devel
BuildRequires:    gdal-devel = 1.11.2
BuildRequires:    libxslt-devel
BuildRequires:    libxml2-devel
BuildRequires:    libjpeg-turbo-devel
BuildRequires:    zlib-devel
BuildRequires:    libtiff-devel
BuildRequires:    freetype-devel
BuildRequires:    littlecms-devel
BuildRequires:    proj-devel
BuildRequires:    geos-devel
BuildRequires:    postgresql93-devel
BuildRequires:    unzip
BuildRequires:    git
Requires:         python27
Requires:         python27-virtualenv
Requires:         gdal = 1.11.2
Requires:         postgresql93
Requires:         postgresql93-server
Requires:         postgis21-postgresql93
Requires:         httpd
Requires:         libxslt
Requires:         libxml2
Requires:         libjpeg-turbo
Requires:         zlib
Requires:         libtiff
Requires:         freetype
Requires:         littlecms
Requires:         proj
Requires:         geos
Requires:         %{name}-geoserver >= 2.6
Requires:         rabbitmq-server >= 3.5.6
Requires:         erlang >= 18.1
AutoReqProv:      no
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GeoShape is designed to enable collaboration on geospatial information between mission partners in connected and disconnected operations. GeoSHAPE has been built utilizing open source software and open standards to make it available for partners and to maximize interoperability.

%prep

%build

%install
# rogue and geonode
GEONODE_LIB=$RPM_BUILD_ROOT%{_localstatedir}/lib/geonode
mkdir -p $GEONODE_LIB/uwsgi/{static,uploaded/thumbs}
pushd $GEONODE_LIB
git clone --depth 1 -b geoint https://github.com/boundlessgeo/rogue_geonode.git

# create virtualenv
virtualenv .
export PATH=/usr/pgsql-9.3/bin:$PATH
source bin/activate

# install rogue_geonode
pushd rogue_geonode
pip install .
popd && popd

# install geoshape_geonode from source
tar -xf %{SOURCE1} -C .
python GeoNode-2.4/setup.py install
rm -fr GeoNode-2.4

# install Python GDAL, uWSGI, Supervisor
pip install GDAL==1.11.2
pip install uwsgi==1.9.17.1
pip install supervisor==3.1.3

# setup supervisord configuration
SUPV_ETC=$RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $SUPV_ETC
install -m 644 %{SOURCE2} $SUPV_ETC/supervisord.conf
GEOSHAPE_LOG=$RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
mkdir -p $GEOSHAPE_LOG
CELERY_LOG=$RPM_BUILD_ROOT%{_localstatedir}/log/celery
mkdir -p $CELERY_LOG
# setup init script
INITD=$RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $INITD
install -m 751 %{SOURCE3} $INITD/%{name}

# setup httpd configuration
HTTPD_CONFD=$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $HTTPD_CONFD
install -m 644 %{SOURCE4} $HTTPD_CONFD/%{name}.conf
install -m 644 %{SOURCE5} $HTTPD_CONFD/proxy.conf

# adjust virtualenv to /var/lib/geonode path
VAR0=$RPM_BUILD_ROOT%{_localstatedir}/lib/geonode
VAR1=%{_localstatedir}/lib/geonode
find $VAR0 -type f -name '*pyc' -exec rm {} +
grep -rl $VAR0 $VAR0 | xargs sed -i 's|'$VAR0'|'$VAR1'|g'

# setup geoshape configuration directory
GEOSHAPE_CONF=$RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $GEOSHAPE_CONF
# local_settings.py
install -m 775 %{SOURCE6} $GEOSHAPE_CONF/local_settings.py

# additions to geoshape directory
# robots.txt
install -m 755 %{SOURCE7} $GEONODE_LIB/rogue_geonode/%{name}/templates/robots.txt
# add robots.txt as a TemplateView in django original file is urls.py.bak
sed -i.bak "s|urlpatterns = patterns('',|urlpatterns = patterns('',\\n\
url(r'^/robots\\\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),|" $RPM_BUILD_ROOT%{_localstatedir}/lib/geonode/rogue_geonode/%{name}/urls.py

# geoshape-config command
LOCAL_BIN=$RPM_BUILD_ROOT%{_prefix}/local/bin
mkdir -p $LOCAL_BIN
install -m 755 %{SOURCE8} $LOCAL_BIN/

# file-service.war
WEBAPPS=$RPM_BUILD_ROOT%{_localstatedir}/lib/tomcat/webapps
mkdir -p $WEBAPPS
install -m 755 %{SOURCE9} $WEBAPPS/

# geogig-cli
unzip -d RPM_BUILD_ROOT%{_localstatedir}/lib %{SOURCE10}
PROFILE_D=$RPM_BUILD_ROOT%{_sysconfdir}/profile.d
echo  "export GEOGIG_HOME=/var/lib/geogig && PATH=$PATH:$GEOGIG_HOME/bin" > $PROFILE_D/geogig.sh

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -d %{_localstatedir}/lib/geonode/rogue_geonode -g %{name} -s /bin/bash -c "GeoSHAPE Daemon User" %{name}

%post
if [ $1 -eq 1 ] ; then
  ln -s %{_sysconfdir}/%{name}/local_settings.py %{_localstatedir}/lib/geonode/rogue_geonode/%{name}/local_settings.py
fi

%preun
if [ $1 -eq 0 ] ; then
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/service httpd stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
  rm -fr %{_localstatedir}/lib/geonode
  rm -fr %{_sysconfdir}/%{name}
  rm -f %{_sysconfdir}/init.d/%{name}
  rm -f %{_sysconfdir}/supervisord.conf
  rm -f %{_sysconfdir}/httpd/conf.d/%{name}.conf
  rm -f %{_sysconfdir}/httpd/conf.d/proxy.conf
fi

%postun

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(755,%{name},%{name},755)
%{_localstatedir}/lib/geogig
%{_sysconfdir}/$PROFILE_D/geogig.sh
%{_localstatedir}/lib/geonode
%config(noreplace) %{_sysconfdir}/%{name}/local_settings.py
%defattr(775,%{name},%{name},775)
%dir %{_localstatedir}/lib/geonode/uwsgi/static
%dir %{_localstatedir}/lib/geonode/uwsgi/uploaded
%defattr(744,%{name},%{name},744)
%dir %{_localstatedir}/log/celery
%dir %{_localstatedir}/log/%{name}
%defattr(644,%{name},%{name},644)
%dir %{_sysconfdir}/%{name}/
%defattr(644,apache,apache,644)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/proxy.conf
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/supervisord.conf
%defattr(-,root,root,-)
%config %{_sysconfdir}/init.d/%{name}
%{_prefix}/local/bin/%{name}-config
%attr(-,tomcat,tomcat) %{_localstatedir}/lib/tomcat/webapps/file-service.war
%doc ../SOURCES/license/GNU

%changelog
* Tue Dec 08 2015 BerryDaniel <dberry@boundlessgeo.com> [1.5.1-1]
- Updated geoshape.init to run all apps in supervisor.conf under the geoshape group
- Added five celery workers to supervisor.conf
- Added geogig-cli
- Added rabbitmq-server >= 3.5.6 and erlang >= 18.1 as dependencies

* Tue Dec 08 2015 BerryDaniel <dberry@boundlessgeo.com> [1.5-1]
- Updated geoshape-geonode to GeoNode==2.4
