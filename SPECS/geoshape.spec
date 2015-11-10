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
Source1:          static.zip
Source2:          geoshape.supervisord.conf
Source3:          geoshape.init
Source4:          geoshape.conf
Source5:          geoshape.proxy.conf
Source6:          geoshape.README
Source7:          geoshape.local_settings.py
Source8:          geoshape.robots.txt
Source9:          geoshape-geonode-1.3.1.tar.gz
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
BuildRequires:    libjpeg-devel
Requires:         python27
Requires:         python27-virtualenv
Requires:         gdal = 1.11.2
Requires:         postgresql93
Requires:         postgresql93-server
Requires:         postgis21-postgresql93
Requires:         proj
Requires:         httpd
Requires:         libxslt
Requires:         libjpeg
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
Patch0:        geoshape.web.xml.patch
Patch1:        geoshape.context.xml.patch
BuildArch:     noarch

%description geoserver
GeoServer is built with the geoserver-geonode-ext, which extends GeoServer
with certain JSON, REST, and security capabilites specifically for GeoShape %{version}-%{release}.

%prep
[ -d $RPM_SOURCE_DIR/geoserver ] && rm -rf $RPM_SOURCE_DIR/geoserver
unzip $RPM_SOURCE_DIR/geoserver.war -d $RPM_SOURCE_DIR/geoserver
[ -d $RPM_SOURCE_DIR/data ] && rm -rf $RPM_SOURCE_DIR/data
unzip $RPM_SOURCE_DIR/data.zip -d $RPM_SOURCE_DIR/data
pushd $RPM_SOURCE_DIR/geoserver

%patch0 -p1
%patch1 -p1

popd

%build

%install
# rogue and geonode
GEONODE_LIB=$RPM_BUILD_ROOT%{_localstatedir}/lib/geonode
mkdir -p $GEONODE_LIB
pushd $GEONODE_LIB
git clone https://github.com/ROGUE-JCTD/rogue_geonode

# create virtualenv
virtualenv-2.7 .
export PATH=/usr/pgsql-9.3/bin:$PATH
source bin/activate

# install rogue_geonode
pushd rogue_geonode
pip install .
popd && popd

# install geoshape_geonode from source
tar -xf %{SOURCE9} -C .
python geoshape-geonode-1.3.1/setup.py install 
rm -fr geoshape-geonode-1.3.1

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
install -m 755 %{SOURCE6} $GEOSHAPE_CONF/README

# additions to mapstory directory
# local_settings.py
install -m 755 %{SOURCE7} $GEONODE_LIB/rogue_geonode/%{name}/local_settings.py
# robots.txt
install -m 755 %{SOURCE8} $GEONODE_LIB/rogue_geonode/%{name}/templates/robots.txt
# add robots.txt as a TemplateView in django original file is urls.py.bak
sed -i.bak "s|urlpatterns = patterns('',|urlpatterns = patterns('',\\n\
url(r'^/robots\\\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),|" $RPM_BUILD_ROOT%{_localstatedir}/lib/geonode/rogue_geonode/%{name}/urls.py

# setup envionment for geonode user
echo "export PYTHONPATH=/var/lib/geonode:/var/lib/geonode/lib/python2.7/site-packages" >> $GEONODE_LIB/rogue_geonode/.bash_profile
echo "alias python='/var/lib/geonode/bin/python'" >> $GEONODE_LIB/rogue_geonode/.bash_profile
echo "alias pip='python /var/lib/geonode/bin/pip'" >> $GEONODE_LIB/rogue_geonode/.bash_profile
echo "alias activate='source /var/lib/geonode/bin/activate'" >> $GEONODE_LIB/rogue_geonode/.bash_profile
echo "alias collectstatic='python /var/lib/geonode/rogue_geonode/manage.py collectstatic'" >> $GEONODE_LIB/rogue_geonode/.bash_profile
echo "alias syncdb='python /var/lib/geonode/rogue_geonode/manage.py syncdb'" >> $GEONODE_LIB/rogue_geonode/.bash_profile
echo "alias createsuperuser='python /var/lib/geonode/rogue_geonode/manage.py createsuperuser'" >> $GEONODE_LIB/rogue_geonode/.bash_profile

