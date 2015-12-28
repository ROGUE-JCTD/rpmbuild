echo 'downloading sources'
[ -f geoshape-1.7.6.tar.gz ] && rm -f geoshape-1.7.6.tar.gz
wget https://pypi.python.org/packages/source/g/geoshape/geoshape-1.7.6.tar.gz
[ -f geoshape-geonode-1.4.tar.gz ] && rm -f geoshape-geonode-1.4.tar.gz
wget https://pypi.python.org/packages/source/g/geoshape-geonode/geoshape-geonode-1.4.tar.gz
[ -f Python-2.7.10.tgz ] && rm -f Python-2.7.10.tgz
wget http://yum.geoshape.org/src/Python-2.7.10.tgz
[ -f geogig-cli-app-1.0.zip ] && rm -f geogig-cli-app-1.0.zip
wget http://yum.geoshape.org/src/geogig-cli-app-1.0.zip
[ -f geoserver.war ] && rm -f geoserver.war
wget http://yum.geoshape.org/src/geoserver.war
[ -f geoserver_data-geogig_od3.zip ] && rm -f geoserver_data-geogig_od3.zip
wget http://yum.geoshape.org/src/geoserver_data-geogig_od3.zip
[ -f setuptools-18.7.1.tar.gz ] && rm -f setuptools-18.7.1.tar.gz
wget http://yum.geoshape.org/src/setuptools-18.7.1.tar.gz
[ -f virtualenv-13.1.0.tar.gz ] && rm -f virtualenv-13.1.0.tar.gz
wget http://yum.geoshape.org/src/virtualenv-13.1.0.tar.gz
echo 'finished get sources'
