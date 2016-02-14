%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Summary:	Apache module to send files efficiently
Name:		mod_xsendfile
Version:	0.12
Release:	3%{?dist}
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://tn123.org/%{name}/
Source0:	https://tn123.org/%{name}/%{name}-%{version}.tar.bz2
Source1:	xsendfile.conf
BuildRequires:	httpd-devel
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global modulesdir %{_libdir}/httpd/modules
%global confdir %{_sysconfdir}/httpd/conf.d

%description
%{name} is a small Apache2 module that processes X-SENDFILE headers
registered by the original output handler.

If it encounters the presence of such header it will discard all output and
send the file specified by that header instead using Apache internals
including all optimizations like caching-headers and sendfile or mmap if
configured.

It is useful for processing script-output of e.g. php, perl or any cgi.


%prep
%setup -q


%build
%{_bindir}/apxs -c %{name}.c


%install
rm -rf $%{buildroot}
mkdir -p %{buildroot}/%{modulesdir}
%{_bindir}/apxs -i -S LIBEXECDIR=%{buildroot}/%{modulesdir} -n %{name} %{name}.la
mkdir -p %{buildroot}/%{confdir}
cp -p %SOURCE1 %{buildroot}/%{confdir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc docs/*
%config(noreplace) %{confdir}/xsendfile.conf
%{modulesdir}/%{name}.so


%changelog
* Mon Apr 25 2011 Orion Poplawski <orion@cora.nwra.com> 0.12-3
- Fix license tag

* Wed Dec 1 2010 Orion Poplawski <orion@cora.nwra.com> 0.12-2
- Upstream fixed tar ball packaging

* Mon Oct 25 2010 Orion Poplawski <orion@cora.nwra.com> 0.12-1
- Initial package
