GeoShape rpmbuild for Enterprise Linux 6/7
----------------------

__Using Vagrant - https://www.vagrantup.com/__

__For RHEL/CentOS7 change the vagrant box to bento/centos-7.2__
```bash
git clone -b geoint git@github.com:ROGUE-JCTD/rpmbuild.git
cd rpmbuild
vagrant up
vagrant ssh
version=`rpm -qa \*-release | grep -Ei "redhat|centos" | cut -d"-" -f3`
if [ $version == 7 ];then
  yum -y remove swig
  # RHEL7/CentOS7 come with SWIG 2.0, however Geoserver's GDAL bindings only work with SWIG 1.3.x
  QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/centos7/swig.spec
  yum -y install /vagrant/RPMS/swig-*.rpm
fi

QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/lcms2.spec
yum -y install /vagrant/RPMS/lcms2-*.rpm
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/openjpeg2.spec
yum -y install /vagrant/RPMS/openjpeg2*.rpm

if [ $version == 7 ];then
  QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/centos7/libkml.spec
  yum -y install /vagrant/RPMS/libkml-*.rpm
  QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/centos7/gdal.spec
else
  QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/libkml.spec
  yum -y install /vagrant/RPMS/libkml-*.rpm
  QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/gdal.spec
fi
yum -y install /vagrant/RPMS/gdal-*
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/postgis.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/tomcat.spec

if [ $version == 7 ];then
  QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/centos7/geoshape.spec
  QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/centos7/mod_xsendfile.spec
else
  QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/geoshape.spec
  QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/mod_xsendfile.spec
fi

QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/geoshape-geoserver.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/erlang.spec
```

__The newly created rpms will be located at /vagrant/RPMS__

Once finished close out the vm

```bash
vagrant destroy
```