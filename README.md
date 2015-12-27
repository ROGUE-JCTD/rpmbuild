GeoShape rpmbuild for Enterprise Linux 6
----------------------

__Using Vagrant - https://www.vagrantup.com/__

```bash
git clone -b geoint git@github.com:ROGUE-JCTD/rpmbuild.git
cd rpmbuild
vagrant up
vagrant ssh
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/geoshape.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/geoshape-geoserver.spec
vagrant destroy
```

The newly created rpms will be located at /vagrant/RPMS

If using this on a disconnected environment the following links include non "BASE" rpms in zip file format:

__Note:__ devel rpms are needed only from buildign the GeoSHAPE rpms.

[external.zip - 47.3MB](http://yum.geoshape.org/zip/external.zip)
- elasticsearch-1.6.0.noarch.rpm
- erlang-18.1-1.el6.x86_64.rpm
- rabbitmq-server-3.5.6-1.noarch.rpm

[opengeo.zip - 51.2 MB](http://yum.geoshape.org/zip/opengeo.zip)
- gdal-1.11.2-1.el6.x86_64.rpm
- gdal-devel-1.11.2-1.el6.x86_64.rpm
- geos-3.4.2-1.el6.x86_64.rpm
- geos-devel-3.4.2-1.el6.x86_64.rpm
- postgis21-2.1.7-1.x86_64.rpm
- postgis21-postgresql93-2.1.7-1.x86_64.rpm
- postgresql93-9.3.5-og1.el6.x86_64.rpm
- postgresql93-devel-9.3.5-og1.el6.x86_64.rpm
- postgresql93-libs-9.3.5-og1.el6.x86_64.rpm
- postgresql93-server-9.3.5-og1.el6.x86_64.rpm
- proj-4.8.0-3.el6.x86_64.rpm
- proj-devel-4.8.0-3.el6.x86_64.rpm
- tomcat-7.0.33-4.el6.noarch.rpm
- tomcat-el-2.2-api-7.0.33-4.el6.noarch.rpm
- tomcat-jsp-2.2-api-7.0.33-4.el6.noarch.rpm
- tomcat-lib-7.0.33-4.el6.noarch.rpm
- tomcat-servlet-3.0-api-7.0.33-4.el6.noarch.rpm

[python27.zip - 17.8 MB](http://yum.geoshape.org/zip/python27.zip)
- python27-2.7.10-2.el6.x86_64.rpm
- python27-devel-2.7.10-2.el6.x86_64.rpm
- python27-setuptools-18.7.1-1.el6.noarch.rpm
- python27-virtualenv-13.1.0-1.el6.noarch.rpm
