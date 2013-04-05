%define _with_systemd 1
%define _disable_ld_no_undefined 1

%define _libdir /%{_lib}

Summary:	Enhanced system logging and kernel message trapping daemons
Name:		rsyslog
Version:	5.10.1
Release:	1
License:	GPLv3
Group:		System/Kernel and hardware
URL:		http://www.rsyslog.com/
Source0:	http://www.rsyslog.com/files/download/%{name}/%{name}-%{version}.tar.gz
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
Patch0:		rsyslog-5.8.12-systemd.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	java-rpmbuild
BuildRequires:	krb5-devel
BuildRequires:	libdbi-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel >= 4.0
BuildRequires:	net-snmp-devel
BuildRequires:	pkgconfig
BuildRequires:	postgresql-devel
BuildRequires:	relp-devel
BuildRequires:	zlib-devel
%if %{_with_systemd}
BuildRequires:	systemd-units
%endif
Requires:	logrotate
Provides:	syslog-daemon
Requires(post):	/sbin/chkconfig
Requires(post):	coreutils
%if %{_with_systemd}
Requires(post):	systemd-units
Requires(post):	systemd-sysvinit
Requires(preun):	systemd-units
Requires(postun):	systemd-units
%endif
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
# Nothing requires sysklogd
#Provides:	sysklogd = 1.4.5-5
Obsoletes:	sysklogd < 1.5-5
Conflicts:	logrotate < 3.5.2
#Conflicts:	sysklogd
Conflicts:	syslog-ng

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

%package mysql
Summary:	MySQL support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

 o ommysql.so - This is the implementation of the build-in output module for
                MySQL.

%package pgsql
Summary:	PostgreSQL support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

 o ompgsql.so - This is the implementation of the build-in output module for
                PgSQL.

%package gssapi
Summary:	GSS-API support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description gssapi
The rsyslog-gssapi package contains dynamic shared objects that will add
GSS-API support to rsyslog.

 o lmgssutil.so - This is a miscellaneous helper class for gss-api features.
 o imgssapi.so  - This is the implementation of the GSSAPI input module.
 o omgssapi.so  - This is the implementation of the build-in forwarding output
                  module.

%package relp
Summary:	RELP support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description relp
The rsyslog-relp package contains a dynamic shared object that will add
RELP support to rsyslog.

 o imrelp.so - This is the implementation of the RELP input module.
 o omrelp.so - This is the implementation of the RELP output module.

%package dbi
Summary:	Dbi support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description dbi
The rsyslog-dbi package contains a dynamic shared object that will add
dbi driver support to rsyslog.

 o omlibdbi.so - This is the implementation of the dbi output module.

%package snmp
Summary:	SNMP support for rsyslog
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description snmp
The rsyslog-snmp package contains a dynamic shared object that will add
SNMP support to rsyslog.

 o omsnmp.so - This module sends an snmp trap.

%package docs
Summary:	HTML documentation for rsyslog
Group:		System/Kernel and hardware

%description docs
This package contains the HTML documentation for rsyslog.

%prep
%setup -q

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

%patch0 -p1 -b .systemd

%build
%if %mdkver >= 201200
%serverbuild_hardened
%else
%serverbuild
%endif

%configure2_5x \
%if %{_with_systemd}
    --with-systemdsystemunitdir=%{_unitdir} \
%endif
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
%makeinstall_std

install -d -m 755 %{buildroot}%{_initrddir}
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -d -m 755 %{buildroot}%{_sysconfdir}/rsyslog.d

%if !%{_with_systemd}
install -p -m 755 Mandriva/rsyslog.init %{buildroot}%{_initrddir}/rsyslog
%endif
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

# (bor) rsyslog.socket conflicts with syslog.socket for the /dev/log
rm -f %{buildroot}/lib/systemd/system/rsyslog.socket

%post
# The following should really be part of _post_service
[ $1 = 1 -a -x /bin/systemctl ] && /bin/systemctl enable rsyslog.service || :

%_post_service rsyslog

for n in /var/log/{messages,secure,maillog,spooler}; do
    [ -f $n ] && continue
    umask 066 && touch $n
done

# (from Mageia) Handle a quirk of rsyslog installation
if [ -f /etc/systemd/system/multi-user.target.wants/rsyslog.service -a ! -f /etc/systemd/system/syslog.service ]; then
	cp -a /etc/systemd/system/multi-user.target.wants/rsyslog.service /etc/systemd/system/syslog.service
fi

