#!/usr/bin/env bash

yum -y install http://yum.geoshape.org/geoshape-repo-1.0.0-1.el6.noarch.rpm
sudo yum -y update
sudo yum -y install gcc gcc-c++ make expat-devel db4-devel gdbm-devel sqlite-devel readline-devel zlib-devel bzip2-devel openssl-devel tk-devel gdal-devel-1.11.2 libxslt-devel libxml2-devel libjpeg-turbo-devel zlib-devel libtiff-devel freetype-devel littlecms-devel proj-devel geos-devel postgresql93-devel unzip rpmdevtools git python27-devel python27-virtualenv
pushd /vagrant/SOURCES
./get_sources.sh
popd
