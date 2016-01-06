# Define Constants
%define name geoshape
%define version 1.7.11
%define release 2%{?dist}
%define geonode_clone_version 1.4
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name:             %{name}
Version:          %{version}
Release:          %{release}
Summary:          Geospatial capabilities for Security, Humanitarian Assistance, Partner Engagement
Group:            Applications/Engineering
License:          GPLv2
Source0:          %{name}-%{version}.tar.gz
Source1:          pkgs.zip
Source2:          requirements.txt
Source3:          %{name}-geonode-%{geonode_clone_version}.tar.gz
Source4:          supervisord.conf
Source5:          %{name}.init
Source6:          %{name}.conf
Source7:          proxy.conf
Source8:          local_settings.py
Source9:          robots.txt
Source10:         %{name}-config
Source11:         geogig-cli-app-1.0.zip
Source12:         admin.json
Source13:         manage.py
Source14:         %{name}-config.conf
Packager:         Daniel Berry <dberry@boundlessgeo.com>
Requires(pre):    /usr/sbin/useradd
Requires(pre):    /usr/bin/getent
Requires(pre):    bash
Requires(postun): /usr/sbin/userdel
Requires(postun): bash
BuildRequires:    python27-devel
BuildRequires:    python27-virtualenv
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
Requires:         mod_ssl
Requires:         mod_xsendfile
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
Requires:         elasticsearch >= 1.6.0
AutoReqProv:      no

%description
GeoShape is designed to enable collaboration on geospatial information between mission partners in connected and disconnected operations. GeoSHAPE has been built utilizing open source software and open standards to make it available for partners and to maximize interoperability.

%prep

%build

%install
# rogue and geonode
GEONODE_LIB=$RPM_BUILD_ROOT%{_localstatedir}/lib/geonode
mkdir -p $GEONODE_LIB/uwsgi/{static,uploaded/thumbs}
pushd $GEONODE_LIB
tar -xf %{SOURCE0} -C .
mv %{name}-%{version} rogue_geonode

# create virtualenv
virtualenv .
export PATH=/usr/pgsql-9.3/bin:$PATH
source bin/activate

# install pip dependencies
unzip %{SOURCE1} -d $GEONODE_LIB
install -m 755 %{SOURCE2} $GEONODE_LIB
pip install -r requirements.txt --no-index --find-links $GEONODE_LIB/pkgs
rm -fr $GEONODE_LIB/pkgs $GEONODE_LIB/requirements.txt

# install rogue_geonode
pushd rogue_geonode
pip install .
popd && popd

tar -xf %{SOURCE3} -C .
python %{name}-geonode-%{geonode_clone_version}/setup.py install
rm -fr %{name}-geonode-%{geonode_clone_version}

# setup supervisord configuration
SUPV_ETC=$RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $SUPV_ETC
install -m 644 %{SOURCE4} $SUPV_ETC/supervisord.conf
GEOSHAPE_LOG=$RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
mkdir -p $GEOSHAPE_LOG
CELERY_LOG=$RPM_BUILD_ROOT%{_localstatedir}/log/celery
mkdir -p $CELERY_LOG
# setup init script
INITD=$RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $INITD
install -m 751 %{SOURCE5} $INITD/%{name}

# setup httpd configuration
HTTPD_CONFD=$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $HTTPD_CONFD
install -m 644 %{SOURCE6} $HTTPD_CONFD/%{name}.conf
install -m 644 %{SOURCE7} $HTTPD_CONFD/proxy.conf

# adjust virtualenv to /var/lib/geonode path
VAR0=$RPM_BUILD_ROOT%{_localstatedir}/lib/geonode
VAR1=%{_localstatedir}/lib/geonode
find $VAR0 -type f -name '*pyc' -exec rm {} +
grep -rl $VAR0 $VAR0 | xargs sed -i 's|'$VAR0'|'$VAR1'|g'

# setup geoshape configuration directory
GEOSHAPE_CONF=$RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $GEOSHAPE_CONF
# local_settings.py
install -m 775 %{SOURCE8} $GEOSHAPE_CONF/local_settings.py

# robots.txt
install -m 755 %{SOURCE9} $GEONODE_LIB/rogue_geonode/%{name}/templates/robots.txt
# add robots.txt as a TemplateView in django original file is urls.py.bak
sed -i.bak "s|urlpatterns = patterns('',|urlpatterns = patterns('',\\n\
url(r'^/robots\\\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),|" $RPM_BUILD_ROOT%{_localstatedir}/lib/geonode/rogue_geonode/%{name}/urls.py

