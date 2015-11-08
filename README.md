GeoShape rpmbuild for Enterprise Linux 6
----------------------

__as a non-root user with sudo access on an EL6 Operating System...__

```bash
cd ~
sudo yum -y update
sudo yum -y install git
git clone git@github.com:ROGUE-JCTD/rpmbuild.git
sudo yum -y install rpmdevtools
sudo yum -y install http://yum.geonode.boundlessps.com/geonode-repo-1.0.0-1.el6.noarch.rpm
sudo yum -y install python27-devel python27-virtualenv gdal-devel=1.11.2 proj-devel postgresql93-devel libxslt-devel pcre-devel gcc gcc-c++ bzip2-devel db4-devel expat-devel gdbm-devel ncurses-devel openssl-devel readline-devel sqlite-devel tk-devel tcl-devel unzip wget 
```

Build Steps
```bash
cd rpmbuild/SOURCES
./get_sources
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -bb ~/rpmbuild/SPECS/geoshape.spec
```
