GeoShape rpmbuild for Enterprise Linux 6
----------------------

__as a non-root user with sudo access on an EL6 Operating System...__

```bash
cd /etc/yum.repos.d
sudo wget http://yum.boundlessgeo.com/suite/v47/rhel/6Server/x86_64/OpenGeo.repo
sudo yum -y update
sudo yum -y install rpmdevtools
sudo yum -y install git
cd ~
git clone -b geoint git@github.com:ROGUE-JCTD/rpmbuild.git
sudo yum -y install gcc gcc-c++ make expat-devel db4-devel gdbm-devel sqlite-devel readline-devel zlib-devel bzip2-devel openssl-devel tk-devel gdal-devel-1.11.2 libxslt-devel libxml2-devel libjpeg-turbo-devel zlib-devel libtiff-devel freetype-devel littlecms-devel proj-devel geos-devel postgresql93-devel unzip
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -bb ~/rpmbuild/SPECS/python27.spec
sudo yum install -y ~/rpmbuild/RPMS/python27-*
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -bb ~/rpmbuild/SPECS/python27-setuptools.spec
sudo yum install -y ~/rpmbuild/RPMS/python27-*
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -bb ~/rpmbuild/SPECS/python27-virtualenv.spec
sudo yum install -y ~/rpmbuild/RPMS/python27-*
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -bb ~/rpmbuild/SPECS/geoshape.spec
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -bb ~/rpmbuild/SPECS/geoshape-geoserver.spec
```
