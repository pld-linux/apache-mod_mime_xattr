%define		mod_name	mime_xattr
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache HTTPD module: mod_mime_xattr
Name:		apache-mod_%{mod_name}
Version:	0.4
Release:	1
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	http://0pointer.de/lennart/projects/mod_mime_xattr/mod_mime_xattr-%{version}.tar.gz
# Source0-md5:	cf04dd8d8ce31a9690f7ddc4495f1b3b
Source1:	apache.conf
URL:		http://0pointer.de/lennart/projects/mod_mime_xattr/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.9
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_mime_xattr is a module for the Apache HTTPD which may be used to
set a range of MIME properties of files served from a document tree
with extended attributes (EAs) as supported by the underlying file
system.

The current version of mod_mime_xattr has support for Linux style EAs
which are supported by Linux 2.4 with the ACL/EA patches applied and
vanilla Linux 2.6. The following attributes may be used:

- user.mime_type: set the MIME type of a file explicitly. This
  attribute is compatible with the shared MIME database specification as
  published by freedesktop.org
- user.charset: set the charset used in a file
- user.mime_encoding: set the MIME encoding of a file (e.g. gzip)
- user.apache_handler: set the apache handler of a file explicitly

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%configure \
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
install -p src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/mod_%{mod_name}.so