%triggerin -- rsyslog < 5.6.2-3
# enable systemd unit on update
[ -x /bin/systemctl ] && /bin/systemctl enable rsyslog.service || :

%triggerpostun -- rsyslog < 2.0.1-2mdv2008.1
if [ ! -f /etc/syslog.conf ]; then
    # restore syslog.conf
    mv -f /etc/rsyslog.conf /etc/syslog.conf
    mv -f /etc/rsyslog.conf.rpmnew /etc/rsyslog.conf
fi

%triggerun -- rsyslog < 3.0.0
/bin/kill `cat /var/run/rklogd.pid 2> /dev/null` > /dev/null 2>&1 ||:

%triggerun -- sysklogd < 1.5-5
. /etc/sysconfig/syslog
if echo $SYSLOGD_OPTIONS | grep -q -- "-r"
then
	sed -i	-e 's/^\#\$ModLoad imudp.so$/$ModLoad imudp.so/' \
		-e 's/^\#\$UDPServerRun 514$/$UDPServerRun 514/' /etc/rsyslog.d/00_common.conf
fi
if [ -f /var/run/syslogd.pid ]
then
	%{_initrddir}/syslog stop
	%{_initrddir}/rsyslog start
fi

%preun
%_preun_service rsyslog
# The following should really be part of _preun_service
[ $1 = 0 -a -x /bin/systemctl ] && /bin/systemctl disable rsyslog.service || :

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

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README  doc/rsyslog-example.conf
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/syslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/rsyslog
%dir %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_common.conf
%if %{_with_systemd}
%{_unitdir}/rsyslog.service
%else
%{_initrddir}/rsyslog
%endif
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
%{_libdir}/rsyslog/lmstrmsrv.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omruleset.so
%{_mandir}/*/*

%files mysql
%doc plugins/ommysql/createDB.sql plugins/ommysql/contrib/delete_mysql
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_mysql.conf
%{_libdir}/rsyslog/ommysql.so

%files pgsql
%doc plugins/ompgsql/createDB.sql
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_pgsql.conf
%{_libdir}/rsyslog/ompgsql.so

%files gssapi
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_gssapi.conf
%{_libdir}/rsyslog/omgssapi.so
%{_libdir}/rsyslog/imgssapi.so
%{_libdir}/rsyslog/lmgssutil.so

%files relp
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_relp.conf
%{_libdir}/rsyslog/imrelp.so
%{_libdir}/rsyslog/omrelp.so

%files dbi
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_dbi.conf
%{_libdir}/rsyslog/omlibdbi.so

%files snmp
%config(noreplace) %{_sysconfdir}/rsyslog.d/*_snmp.conf
%{_libdir}/rsyslog/omsnmp.so

%files docs
%doc html_docs/*


%changelog
* Sun Jul 08 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 5.8.12-1
+ Revision: 808489
- rediff patch 0 drop ExecStartPre stuff
- handle a quirk of rsyslog installation

* Mon May 28 2012 Alexander Khrukin <akhrukin@mandriva.org> 5.8.11-1
+ Revision: 800922
- version update 5.8.11

* Sat Apr 07 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 5.8.10-1
+ Revision: 789669
- update to new version 5.8.10

* Thu Mar 22 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 5.8.9-1
+ Revision: 786209
- update to new version 5.8.9

* Tue Feb 14 2012 Alexander Khrukin <akhrukin@mandriva.org> 5.8.7-1
+ Revision: 774074
- version update 5.8.7

* Sun Jan 15 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 5.8.6-2
+ Revision: 761634
- do not install initscripts files when systemd support is enabled

* Sat Jan 07 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 5.8.6-1
+ Revision: 758620
- update to new version 5.8.6

* Tue Oct 11 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 5.8.5-2
+ Revision: 704344
- Patch0: fix systemd service file
- use %%serverbuild_hardened for mdv2012
- spec file clean

* Mon Sep 05 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 5.8.5-1
+ Revision: 698261
- update to new version 5.8.5

* Mon Jul 18 2011 Oden Eriksson <oeriksson@mandriva.com> 5.8.2-2
+ Revision: 690303
- rebuilt against new net-snmp libs

* Sun Jun 26 2011 Oden Eriksson <oeriksson@mandriva.com> 5.8.2-1
+ Revision: 687263
- 5.8.2

* Wed Jun 08 2011 Oden Eriksson <oeriksson@mandriva.com> 5.8.1-1
+ Revision: 683152
- 5.8.1

* Sun Apr 17 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 5.8.0-1
+ Revision: 654464
- update to new version 5.8.0
- drop systemd patches, because they were merged by upstream

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 5.6.2-6
+ Revision: 645758
- relink against libmysqlclient.so.18

* Thu Mar 10 2011 Andrey Borzenkov <arvidjaar@mandriva.org> 5.6.2-5
+ Revision: 643652
- P1,2: proper support for systemd socket activation

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 5.6.2-4
+ Revision: 640279
- rebuild to obsolete old packages

* Sun Jan 23 2011 Andrey Borzenkov <arvidjaar@mandriva.org> 5.6.2-3
+ Revision: 632437
- do not install rsyslog.socket, it conflicts with syslog.socket
- enable systemd unit on install/update
- P0: rsyslog.service should be after local-fs.target

* Fri Jan 14 2011 Eugeni Dodonov <eugeni@mandriva.com> 5.6.2-2
+ Revision: 631095
- Add systemd support.

* Wed Dec 29 2010 Eugeni Dodonov <eugeni@mandriva.com> 5.6.2-1mdv2011.0
+ Revision: 626005
- Updated to 5.6.2.

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 4.6.5-2mdv2011.0
+ Revision: 614429
- stupid build system
- 4.6.5

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 4.6.4-3mdv2011.0
+ Revision: 609662
- rebuilt against new libdbi

* Tue Oct 12 2010 Funda Wang <fwang@mandriva.org> 4.6.4-2mdv2011.0
+ Revision: 585014
- rebuild

* Sat Aug 28 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.4-1mdv2011.0
+ Revision: 573964
- update to new version 4.6.4

* Sat Jul 10 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.3-1mdv2011.0
+ Revision: 550152
- update to new version 4.6.3

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 4.6.2-3mdv2010.1
+ Revision: 539599
- rebuild so that shared libraries are properly stripped again

* Thu Apr 22 2010 Pascal Terjan <pterjan@mandriva.org> 4.6.2-2mdv2010.1
+ Revision: 537780
- Write data to file at the end of each transaction (#58468)

* Mon Mar 29 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.2-1mdv2010.1
+ Revision: 528659
- update to new version 4.6.2

* Thu Mar 04 2010 Frederic Crozat <fcrozat@mandriva.com> 4.6.1-1mdv2010.1
+ Revision: 514084
- Release 4.6.1
- enable back serverbuild, fixed in 4.6.1 (thanks to Yann Droneaud)

* Tue Mar 02 2010 Frederic Crozat <fcrozat@mandriva.com> 4.6.0-2mdv2010.1
+ Revision: 513597
- temporary disable full stack protection, causes crashes (upstream bug http://bugzilla.adiscon.com/show_bug.cgi?id=182)

* Wed Feb 24 2010 Frederik Himpe <fhimpe@mandriva.org> 4.6.0-1mdv2010.1
+ Revision: 510818
- Update to new version 4.6.0
- Remove old, unneeded Fedora patch

* Wed Feb 17 2010 Oden Eriksson <oeriksson@mandriva.com> 4.4.2-6mdv2010.1
+ Revision: 507043
- rebuild

* Wed Nov 25 2009 Frederik Himpe <fhimpe@mandriva.org> 4.4.2-5mdv2010.1
+ Revision: 470110
- Rebuild for main
- Preserve remote syslog server setting from sysklogd

* Fri Nov 20 2009 Frederik Himpe <fhimpe@mandriva.org> 4.4.2-3mdv2010.1
+ Revision: 467753
- Obsolete sysklogd
- Don't try to migrate /etc/sysconfig/syslog to /etc/sysconfig/rsyslog,
  they are totally different
- Start rsyslog on upgrade from sysklogd if sysklogd was running

* Thu Oct 15 2009 Oden Eriksson <oeriksson@mandriva.com> 4.4.2-2mdv2010.0
+ Revision: 457696
- rebuild

* Fri Oct 09 2009 Frederik Himpe <fhimpe@mandriva.org> 4.4.2-1mdv2010.0
+ Revision: 456417
- update to new version 4.4.2

* Thu Sep 10 2009 Frederik Himpe <fhimpe@mandriva.org> 4.4.1-2mdv2010.0
+ Revision: 437130
- Use -c4 option to prevent warning about deprecated configuration

* Wed Sep 02 2009 Frederik Himpe <fhimpe@mandriva.org> 4.4.1-1mdv2010.0
+ Revision: 425455
- update to new version 4.4.1

* Fri Aug 21 2009 Frederik Himpe <fhimpe@mandriva.org> 4.4.0-1mdv2010.0
+ Revision: 419392
- Fix BuildRequires
- Update to new version 4.4.0

* Tue Jun 23 2009 Frederik Himpe <fhimpe@mandriva.org> 4.2.0-1mdv2010.0
+ Revision: 388745
- Update to new version 4.20, first stable, production ready release in v4
  branch
- Remove imudp patch included upstream

* Sat May 16 2009 Frederik Himpe <fhimpe@mandriva.org> 3.22.0-1mdv2010.0
+ Revision: 376421
- Sync file list in logrotate configuration with sysklogd package:
  so that all log files are rotated correctly
- Update to new stable version 3.22.0
- Remove patch integrated upstream
- Add upstream patch (via Debian) which fixes a segfault in imudp
  when multiple udp listeners are configured

* Thu Mar 26 2009 Frederik Himpe <fhimpe@mandriva.org> 3.21.10-3mdv2009.1
+ Revision: 361489
- Add Fedora patch fixing RH bug #485937
- Sync init script LSB headers with Fedora's: now rsyslog does not
  depend anymore on network which will speed up the boot procedure a lot
- Conflict with sysklogd and syslog-ng: as they do the same thing, it makes
  no sense having them installed together. Also this caused duplication in
  the logrotation configuration, completely breaking logrotate (bug #39426)
- Add some missing log files to logrotate configuration

* Thu Feb 05 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 3.21.10-2mdv2009.1
+ Revision: 337995
- Add support for runlevel 7

* Tue Feb 03 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 3.21.10-1mdv2009.1
+ Revision: 336948
- update to new version 3.21.10

* Mon Jan 19 2009 Jérôme Soyer <saispo@mandriva.org> 3.20.3-1mdv2009.1
+ Revision: 331181
- New upstream release

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 3.20.2-1mdv2009.1
+ Revision: 311491
- 3.20.2
- 3.20.1

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 3.20.0-2mdv2009.1
+ Revision: 311317
- rebuilt against mysql-5.1.30 libs

* Thu Nov 06 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 3.20.0-1mdv2009.1
+ Revision: 300325
- update to new version 3.20.0

* Tue Oct 21 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 3.19.12-1mdv2009.1
+ Revision: 296223
- fix file list
- provide logrotate conf file
- update to new version 3.19.12

* Fri Oct 10 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 3.18.5-1mdv2009.1
+ Revision: 291516
- update to new version 3.18.5
- update to new version 3.18.4

* Mon Aug 18 2008 Frederik Himpe <fhimpe@mandriva.org> 3.18.3-1mdv2009.0
+ Revision: 273386
- update to new version 3.18.3

* Wed Aug 13 2008 Frederik Himpe <fhimpe@mandriva.org> 3.18.2-1mdv2009.0
+ Revision: 271579
- update to new version 3.18.2

* Tue Jul 22 2008 Funda Wang <fwang@mandriva.org> 3.18.1-1mdv2009.0
+ Revision: 239940
- New version 3.18.1

* Sat Jul 19 2008 Oden Eriksson <oeriksson@mandriva.com> 3.18.0-1mdv2009.0
+ Revision: 238712
- added the mail plugin feature
- added the sysklogd.conf file from the sysklogd package

* Sat Jul 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 3.18.0-0.1mdv2009.0
+ Revision: 234124
- Patch0: rediff
- update to new version 3.18.0
- new license policy
- do not package COPYING and INSTALL files

* Sat May 03 2008 Oden Eriksson <oeriksson@mandriva.com> 3.16.1-0.1mdv2009.0
+ Revision: 200689
- 3.16.1
- sync with rsyslog-3.14.1-2.fc9.src.rpm
- fix order in S3
- added S4-S10 to take advantage of the new modular design
- fix descriptions
- added the relp, dbi and snmp sub packages
- fix %%post and %%preun script for the modules
- put the modules in /%%{_lib}/rsyslog/ to avoid future problems
  if /usr for some reason should not be mounted at boot...

* Mon Jan 28 2008 Olivier Blin <blino@mandriva.org> 2.0.1-2mdv2008.1
+ Revision: 159377
- create /etc/rsyslog.d and include /etc/rsyslog.d/*.conf from rsyslog.conf
- restore syslog.conf on upgrade of previous rsyslog package
- include syslog.conf in rsyslog.conf instead of moving the file, to ease cohabitation of sysklogd and rsyslog packages
- do not remove original /etc/sysconfig/syslog
- migrate sysklogd configuration files in initial installation only

* Thu Jan 24 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-1mdv2008.1
+ Revision: 157600
- 2.0.1 (3.x.x is the unstable branch)

  + Olivier Blin <blino@mandriva.org>
    - 3.10.2

* Wed Jan 02 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-1mdv2008.1
+ Revision: 140614
- 2.0.0

* Sat Dec 29 2007 Oden Eriksson <oeriksson@mandriva.com> 1.21.2-1mdv2008.1
+ Revision: 139317
- 1.21.2

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1.21.1-1mdv2008.1
+ Revision: 137430
- 1.21.1

* Wed Dec 19 2007 Oden Eriksson <oeriksson@mandriva.com> 1.21.0-1mdv2008.1
+ Revision: 134359
- 1.21.0
- enable all features

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Dec 13 2007 Oden Eriksson <oeriksson@mandriva.com> 1.20.1-1mdv2008.1
+ Revision: 119281
- 1.20.1

* Fri Dec 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1.20.0-1mdv2008.1
+ Revision: 116322
- 1.20.0

* Mon Dec 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1.19.12-1mdv2008.1
+ Revision: 114551
- 1.19.12

* Thu Nov 22 2007 Oden Eriksson <oeriksson@mandriva.com> 1.19.10-1mdv2008.1
+ Revision: 111227
- import rsyslog


* Thu Nov 22 2007 Oden Eriksson <oeriksson@mandriva.com> 1.19.10-1mdv2008.1
- initial Mandriva package (fedora import)

* Wed Oct 03 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.6-3
- remove NUL character from recieved messages

* Tue Sep 25 2007 Tomas Heinrich <theinric@redhat.com> 1.19.6-2
- fix message suppression (303341)

* Tue Sep 25 2007 Tomas Heinrich <theinric@redhat.com> 1.19.6-1
- upstream bugfix release

* Tue Aug 28 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.2-1
- upstream bugfix release
- support for negative app selector, patch from 
  theinric@redhat.com

* Fri Aug 17 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.0-1
- new upstream release with MySQL support(as plugin)

* Wed Aug 08 2007 Peter Vrabec <pvrabec@redhat.com> 1.18.1-1
- upstream bugfix release

* Mon Aug 06 2007 Peter Vrabec <pvrabec@redhat.com> 1.18.0-1
- new upstream release

* Thu Aug 02 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.6-1
- upstream bugfix release

* Mon Jul 30 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.5-1
- upstream bugfix release
- fix typo in provides 

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 1.17.2-4
- rebuild for toolchain bug

* Tue Jul 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.2-3
- take care of sysklogd configuration files in %%post

* Tue Jul 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.2-2
- use EVR in provides/obsoletes sysklogd

* Mon Jul 23 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.2-1
- upstream bug fix release

* Fri Jul 20 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.1-1
- upstream bug fix release
- include html docs (#248712)
- make "-r" option compatible with sysklogd config (248982)

* Tue Jul 17 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.0-1
- feature rich upstream release

* Thu Jul 12 2007 Peter Vrabec <pvrabec@redhat.com> 1.15.1-2
- use obsoletes and hadle old config files

* Wed Jul 11 2007 Peter Vrabec <pvrabec@redhat.com> 1.15.1-1
- new upstream bugfix release

* Tue Jul 10 2007 Peter Vrabec <pvrabec@redhat.com> 1.15.0-1
- new upstream release introduce capability to generate output 
  file names based on templates

* Tue Jul 03 2007 Peter Vrabec <pvrabec@redhat.com> 1.14.2-1
- new upstream bugfix release

* Mon Jul 02 2007 Peter Vrabec <pvrabec@redhat.com> 1.14.1-1
- new upstream release with IPv6 support

* Tue Jun 26 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.5-3
- add BuildRequires for  zlib compression feature

* Mon Jun 25 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.5-2
- some spec file adjustments.
- fix syslog init script error codes (#245330)

* Fri Jun 22 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.5-1
- new upstream release

* Fri Jun 22 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.4-2
- some spec file adjustments.

* Mon Jun 18 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.4-1
- upgrade to new upstream release

* Wed Jun 13 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.2-2
- DB support off

* Tue Jun 12 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.2-1
- new upstream release based on redhat patch

* Fri Jun 08 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.1-2
- rsyslog package provides its own kernel log. daemon (rklogd)

* Mon Jun 04 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.1-1
- Initial rpm build
