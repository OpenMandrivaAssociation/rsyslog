%define _libdir /%{_lib}

Summary:	Enhanced system logging and kernel message trapping daemons
Name:		rsyslog
Version:	3.20.3
Release:	%mkrel 1
License:	GPLv3
Group:		System/Kernel and hardware
URL:		http://www.rsyslog.com/
Source0:	http://download.rsyslog.com/%{name}/%{name}-%{version}.tar.gz
Source1:	rsyslog.init
Source2:	rsyslog.sysconfig
Source3:	rsyslog.conf
Source4:	00_common.conf
Source5:	01_mysql.conf
Source6:	02_pgsql.conf
Source7:	03_gssapi.conf
Source8:	04_relp.conf
Source9:	05_dbi.conf
Source10:	06_snmp.conf
Source11:	sysklogd.conf
Source12:	07_rsyslog.log
Patch0:		rsyslog-3.20.3-undef.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	krb5-devel
BuildRequires:	libdbi-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel >= 4.0
BuildRequires:	net-snmp-devel
BuildRequires:	pkgconfig
BuildRequires:	postgresql-devel
BuildRequires:	relp-devel
BuildRequires:	zlib-devel
Requires:	logrotate
Provides:       syslog-daemon
Requires(post):	rpm-helper
Requires(preun):rpm-helper
#Provides:	sysklogd = 1.4.3-1
#Obsoletes:	sysklogd < 1.4.3-1
Conflicts:	logrotate < 3.5.2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Rsyslog is an enhanced multi-threaded syslogd supporting, among others, MySQL,
PostgreSQL, syslog/tcp, RFC 3195, permitted sender lists, filtering on any
message part, and fine grain output format control. It is quite compatible to
stock sysklogd and can be used as a drop-in replacement. Its advanced features
make it suitable for enterprise-class, encryption protected syslog relay chains
while  at the same time being very easy to setup for the novice user.

 o lmnet.so    - Implementation of network related stuff.
 o lmregexp.so - Implementation of regexp related stuff.
 o lmtcpclt.so - This is the implementation of TCP-based syslog clients.
 o lmtcpsrv.so - Common code for plain TCP based servers.
 o imtcp.so    - This is the implementation of the TCP input module.
 o imudp.so    - This is the implementation of the UDP input module.
 o imuxsock.so - This is the implementation of the Unix sockets input module.
 o imklog.so   - The kernel log input module for Linux.
 o immark.so   - This is the implementation of the build-in mark message input
                 module.
 o imfile.so - This is the input module for reading text file data.

%package	mysql
Summary:	MySQL support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

 o ommysql.so - This is the implementation of the build-in output module for
                MySQL.

%package	pgsql
Summary:	PostgreSQL support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

 o ompgsql.so - This is the implementation of the build-in output module for
                PgSQL.

%package	gssapi
Summary:	GSS-API support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	gssapi
The rsyslog-gssapi package contains dynamic shared objects that will add
GSS-API support to rsyslog.

 o lmgssutil.so - This is a miscellaneous helper class for gss-api features.
 o imgssapi.so  - This is the implementation of the GSSAPI input module.
 o omgssapi.so  - This is the implementation of the build-in forwarding output
                  module.

%package	relp
Summary:	RELP support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	relp
The rsyslog-relp package contains a dynamic shared object that will add
RELP support to rsyslog.

 o imrelp.so - This is the implementation of the RELP input module.
 o omrelp.so - This is the implementation of the RELP output module.

%package	dbi
Summary:	Dbi support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	dbi
The rsyslog-dbi package contains a dynamic shared object that will add
dbi driver support to rsyslog.

 o omlibdbi.so - This is the implementation of the dbi output module.

%package	snmp
Summary:	SNMP support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	snmp
The rsyslog-snmp package contains a dynamic shared object that will add
SNMP support to rsyslog.

 o omsnmp.so - This module sends an snmp trap.

%package	docs
Summary:	HTML documentation for rsyslog
Group:		System/Kernel and hardware

%description	docs
This package contains the HTML documentation for rsyslog.

%prep

%setup -q
%patch0 -p0 -b .undef

mkdir -p Mandriva
cp %{SOURCE1} Mandriva/rsyslog.init
cp %{SOURCE2} Mandriva/rsyslog.sysconfig
cp %{SOURCE3} Mandriva/rsyslog.conf
cp %{SOURCE4} Mandriva/00_common.conf
cp %{SOURCE5} Mandriva/01_mysql.conf
cp %{SOURCE6} Mandriva/02_pgsql.conf
cp %{SOURCE7} Mandriva/03_gssapi.conf
cp %{SOURCE8} Mandriva/04_relp.conf
cp %{SOURCE9} Mandriva/05_dbi.conf
cp %{SOURCE10} Mandriva/06_snmp.conf
cp %{SOURCE11} Mandriva/syslog.conf
cp %{SOURCE12} Mandriva/rsyslog.log

%build
%serverbuild