# GeoServer Install
CX_ROOT=$RPM_BUILD_ROOT%{_sysconfdir}/tomcat/Catalina/localhost
WEBAPPS=$RPM_BUILD_ROOT%{_localstatedir}/lib/tomcat/webapps
GS=$RPM_SOURCE_DIR/geoserver
DATA=$RPM_BUILD_ROOT%{_localstatedir}/lib/geoserver
WAR_DATA=$RPM_SOURCE_DIR/data
CX=$RPM_SOURCE_DIR/geoserver/WEB-INF/classes/org/geonode/security/geoserver.xml
SQL=$RPM_SOURCE_DIR/geoserver/WEB-INF/classes/org/geonode/security/geonode_authorize_layer.sql
mkdir -p $CX_ROOT $WEBAPPS
cp -rp $CX $CX_ROOT
cp -rp $GS $WEBAPPS
if [ ! -d $DATA ]; then
  mkdir -p $DATA
  cp -R $WAR_DATA/* $DATA
fi
cp -rp $SQL $DATA
rm -fr $GS

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -d %{_localstatedir}/lib/geonode/rogue_geonode -g %{name} -s /bin/bash -c "GeoShape Daemon User" %{name}

%post
if [ $1 -eq 1 ] ; then
  /sbin/chkconfig --add %{name}
  ln -s %{_localstatedir}/lib/geonode/rogue_geonode/%{name}/local_settings.py %{_sysconfdir}/%{name}/local_settings.py
  echo ""
  echo " GeoShape Version - %{version}-%{release}"
  echo ""
  echo "     -------------------------------     "
  echo "              Important!!!               "
  echo "                                         "
  echo "      Reference /etc/geoshape/README     "
  echo "         for post configuration          "
  echo "     -------------------------------     "
  echo ""
  echo ""
fi

%post geoserver
if [ $1 -eq 1 ] ; then
  # add Java specific options
  echo '# Next line added for geoshape service' >> %{_sysconfdir}/tomcat/tomcat.conf
  echo 'JAVA_OPTS="-Xmx1024m -XX:MaxPermSize=256m"' >> %{_sysconfdir}/tomcat/tomcat.conf
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

%preun geoserver
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat stop > /dev/null 2>&1
  rm -fr %{_localstatedir}/lib/tomcat/webapps/geoserver
  rm -f %{_sysconfdir}/tomcat/Catalina/localhost/geoserver.xml
  echo ""
  echo ""
  echo "  -------------------------------"
  echo "           Important!!!          "
  echo "                                 "
  echo "     Uninstall does not delete   "
  echo "      /var/lib/geoserver/data    "
  echo "  -------------------------------"
  echo ""
  echo ""
fi

%postun

%postun geoserver
if [ $1 -eq 1 ] ; then
  /sbin/service tomcat condrestart >/dev/null 2>&1
fi

%clean 
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}
[ -d $RPM_SOURCE_DIR/geoserver ] && rm -rf $RPM_SOURCE_DIR/geoserver
[ -d $RPM_SOURCE_DIR/data ] && rm -rf $RPM_SOURCE_DIR/data
%files
%defattr(755,%{name},%{name},-)
%{_localstatedir}/lib/geonode/
%config(noreplace) %{_localstatedir}/lib/geonode/rogue_geonode/%{name}/local_settings.py
%defattr(744,%{name},%{name},-)
%{_localstatedir}/log/%{name}/
%defattr(644,%{name},%{name},-)
%dir %{_sysconfdir}/%{name}/
%{_sysconfdir}/%{name}/README
%defattr(644,apache,apache,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/proxy.conf
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/supervisord.conf
%defattr(-,root,root,-)
%config %{_sysconfdir}/init.d/%{name}
%doc ../SOURCES/license/GNU

%files geoserver
%defattr(-,root,root,-)
%attr(-,tomcat,tomcat) %{_localstatedir}/lib/tomcat/webapps/geoserver
%attr(-,tomcat,tomcat) %{_localstatedir}/lib/geoserver
%dir %{_sysconfdir}/tomcat/Catalina/localhost
%attr(-,tomcat,tomcat) %{_sysconfdir}/tomcat/Catalina/localhost/geoserver.xml
%doc ../SOURCES/license/geoserver/GPL
%doc ../SOURCES/license/GNU

%changelog
* Sun Nov 8 2015 Daniel Berry <dberry@boundlessgeo.com> 1.5-0.1.beta
- add comments
