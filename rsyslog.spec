Summary:	Enhanced system logging and kernel message trapping daemons
Name:		rsyslog
Version:	1.20.1
Release:	%mkrel 1
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.rsyslog.com/
Source0:	http://download.adiscon.com/rsyslog/%{name}-%{version}.tar.gz
Source1:	rsyslog.init
Source2:	rsyslog.sysconfig
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mysql-devel >= 4.0
BuildRequires:	postgresql-devel
BuildRequires:	zlib-devel
Requires:	logrotate
Provides:       syslog-daemon
Requires(post):	rpm-helper
Requires(preun):rpm-helper
#Provides:	sysklogd = 1.4.3-1
#Obsoletes:	sysklogd < 1.4.3-1
Conflicts:	logrotate < 3.5.2

%description
Rsyslog is an enhanced multi-threaded syslogd supporting, among others, MySQL,
PostgreSQL, syslog/tcp, RFC 3195, permitted sender lists, filtering on any
message part, and fine grain output format control. It is quite compatible to
stock sysklogd and can be used as a drop-in replacement. Its advanced features
make it suitable for enterprise-class, encryption protected syslog relay chains
while  at the same time being very easy to setup for the novice user.

%package	mysql
Summary:	MySQL support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%package	pgsql
Summary:	PostgreSQL support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

%package	docs
Summary:	HTML documentation for rsyslog
Group:		System/Kernel and hardware

%description	docs
This package contains the HTML documentation for rsyslog.

%prep

%setup -q

%build
%serverbuild

%configure2_5x \
    --sbindir=/sbin \
    --enable-mysql \
    --enable-pgsql \
    --disable-static

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d -m 755 %{buildroot}%{_initrddir}
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d

install -p -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/rsyslog
install -p -m 644 redhat/rsyslog.conf %{buildroot}%{_sysconfdir}/rsyslog.conf
install -p -m 644 redhat/rsyslog.log %{buildroot}%{_sysconfdir}/logrotate.d/rsyslog
install -p -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/rsyslog

#get rid of *.la
rm %{buildroot}/%{_libdir}/rsyslog/*.la

# fix html docs
rm -rf html_docs; mkdir -p html_docs
cp doc/* html_docs/
chmod 644 html_docs/*
rm -f html_docs/Makefile*

%post
%_post_service rsyslog

for n in /var/log/{messages,secure,maillog,spooler}; do
    [ -f $n ] && continue
    umask 066 && touch $n
done

#use sysklogd configuration files
if [ -f /etc/syslog.conf ]; then
    mv -f /etc/rsyslog.conf /etc/rsyslog.conf.rpmnew
    mv -f /etc/syslog.conf  /etc/rsyslog.conf
fi
if [ -f /etc/sysconfig/syslog ]; then
    mv -f /etc/sysconfig/rsyslog /etc/sysconfig/rsyslog.rpmnew
    mv -f /etc/sysconfig/syslog  /etc/sysconfig/rsyslog
fi

%preun
%_preun_service rsyslog

%postun
if [ "$1" -ge "1" ]; then
    %{_initrddir}/rsyslog condrestart > /dev/null 2>&1 ||:
fi	

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL NEWS README
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/rsyslog
%{_initrddir}/rsyslog
/sbin/rsyslogd
/sbin/rklogd
/sbin/rfc3195d
%{_mandir}/*/*

%files mysql
%defattr(-,root,root)
%doc plugins/ommysql/createDB.sql plugins/ommysql/contrib/delete_mysql
%{_libdir}/rsyslog/ommysql.so

%files pgsql
%defattr(-,root,root)
%doc plugins/ompgsql/createDB.sql
%{_libdir}/rsyslog/ompgsql.so

%files docs
%defattr(-,root,root)
%doc html_docs/*
