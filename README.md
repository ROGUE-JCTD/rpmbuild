GeoShape rpmbuild for Enterprise Linux 6
----------------------

__Using Vagrant - https://www.vagrantup.com/__

```bash
git clone -b geoint git@github.com:ROGUE-JCTD/rpmbuild.git
cd rpmbuild
vagrant up
vagrant ssh
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/proj.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/lcms2.spec
yum -y install /vagrant/RPMS/*.rpm
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/openjpeg2.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/libkml.spec
yum -y install /vagrant/RPMS/*.rpm
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/gdal.spec
yum -y install /vagrant/RPMS/*.rpm
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/postgis.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/tomcat.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/geoshape.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/geoshape-geoserver.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/erlang.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/mod_xsendfile.spec
```

__The newly created rpms will be located at /vagrant/RPMS__

Once finished close out the vm

```bash
vagrant destroy
```