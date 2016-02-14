%define ver 1.3.40
%define prefix /usr
%define home_page http://www.swig.org
%define docprefix %{prefix}/share

Summary: Simplified Wrapper and Interface Generator
Name: swig
Version: %{ver}
Release: 1%{?dist}
URL: %{home_page}
Source0: %{name}-%{version}.tar.gz
License: BSD
Group: Development/Tools
BuildRoot: %{_tmppath}/%{name}-root

%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%define _unpackaged_files_terminate_build 0

%description
SWIG is a software development tool that connects programs written in C and C++
with a variety of high-level programming languages. SWIG is primarily used with
common scripting languages such as Perl, Python, Tcl/Tk, and Ruby, however the
list of supported languages also includes non-scripting languages such as Java,
OCAML and C#. Also several interpreted and compiled Scheme implementations
(Guile, MzScheme, Chicken) are supported. SWIG is most commonly used to create
high-level interpreted or compiled programming environments, user interfaces,
and as a tool for testing and prototyping C/C++ software. SWIG can also export
its parse tree in the form of XML and Lisp s-expressions. 

%prep
%setup -q -n %{name}-%{version}

%build
# so we can build package from Git source too
[ ! -r configure ] && ./autogen.sh
%configure
make

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc ANNOUNCE CHANGES INSTALL LICENSE README
%doc Doc/*
%{_bindir}/*
%{prefix}/share/*

%changelog
* Sat Feb 13 2016 amirahav <arahav@boundlessgeo.com>
- Initial build

