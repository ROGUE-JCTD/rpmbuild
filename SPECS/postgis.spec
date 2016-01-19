
%define pgdir /usr/pgsql-9.5
%define mver 2.2
%define majorversion 22

Summary:        Geographic Information Systems Extensions to PostgreSQL
Name:           postgis
Version:        2.2.1
Release:        1%{?dist}
License:        GPL v2
Group:          Applications/Databases
Source:         http://download.osgeo.org/postgis/source/postgis-%{version}.tar.gz
Source1:        %{name}.rpmlintrc
Vendor:         The PostGIS Project
Packager:       Otto Dassau <dassau@gbd-consult.de>
URL:            http://postgis.org/


%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

BuildRequires:  geos-devel >= 3.5.0
BuildRequires:  gdal-devel >= 2.0.1
BuildRequires:  proj-devel >= 4.8.0
BuildRequires:  libxml2-devel
BuildRequires:  json-c-devel >= 0.11
BuildRequires:  gtk2-devel
BuildRequires:  gettext-devel
BuildRequires:  perl
BuildRequires:  gcc-c++ libxslt-devel dos2unix
BuildRequires:  postgresql95-devel

AutoReq:        no
Requires:       postgresql95-libs
Requires:       geos >= 3.5.0
Requires:       proj >= 4.8.0
Requires:       gdal >= 2.0.1
Requires:       json-c >= 0.11
Requires:       libxml2 perl gettext

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS
follows the OpenGIS "Simple Features Specification for SQL" and will be
submitted for conformance testing at version 1.0.

%package postgresql95
Summary:        PostGIS for PostgreSQL 9.5
Group:          Applications/Databases
Requires:       %{name} = %{version}
Requires:       postgresql95-server, json-c >= 0.11

%description postgresql95
The postgresql95 package provides the PostGIS server side libraries for
PostgreSQL 9.5.

#%package utils
#Summary:        The utils for PostGIS
#Group:          Applications/Interfaces
#Requires:       %{name} = %{version} perl-DBD-Pg

#%description utils
#The postgis-utils package provides the utilities for PostGIS.

%package gui
Summary:        Graphical shapefile loader and dumper for PostGIS
Group:          Applications/Interfaces
Requires:       %{name} = %{version} gtk2

%description gui
The postgis-gui package provides a graphical shapefile loader and dumper for PostGIS.

%prep
%setup -q


%build
LDFLAGS=-L%{pgdir}/lib
export LD_LIBRARY_PATH=%{pgdir}/lib
# prevent conflicts with a $PROFILE used in the makefiles
export PROFILE=
%configure --with-pgconfig=%{pgdir}/bin/pg_config --with-gui
make

