#!/bin/bash

echo 'downloading sources'
echo '-------------------'
srcs=()
srcs+=("http://yum.geoshape.org/src/Python-2.7.10.tgz")
srcs+=("http://yum.geoshape.org/src/geoserver.war")
srcs+=("http://yum.geoshape.org/src/geoserver_data-geogig_od3.zip")
srcs+=("http://yum.geoshape.org/src/geogig-cli-app-1.0.zip")
srcs+=("http://yum.geoshape.org/src/setuptools-18.7.1.tar.gz")
srcs+=("http://yum.geoshape.org/src/virtualenv-13.1.0.tar.gz")
for src in "${srcs[@]}"
do
  filename=`echo $src | sed 's/.*\///'`
  if [[ ! -f $filename ]]
  then
    wget $src
  else
    echo $filename "already downloaded"
  fi
done
[ ! -d pkgs ] && mkdir pkgs
pushd pkgs
while read line;
do
  name=`echo $line | awk -F '==' '{print $1}'`
  version=`echo $line | awk -F '==' '{print $2}'`
  base="https://pypi.python.org/packages/source"
  name_lc=`echo $name | tr '[:upper:]' '[:lower:]'`
  loop=1
  for ext in {.tar.gz,.zip}
  do
    urls=()
    urls+=("${base}/${name:0:1}/${name}/${name}-${version}${ext}")
    # substitute a char with alpha in version variable
    urls+=("${base}/${name:0:1}/${name}/${name}-${version//a/alpha}${ext}")
    # substitute b char with beta in version variable
    urls+=("${base}/${name:0:1}/${name}/${name}-${version//b/beta}${ext}")
    # modify name variable to lowercase
    urls+=("${base}/${name:0:1}/${name}/${name_lc}-${version}${ext}")
    # substitute hypens with undrscores in name variable
    urls+=("${base}/${name:0:1}/${name//-/_}/${name//-/_}-${version}${ext}")
    # pad version variable with a 0.0 for Unidecode
    urls+=("${base}/${name:0:1}/${name}/${name}-${version//0./0.0}${ext}")
    for url in "${urls[@]}"
    do
      filename=`echo $url | sed 's/.*\///'`
      if [[ `wget -S --spider $url  2>&1 | grep 'HTTP/1.1 200 OK'` ]]
      then
        if [[ ! -f $filename ]]
        then
          wget $url
          loop=0
          break
        else
          echo $filename "already downloaded"
          loop=0
          break
        fi
      fi
    done
    [ $loop -eq 0 ] && break
  done
  [ $loop -eq 1 ] && echo $name-$version "not found" >> missing-packages.txt
done < ../requirements.txt
cp -f geoshape-* ..
popd
[ -f pkgs.zip ] && rm -f pkgs.zip
zip -r pkgs.zip pkgs -x "*.DS_Store"
echo '-------------------'
echo 'finished get sources'