# geoshape-config command
USER_BIN=$RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $USER_BIN
install -m 755 %{SOURCE10} $USER_BIN/

# geogig-cli
unzip -d $RPM_BUILD_ROOT%{_localstatedir}/lib %{SOURCE11}
PROFILE_D=$RPM_BUILD_ROOT%{_sysconfdir}/profile.d
mkdir -p $PROFILE_D
find $RPM_BUILD_ROOT%{_localstatedir}/lib/geogig -type f -name '*bat' -exec rm {} +
echo  'export GEOGIG_HOME="/var/lib/geogig" && PATH="$PATH:$GEOGIG_HOME/bin"' > $PROFILE_D/geogig.sh

# admin.json
install -m 755 %{SOURCE12} $GEOSHAPE_CONF/

# manage.py
install -m 755 %{SOURCE13} $GEONODE_LIB/rogue_geonode/

# geoshape-config.conf
install -m 755 %{SOURCE14} $GEOSHAPE_CONF/

%pre
getent group geoservice >/dev/null || groupadd -r geoservice
usermod -a -G geoservice tomcat
usermod -a -G geoservice apache
getent passwd %{name} >/dev/null || useradd -r -d %{_localstatedir}/lib/geonode/rogue_geonode -g geoservice -s /bin/bash -c "GeoSHAPE Daemon User" %{name}

%post
if [ $1 -eq 1 ] ; then
  ln -s %{_sysconfdir}/%{name}/local_settings.py %{_localstatedir}/lib/geonode/rogue_geonode/%{name}/local_settings.py
  source %{_sysconfdir}/profile.d/geogig.sh
  chgrp -hR geoservice /var/lib/geoserver_data
  chmod -R 775 /var/lib/geoserver_data
fi

%preun
find %{_localstatedir}/lib/geonode -type f -name '*pyc' -exec rm {} +
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat stop > /dev/null 2>&1
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/service httpd stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
  #remove soft link and virtual environment
  rm -fr %{_localstatedir}/lib/geonode
fi

%postun

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(755,%{name},geoservice,755)
%{_localstatedir}/lib/geogig
%{_sysconfdir}/profile.d/geogig.sh
%{_localstatedir}/lib/geonode
%config(noreplace) %{_sysconfdir}/%{name}/local_settings.py
%{_sysconfdir}/%{name}/admin.json
%{_sysconfdir}/%{name}/%{name}-config.conf
%defattr(775,%{name},geoservice,775)
%dir %{_localstatedir}/lib/geonode/uwsgi/static
%dir %{_localstatedir}/lib/geonode/uwsgi/uploaded
%defattr(744,%{name},geoservice,744)
%dir %{_localstatedir}/log/celery
%dir %{_localstatedir}/log/%{name}
%defattr(644,%{name},geoservice,644)
%dir %{_sysconfdir}/%{name}/
%defattr(644,apache,apache,644)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/proxy.conf
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/supervisord.conf
%defattr(-,root,root,-)
%config %{_sysconfdir}/init.d/%{name}
%{_prefix}/bin/%{name}-config
%doc ../SOURCES/license/GNU

%changelog
* Tue Jan 05 2016 BerryDaniel <dberry@boundlessgeo.com> [1.7.11-2]
- Added requirements.txt
- Change to install from local source using pip
- Added Access-Control Headers for Apache

* Mon Jan 04 2016 BerryDaniel <dberry@boundlessgeo.com> [1.7.11-1]
- Upgraded to GeoSHAPE 1.7.11

* Wed Dec 30 2015 BerryDaniel <dberry@boundlessgeo.com> [1.7.9-1]
- Upgraded to GeoSHAPE 1.7.9

* Tue Dec 29 2015 BerryDaniel <dberry@boundlessgeo.com> [1.7.6-0.2]
- Upgraded to GeoSHAPE 1.7.6
- removed file-service.war
- adjustments to geoshape.conf and geoshape-config
- added geoservice group
- added ssl
- added geoshape-config.conf

* Tue Dec 15 2015 BerryDaniel <dberry@boundlessgeo.com> [1.5.1-1]
- Updated geoshape.init to run all apps in supervisor.conf under the geoshape group
- Added five celery workers to supervisor.conf
- Added geogig-cli
- Added rabbitmq-server >= 3.5.6 and erlang >= 18.1 as dependencies

* Tue Dec 08 2015 BerryDaniel <dberry@boundlessgeo.com> [1.5-1]
- Updated geoshape-geonode to GeoNode==2.4
