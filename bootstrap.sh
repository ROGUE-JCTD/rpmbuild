#!/usr/bin/env bash
pushd /etc/yum.repos.d
wget http://yum.geoshape.org/GeoSHAPE-rpmbuild.repo
rpm -ivh http://yum.postgresql.org/9.5/redhat/rhel-6-x86_64/pgdg-centos95-9.5-2.noarch.rpm
popd
sudo yum -y update
sudo yum -y install gcc gcc-c++ make expat-devel db4-devel gdbm-devel sqlite-devel readline-devel zlib-devel bzip2-devel openssl-devel tk-devel libxslt-devel libxml2-devel libjpeg-turbo-devel zlib-devel libtiff-devel freetype-devel littlecms-devel proj-devel geos-devel postgresql95-devel zip unzip rpmdevtools git python27-devel python27-virtualenv createrepo libcurl-devel poppler-devel xerces-c-devel java-1.8.0-openjdk-devel ant chrpath libtool swig cmake doxygen libpng-devel cppunit autoconf libgcj-devel json-c-devel gtk2-devel gettext-devel dos2unix --exclude=java-1.6.0-openjdk* httpd-devel
pushd /vagrant/SOURCES
./get_sources.sh
popd