%configure2_5x \
    --disable-static \
    --sbindir=/sbin \
    --enable-largefile \
    --enable-regexp \
    --enable-zlib \
    --enable-gssapi-krb5 \
    --enable-pthreads \
    --enable-klog \
    --enable-inet \
    --enable-mysql \
    --enable-pgsql \
    --enable-libdbi \
    --enable-snmp \
    --enable-rsyslogd \
    --enable-mail \
    --enable-relp \
    --enable-imfile \
    --enable-imtemplate

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d -m 755 %{buildroot}%{_initrddir}
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -d -m 755 %{buildroot}%{_sysconfdir}/rsyslog.d

install -p -m 755 Mandriva/rsyslog.init %{buildroot}%{_initrddir}/rsyslog
install -p -m 644 Mandriva/rsyslog.conf %{buildroot}%{_sysconfdir}/rsyslog.conf
install -p -m 644 Mandriva/syslog.conf %{buildroot}%{_sysconfdir}/syslog.conf
install -p -m 644 Mandriva/rsyslog.log %{buildroot}%{_sysconfdir}/logrotate.d/rsyslog
install -p -m 644 Mandriva/rsyslog.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/rsyslog
install -p -m 644 Mandriva/*_*.conf %{buildroot}%{_sysconfdir}/rsyslog.d/

#get rid of *.la
rm %{buildroot}/%{_libdir}/rsyslog/*.la

# cleanup
rm -f %{buildroot}%{_libdir}/rsyslog/imtemplate.so

# fix html docs
rm -rf html_docs; mkdir -p html_docs
cp doc/*.html doc/*.jpg html_docs/
chmod 644 html_docs/*

%post
%_post_service rsyslog

for n in /var/log/{messages,secure,maillog,spooler}; do
    [ -f $n ] && continue
    umask 066 && touch $n
done

if [ "$1" = 0 ]; then
    # use sysklogd configuration file
    if [ -f /etc/sysconfig/syslog ]; then
        mv -f /etc/sysconfig/rsyslog /etc/sysconfig/rsyslog.rpmnew
        cp /etc/sysconfig/syslog /etc/sysconfig/rsyslog
    fi
fi

%triggerpostun -- rsyslog < 2.0.1-2mdv2008.1
if [ ! -f /etc/syslog.conf ]; then
    # restore syslog.conf
    mv -f /etc/rsyslog.conf /etc/syslog.conf
    mv -f /etc/rsyslog.conf.rpmnew /etc/rsyslog.conf
fi

%triggerun -- rsyslog < 3.0.0
/bin/kill `cat /var/run/rklogd.pid 2> /dev/null` > /dev/null 2>&1 ||:

%preun
%_preun_service rsyslog

%postun
if [ "$1" -ge "1" ]; then
    %{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :
fi

%post mysql
%{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :

%preun mysql
if [ "$1" = 0 ]; then
    %{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :
fi

%post pgsql
%{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :

%preun pgsql
if [ "$1" = 0 ]; then
    %{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :
fi

%post gssapi
%{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :

%preun gssapi
if [ "$1" = 0 ]; then
    %{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :
fi

%post relp
%{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :

%preun relp
if [ "$1" = 0 ]; then
    %{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :
fi

%post dbi
%{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :

%preun dbi
if [ "$1" = 0 ]; then
    %{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :
fi

%post snmp
%{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :

%preun snmp
if [ "$1" = 0 ]; then
    %{_initrddir}/rsyslog condrestart > /dev/null 2>/dev/null || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README  doc/rsyslog-example.conf
%{_initrddir}/rsyslog
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/syslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/rsyslog
%dir %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_common.conf
/sbin/rsyslogd
%dir %{_libdir}/rsyslog
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/imklog.so
%{_libdir}/rsyslog/immark.so
%{_libdir}/rsyslog/imtcp.so
%{_libdir}/rsyslog/imudp.so
%{_libdir}/rsyslog/imuxsock.so
%{_libdir}/rsyslog/lmnet.so
%{_libdir}/rsyslog/lmnetstrms.so
%{_libdir}/rsyslog/lmnsd_ptcp.so
%{_libdir}/rsyslog/lmregexp.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/ommail.so
%{_mandir}/*/*

%files mysql
%defattr(-,root,root)
%doc plugins/ommysql/createDB.sql plugins/ommysql/contrib/delete_mysql
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_mysql.conf
%{_libdir}/rsyslog/ommysql.so

%files pgsql
%defattr(-,root,root)
%doc plugins/ompgsql/createDB.sql
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_pgsql.conf
%{_libdir}/rsyslog/ompgsql.so

%files gssapi
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_gssapi.conf
%{_libdir}/rsyslog/omgssapi.so
%{_libdir}/rsyslog/imgssapi.so
%{_libdir}/rsyslog/lmgssutil.so

%files relp
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_relp.conf
%{_libdir}/rsyslog/imrelp.so
%{_libdir}/rsyslog/omrelp.so

%files dbi
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_dbi.conf
%{_libdir}/rsyslog/omlibdbi.so

%files snmp
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_snmp.conf
%{_libdir}/rsyslog/omsnmp.so

%files docs
%defattr(-,root,root)
%doc html_docs/*