%install
make install DESTDIR=%{buildroot}
mv %{buildroot}%{pgdir}/bin %{buildroot}%{_bindir}
install -m 755 utils/create_undef.pl %{buildroot}%{_bindir}
install -m 755 utils/postgis_restore.pl %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}
install -d %{buildroot}%{_mandir}/man1
install -m 644 doc/man/*.1 %{buildroot}%{_mandir}/man1
#install -d %{buildroot}%{sqldir}
#install -m 755 *.sql %{buildroot}%{sqldir}
#install -d %{buildroot}%{pgdir}/bin
#install -m 755 utils/create_undef.pl %{buildroot}%{pgdir}/bin
#install -m 755 utils/postgis_restore.pl %{buildroot}%{pgdir}/bin

#JD: issue on centos with the perl Pg module, remove all developer scripts
#rm %{buildroot}%{_bindir}/test_*.pl
#rm %{buildroot}%{_bindir}/profile*.pl
#install -d %{buildroot}%{pgdir}/share/man
#install -d %{buildroot}%{pgdir}/share/man/man1
#install -m 644 doc/man/*.1 %{buildroot}%{pgdir}/share/man/man1

perl -e '
foreach $d (split "\n",`find -type d`)
{
  next if $d eq ".";
  foreach $f ("TODO", "README")
  {
    my $r = "$f.$d"; $r =~ s/\.\///; $r =~ s/\//_/g; rename "$d/$f",$r;
    rename "$d.txt/$f",$r;
  }
}
'
dos2unix README.extras_tiger_geocoder
if ! [ -s TODO.loader ]; then
  rm TODO.loader
fi

ls -R

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS README* TODO* doc/html/* loader/README.*
%doc doc/ZMSgeoms.txt doc/postgis_comments.sql
%{_bindir}/shp2pgsql
%{_bindir}/pgsql2shp
%{_bindir}/raster2pgsql
%{_bindir}/*.pl
%{_libdir}/*
%{_includedir}/*
%{_mandir}/*

%files postgresql95
%{pgdir}/lib/*
%defattr(644,root,root)
%{pgdir}/share/contrib/postgis-%{mver}/*
%{pgdir}/share/extension/*
#%{pgdir}/share/man/man1/*
%defattr(755,root,root)

#%files utils
#%defattr(755,root,root)
#%{pgdir}/bin/create_undef.pl
#%{pgdir}/bin/postgis_restore.pl

%files gui
%defattr(755,root,root)
%{_bindir}/shp2pgsql-gui
#%{pgdir}/bin/shp2pgsql-gui

%changelog
* Sat Jan 16 2016 amirahav <arahav@boundlessgeo.com> [1.7.11-3]
- Upgrade PostgreSQL to 9.5
- Upgrade PostGIS to 2.2.1
* Wed Nov 25 2015 Boundless Spatial, Inc <contact@boundlessgeo.com> - 2.1.8
- update to postgis 2.1.8
* Wed Nov 19 2014 Michael Weisman 2.1.4
- update to postgis 2.1.4
* Wed Jun 13 2014 Michael Weisman 2.1.3
- update to postgis 2.1.3
* Tue May 13 2014 Michael Weisman 2.1.1
- update to postgis 2.1.2
* Fri Dec 13 2013 Michael Weisman 2.1.1
- update to postgis 2.1.1
* Mon Sep 23 2013 Justin Deoliveira 2.1.0
- update to postgis 2.1.0
- separating files into client and server packages
* Fri Mar 19 2010 Otto Dassau 1.5.1
- update to current version
* Fri Feb 19 2010 Otto Dassau 1.5.0
- update to current version
- remove fixwarnings.diff patch
- added doc/postgis_comment.sql
* Thu Dec 31 2009 Otto Dassau 1.4.1
- update to current version
* Thu Sep 04 2009 Otto Dassau 1.4.0
- update to current version
- sqldir is now /usr/share/postgresql/contrib
* Wed Jan 28 2009 Otto Dassau 1.3.5
- update to current version
* Tue Nov 25 2008 Otto Dassau 1.3.4
- update to current version
* Mon Jul 14 2008 Otto Dassau 1.3.3
- added rpmlintrc file
* Wed Jul 09 2007 Dirk Stöcker <opensuse@dstoecker.de> 1.3.1
- adapted to openSUSE build service
* Tue Dec 22 2005 Devrim GUNDUZ 1.1.0
- Final fixes for 1.1.0
* Tue Dec 06 2005 Devrim GUNDUZ 1.10
- Update to 1.1.0
* Mon Oct 03 2005 Devrim GUNDUZ
- Make PostGIS build against pgxs so that we don't need PostgreSQL sources.
- Fixed all build errors except jdbc (so, defaulted to 0)
- Added new files under utils
- Removed postgis-jdbc2-makefile.patch (applied to -head)
* Tue Sep 27 2005 Devrim GUNDUZ 1.0.4
- Update to 1.0.4
* Sun Apr 20 2005 Devrim GUNDUZ 1.0.0
- 1.0.0 Gold
* Sun Apr 17 2005 Devrim GUNDUZ
- Modified the spec file so that we can build JDBC2 RPMs...
- Added -utils RPM to package list.
* Fri Apr 15 2005 Devrim GUNDUZ
- Added preun and postun scripts.
* Sat Apr 09 2005 Devrim GUNDUZ
- Initial RPM build
- Fixed libdir so that PostgreSQL installations will not complain about it.
- Enabled --with-geos and modified the old spec.


