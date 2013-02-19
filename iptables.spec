# because the modules are not libtool aware
%define _disable_ld_no_undefined 1

%define major 7
%define libname %mklibname iptables %{major}
%define develname %mklibname -d iptables

%define iptc_major 0
%define iptc_libname %mklibname iptc %{iptc_major}
%define iptc_develname %mklibname -d iptc

%define ipq_major 0
%define ipq_libname %mklibname ipq %{ipq_major}
%define ipq_develname %mklibname -d ipq

%define ip4tc_major 0
%define ip4tc_libname %mklibname ip4tc %{ip4tc_major}
%define ip4tc_develname %mklibname -d ip4tc

%define ip6tc_major 0
%define ip6tc_libname %mklibname ip6tc %{ip6tc_major}
%define ip6tc_develname %mklibname -d ip6tc

# install init scripts to /usr/libexec with systemd
%define script_path %{_libexecdir}

Summary:	Tools for managing Linux kernel packet filtering capabilities
Name:		iptables
Version:	1.4.17
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://netfilter.org/
Source0:	http://netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
Source2:	iptables.init
Source3:	ip6tables.init
Source4:	iptables.config
Source5:	ip6tables.config
Source6:	iptables.service
# S100 and up used to be in the added patches
Source100:	libipt_IMQ.c
Source101:	libipt_IFWLOG.c
# (oe) psd comes from iptables-1.3.7, was removed in iptables-1.3.8
Source102:	libipt_psd.c
Source103:	libipt_psd.man
Patch0:		iptables-1.2.8-libiptc.h.patch

Patch100:	iptables-imq.diff
Patch101:	iptables-IFWLOG_extension.diff
Patch102:	iptables-psd.diff
Patch103:	iptables-1.4.17-fix-linking.patch
Provides:	userspace-ipfilter
BuildRequires:	nfnetlink-devel
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Obsoletes:	%{name} < 1.4.3.2
Obsoletes:	%{name}-ipv6 < 1.4.1.1-0.5
Provides:	%{name}-ipv6 = %{version}

%description
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

Install iptables if you need to set up firewalling for your network.

%package -n %{libname}
Summary:	Shared iptables library
Group:		System/Libraries
Conflicts:	%mklibname %{name} 1
Conflicts:	%mklibname %{name} 4
Conflicts:	%mklibname %{name} 5

%description -n	%{libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the shared iptables library.

%package -n %{develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{libname} = %{version}-%{release}
Provides:	iptables-devel = %{version}
Obsoletes:	iptables-devel < 1.4.2

%description -n	%{develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the static iptables library.

# ipq
%package -n %{ipq_libname}
Summary:	Shared iptables library
Group:		System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n	%{ipq_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the ipq library.

%package -n %{ipq_develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{ipq_libname} = %{version}-%{release}
Requires:	%{ipq_develname} = %{version}-%{release}
Provides:	iptables-ipq-devel = %{version}

%description -n	%{ipq_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the ipq library.

# iptc
%package -n %{iptc_libname}
Summary:	Shared iptables library
Group:		System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n	%{iptc_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IPTC library.

%package -n %{iptc_develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{iptc_libname} = %{version}-%{release}
Requires:	%{iptc_develname} = %{version}-%{release}
Provides:	iptables-iptc-devel = %{version}

%description -n	%{iptc_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IPTC library.

# ip4tc
%package -n %{ip4tc_libname}
Summary:	Shared iptables library
Group:		System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n	%{ip4tc_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IP4TC library.

%package -n	%{ip4tc_develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{ip4tc_libname} = %{version}-%{release}
Requires:	%{iptc_develname} = %{version}-%{release}
Provides:	iptables-ip4tc-devel = %{version}

%description -n	%{ip4tc_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the development files for IPTC library.

# ip6tc
%package -n %{ip6tc_libname}
Summary:	Shared iptables library
Group:		System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n	%{ip6tc_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IP6TC library.

%package -n %{ip6tc_develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{ip6tc_libname} = %{version}-%{release}
Provides:	iptables-ip6tc-devel = %{version}

%description -n	%{ip6tc_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the development files for IP6TC library.

%prep

%setup -q

cp %{SOURCE2} iptables.init
cp %{SOURCE3} ip6tables.init
cp %{SOURCE4} iptables.sample
cp %{SOURCE5} ip6tables.sample

# fix libdir
perl -pi -e "s|\@lib\@|%{_lib}|g" iptables.init

# extensions
#install -m0644 %{SOURCE100} extensions/ <- it needs ipt_IMQ.h and we don't have it anymore ?!
#install -m0644 %{SOURCE101} extensions/
# (oe) psd comes from iptables-1.3.7, was removed in iptables-1.3.8
install -m0644 %{SOURCE102} extensions/
install -m0644 %{SOURCE103} extensions/

%patch0 -p1 -b .libiptc
%patch100 -p0
#patch101 -p0
%patch102 -p0
%patch103 -p1

find . -type f | xargs perl -pi -e "s,/usr/local,%{_prefix},g"

# don't run /sbin/ldconfig
perl -pi -e "s|/sbin/ldconfig|/bin/true|g" Makefile*

%build
export LIBS="-ldl"

%serverbuild

autoreconf -fi

export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export FFLAGS="$FFLAGS -fPIC"

%configure2_5x \
    --bindir=/sbin \
    --sbindir=/sbin \
    --libdir=/%{_lib} \
    --libexecdir=/%{_lib} \
    --enable-devel \
    --enable-libipq \
    --enable-ipv4 \
    --enable-ipv6 \
    --with-ksource=%{_prefix}/src/linux \
    --with-xtlibdir=/%{_lib}/iptables

%make

%install

%makeinstall_std

# (oe) this in conjunction with the mandriva initscript will make it possible
# to use development versions of the netfilter modules and with different
# api:s. (according to blino)
install -d %{buildroot}/%{_lib}/iptables.d
mv %{buildroot}/%{_lib}/iptables %{buildroot}/%{_lib}/iptables.d/linux-2.6-main

# pkgconfig files
mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}/

# header development files
install -d %{buildroot}%{_includedir}/{libipq,libiptc,libipulog}
install -m0644 include/libipq/*.h %{buildroot}%{_includedir}/libipq/
install -m0644 include/libiptc/*.h %{buildroot}%{_includedir}/libiptc/
install -m0644 include/libipulog/*.h %{buildroot}%{_includedir}/libipulog/

# iptables and netfilter development files
install -d %{buildroot}%{_includedir}/net/netfilter/
install -d %{buildroot}%{_includedir}/iptables
install -m0644 include/net/netfilter/*.h %{buildroot}%{_includedir}/net/netfilter/
install -m0644 include/ip*tables.h %{buildroot}%{_includedir}/
install -m0644 include/iptables/internal.h %{buildroot}%{_includedir}/iptables

#Intird not need. TODO drop it!
#install -d %{buildroot}%{_initrddir}
#install -m0755 iptables.init %{buildroot}%{_initrddir}/iptables
#install -m0755 ip6tables.init %{buildroot}%{_initrddir}/ip6tables

# install compatible excutable (since 1.4.11)
ln -sf xtables-multi %{buildroot}/sbin/iptables-multi
ln -sf xtables-multi %{buildroot}/sbin/ip6tables-multi

# nuke *.la and static files
rm -f %{buildroot}/%{_lib}/*.*a

# (cg) NB the name "iptables.init" is important. The dracut usrmove convertfs
# module will avoid a post-merge conflict by renaming the files to match this
# naming convension. If this package is updated to change the names below,
# you should also take care to update dracut and the convertfs module accordingly.
install -d %{buildroot}%{script_path}
install -m0755 iptables.init %{buildroot}%{script_path}/
install -m0755 ip6tables.init %{buildroot}%{script_path}/

# install systemd service files
install -d -m 755 %{buildroot}/lib/systemd/system
install -c -m 644 %{SOURCE6} %{buildroot}/lib/systemd/system/
sed -e 's;iptables;ip6tables;g' -e 's;IPv4;IPv6;g' < %{SOURCE6} > ip6tables.service
install -c -m 644 ip6tables.service %{buildroot}/lib/systemd/system/
sed -i 's!@LIBDIR@!%{_libdir}!' %{buildroot}/lib/systemd/system/ip6tables.service
sed -i 's!@LIBDIR@!%{_libdir}!' %{buildroot}/lib/systemd/system/iptables.service

%post
%_post_service iptables
%_post_service ip6tables
/sbin/service iptables check

%preun
%_preun_service iptables
%_preun_service ip6tables

%triggerun -- iptables < 1.4.12.1
# Autostart
/bin/systemctl --no-reload enable iptables.service >/dev/null 2>&1 ||:

# Delete from sysv management, try to restart service
/sbin/chkconfig --del iptables >/dev/null 2>&1 || :
/bin/systemctl try-restart iptables.service >/dev/null 2>&1 || :

# Autostart
/bin/systemctl --no-reload enable ip6tables.service >/dev/null 2>&1 ||:

# Delete from sysv management, try to restart service
/sbin/chkconfig --del ip6tables >/dev/null 2>&1 || :
/bin/systemctl try-restart ip6tables.service >/dev/null 2>&1 || :

%files
%doc INSTALL INCOMPATIBILITIES iptables.sample ip6tables.sample
%attr(0755,root,root) %{script_path}/ip*
/lib/systemd/system/iptables.service
/lib/systemd/system/ip6tables.service
/sbin/iptables
/sbin/iptables-restore
/sbin/iptables-save
/sbin/iptables-xml
/sbin/iptables-multi
/sbin/ip6tables-multi
/sbin/xtables-multi
/sbin/nfnl_osf
# ipv6
/sbin/ip6tables
/sbin/ip6tables-restore
/sbin/ip6tables-save
%dir /%{_lib}/iptables.d
%dir /%{_lib}/iptables.d/linux-2.6-main
/%{_lib}/iptables.d/linux-2.6-main/libipt_ah.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_CLUSTERIP.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_DNAT.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_ECN.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_icmp.so
#/%{_lib}/iptables.d/linux-2.6-main/libipt_IFWLOG.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_LOG.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_MASQUERADE.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_MIRROR.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_NETMAP.so
#/%{_lib}/iptables.d/linux-2.6-main/libipt_psd.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_realm.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_REDIRECT.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_REJECT.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_SAME.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_SNAT.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_ttl.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_TTL.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_ULOG.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_unclean.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_addrtype.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_AUDIT.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CHECKSUM.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CLASSIFY.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_cluster.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_comment.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_connbytes.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_connlimit.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_connmark.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CONNMARK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CONNSECMARK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_conntrack.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_cpu.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CT.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_dccp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_devgroup.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_dscp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_DSCP.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_ecn.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_esp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_hashlimit.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_helper.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_HMARK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_IDLETIMER.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_iprange.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_ipvs.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_LED.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_length.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_limit.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_mac.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_mark.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_MARK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_multiport.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_nfacct.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_NFLOG.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_NFQUEUE.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_NOTRACK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_osf.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_owner.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_physdev.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_pkttype.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_policy.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_quota.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_rateest.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_RATEEST.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_recent.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_rpfilter.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_sctp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_SECMARK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_set.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_SET.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_socket.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_standard.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_state.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_statistic.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_string.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_tcpmss.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TCPMSS.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TCPOPTSTRIP.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_tcp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TEE.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_time.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_tos.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TOS.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TPROXY.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TRACE.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_u32.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_udp.so
%{_mandir}/*/iptables*
%{_datadir}/xtables/pf.os
# ipv6
/%{_lib}/iptables.d/linux-2.6-main/libip6t_ah.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_dst.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_eui64.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_frag.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_hbh.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_hl.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_HL.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_icmp6.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_ipv6header.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_LOG.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_mh.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_REJECT.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_rt.so
%{_mandir}/*/ip6tables*

%files -n %{libname}
/%{_lib}/libxtables.so.%{major}*

%files -n %{develname}
%{_includedir}/*.h
%dir %{_includedir}/libipulog
%{_includedir}/libipulog/*.h
%{_includedir}/iptables/*.h
%{_includedir}/net/netfilter/*.h
/%{_lib}/libxtables.so
%{_libdir}/pkgconfig/xtables.pc

%files -n %{ipq_libname}
/%{_lib}/libipq.so.*

%files -n %{ipq_develname}
%{_includedir}/libipq/*.h
%dir %{_includedir}/libipq
/%{_lib}/libipq.so
%{_mandir}/man3/*ipq*
%{_libdir}/pkgconfig/libipq.pc

%files -n %{iptc_libname}
/%{_lib}/libiptc.so.*

%files -n %{iptc_develname}
%{_includedir}/libiptc/*.h
%dir %{_includedir}/libiptc
/%{_lib}/libiptc.so
%{_libdir}/pkgconfig/libip*tc.pc

%files -n %{ip4tc_libname}
/%{_lib}/libip4tc.so.*

%files -n %{ip4tc_develname}
/%{_lib}/libip4tc.so

%files -n %{ip6tc_libname}
/%{_lib}/libip6tc.so.*

%files -n %{ip6tc_develname}
/%{_lib}/libip6tc.so


%changelog
* Mon Dec 3 2012 akdengi <akdengi> 1.4.15-2
- drop SysVinit service. Add systemd service support.

* Fri Jul 20 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.14-2
+ Revision: 810338
- obsolete old majors 4 and 5

* Mon May 28 2012 Oden Eriksson <oeriksson@mandriva.com> 1.4.14-1
+ Revision: 800898
- 1.4.14

* Fri Mar 30 2012 Oden Eriksson <oeriksson@mandriva.com> 1.4.13-1
+ Revision: 788404
- 1.4.13

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.4.12.2-2
+ Revision: 760932
- P1: fix build with linux 3.2 (tmb)

* Tue Jan 10 2012 Oden Eriksson <oeriksson@mandriva.com> 1.4.12.2-1
+ Revision: 759269
- various cleanups
- slight cleanup
- 1.4.12.2
- the iptables-1.4.12-conntract.patch patch was added upstream
- sync with mageia

* Tue Oct 11 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.12.1-1
+ Revision: 704311
- enable support for libnfnetlink on mdv2012
- update file list
- update to new version 1.4.12.1

* Fri Aug 19 2011 Александр Казанцев <kazancas@mandriva.org> 1.4.12-2
+ Revision: 695829
- fix bug with 'iptables-restore v1.4.12: conntrack rev 2 does not support port ranges'

* Wed Jul 27 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.12-1
+ Revision: 691915
- /sbin/nfnl_osf and /usr/share/xtables/pf.os is not installed for some reason...
- 1.4.12

* Thu Jun 09 2011 Funda Wang <fwang@mandriva.org> 1.4.11.1-1
+ Revision: 683329
- update to new version 1.4.11.1

* Fri May 27 2011 Funda Wang <fwang@mandriva.org> 1.4.11-2
+ Revision: 679378
- add compatible executable symlink

* Fri May 27 2011 Funda Wang <fwang@mandriva.org> 1.4.11-1
+ Revision: 679238
- update file list
- update libmajor
- update file list
- update to new version 1.4.11

* Tue May 24 2011 Funda Wang <fwang@mandriva.org> 1.4.10-3
+ Revision: 678001
- move *.so into /lib (bug#63356)

* Sun May 01 2011 Funda Wang <fwang@mandriva.org> 1.4.10-2
+ Revision: 661135
- fix provides of ip4tc-devel

* Sat Oct 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.10-1mnb2
+ Revision: 590455
- 1.4.10

* Thu Jul 15 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.8-1mnb2
+ Revision: 553702
- do not enable nfnetlink support for now
- update to new version 1.4.8
- fix url for Source0
- update file list

* Mon Mar 08 2010 Eugeni Dodonov <eugeni@mandriva.com> 1.4.7-2mnb2
+ Revision: 515788
- Install missing devel files.

* Tue Mar 02 2010 Eugeni Dodonov <eugeni@mandriva.com> 1.4.7-1mnb2
+ Revision: 513519
- Updated to 1.4.7.
  Added IPQ library and its documentation.

* Thu Dec 10 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.4.6-1mnb2
+ Revision: 475942
- Updated to 1.4.6

* Wed Sep 16 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.4.5-2mnb2
+ Revision: 443613
- Updated to 1.4.5.
  Packaged libip4tc and libip6tc.

* Thu Jun 18 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.4.4-2mnb2
+ Revision: 387180
- Resolve conflict over libiptables-devel and libiptc-devel packages.

* Thu Jun 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-1mnb2
+ Revision: 386939
- 1.4.4

* Thu Jun 04 2009 Gustavo De Nardin <gustavodn@mandriva.com> 1.4.3.2-3mnb2
+ Revision: 382860
- fixed obsoletes macro call

* Tue Jun 02 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.4.3.2-2mnb2
+ Revision: 382223
- Adding Obsolete to prevent conflict between iptc and old iptables.

* Fri May 29 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.4.3.2-1mnb2
+ Revision: 381113
- Splitting libiptc to a separate package (it has a different major).
- Updated to 1.4.3.2.
  New major.

* Mon Mar 30 2009 Luiz Fernando Capitulino <lcapitulino@mandriva.com> 1.4.3.1-3mnb2
+ Revision: 362745
- bump release
- libipt_IFWLOG: Update to latest netfilter's API
- libipt_psd: Update to latest netfilter's API

* Thu Mar 26 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.3.1-2mnb2
+ Revision: 361305
- 1.4.3.1 (thanks fhimpe)
- 1.4.3
- drop redundant patches and other stuff (P2,P3,P4,P5)
- new major (1)

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-2mnb2
+ Revision: 316266
- rediffed one fuzzy patch
- fix build with -Werror=format-security

* Thu Oct 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-1mnb2
+ Revision: 296770
- 1.4.2
- drop redundant patches (P1,P5)
- libfifiction adaptations

* Tue Sep 23 2008 Olivier Blin <blino@mandriva.org> 1.4.1.1-4mnb2
+ Revision: 287357
- create /lib/iptables if it does not exist
- always run iptables check on post (real fix for #42579)

* Mon Sep 22 2008 Frederic Crozat <fcrozat@mandriva.com> 1.4.1.1-3mnb2
+ Revision: 286533
- Update source1 to no do useless things when it is not needed (improve boot time)

* Fri Sep 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.1.1-2mnb2
+ Revision: 285907
- rebuild
- sync with iptables-1.4.1.1-2.fc10.src.rpm

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.1.1-1mnb2
+ Revision: 234896
- rebuild

* Sat Jul 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.1.1-0.6mnb2
+ Revision: 234172
- revert last commit only with paths for iptables

* Sat Jul 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.1.1-0.5mnb2
+ Revision: 234155
- merge subpackage iptables-ipv6 into main package
- pass with xtlibdir a real iptables directory
- spec file clean

  + Luiz Fernando Capitulino <lcapitulino@mandriva.com>
    - Remove kernel-source BuildRequires
      kernel-headers package has been fixed to export the needed
      headers, iptables does not have to use headers directly from
      the kernel sources anymore.
    - libipt_psd: convert from target to match (again) and make psd
      to work again.

* Mon Jun 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.1.1-0.4mnb2
+ Revision: 227990
- fix build (duh!)
- make it work as it used to. this change in conjunction with the mandriva
  initscript will make it possible to use development versions of the netfilter
  modules and with different api:s. (according to blino)

* Sun Jun 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.1.1-0.3mnb2
+ Revision: 227943
- rebuild
- added -fPIC because it's needed by packages linking against the devel libs

* Sat Jun 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.1.1-0.1mnb2
+ Revision: 227740
- 1.4.1.1 (uses autoconf now)
- put the modules in /%%{_lib}/iptables.d/ though default now is
  LIBEXECDIR/xtables, but we used to have it in /lib/iptables.d/
  NOTE: third party modules has to be adjusted!
- adjust /lib/ in iptables.init
- tried to port S100,S101,S102 to the new api, but the psd one
  needs some work again (blino?,lcapitulino?)
- had to use _disable_ld_no_undefined due to build problems in
  libxt_comment.c and libxt_CLASSIFY.c
- again...
- fix a small error
- added some props

* Thu Mar 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-1mnb1
+ Revision: 181032
- bump release

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-0.9mnb1
+ Revision: 178419
- added fixes to psd and IFWLOG by lcapitulino to hopefully fix #37158

* Sun Feb 24 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-0.8mnb1
+ Revision: 174357
- pass -fPIC to the CFLAGS

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.4.0-0.7mnb1
+ Revision: 170652
- replace %%mkrel with %%manbo_mkrel for Manbo Core 1

* Sun Feb 10 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.0-0.7mdv2008.1
+ Revision: 164942
- fix broken symlink

* Sat Feb 09 2008 Colin Guthrie <cguthrie@mandriva.org> 1.4.0-0.6mdv2008.1
+ Revision: 164496
- Work around the removal of the kernel headers tarball.

* Sat Feb 09 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.0-0.5mdv2008.1
+ Revision: 164392
- remove source 5, a kernel headers which are now a system wide standalone package
- devel package requires kernel-headers
- new license policy

  + Oden Eriksson <oeriksson@mandriva.com>
    - remove the grsecurity stuff, we don't have it anyway

* Thu Jan 24 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-0.4mdv2008.1
+ Revision: 157396
- enable the build of the IFWLOG extension now that kernel-source-latest is fixed (#37082)

* Tue Jan 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-0.3mdv2008.1
+ Revision: 156462
- added most of the added extensions as sources instead
- dropped unmaintained extensions

  + Thierry Vignaud <tv@mandriva.org>
    - drop kernel-2.4.x versionning

* Tue Jan 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-0.2mdv2008.1
+ Revision: 156206
- fix the %%serverbuild stuff again...

* Tue Jan 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-0.1mdv2008.1
+ Revision: 156091
- 1.4.0
- dropped obsolete patches; P9
- the IFWLOG extension needs rework, it won't build (P6)
- rediffed patches; P1,P7
- rediff P8, but don't apply it just yet
- really use the %%serverbuild rpm macro
- add P10 (psd support)

  + Thierry Vignaud <tv@mandriva.org>
    - remove useless kernel require
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Oct 15 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3.8-1mdv2008.1
+ Revision: 98487
- 1.3.8
- rediffed P1,P7,P9
- added more static development and header files

  + Thierry Vignaud <tv@mandriva.org>
    - kill file require on perl-base
    - buildrequires obsoletes buildprereq

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - new version

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 1.3.7-2mdv2008.0
+ Revision: 36175
- rebuild with correct optflags

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add missing ipv6 extensions: rt ipv6header hbh frag dst ah
    - reenable IPV4OPTSSTRIP extension
    - enable building of CLUSTERIP module
    - fix install of libiptc.a
    - add iptables-xml
    - new version: 1.3.7
    - regenerate P1
    - cleanups


* Tue Aug 08 2006 Emmanuel Andry <eandry@mandriva.org> 1.3.5-3mdv2007.0
- rebuild for x86_64

* Mon Aug 07 2006 Olivier Blin <blino@mandriva.com> 1.3.5-2mdv2007.0
- use linux-2.6-pom (patch-o-matic) as kernel headers basename (#24147)

* Fri Aug 04 2006 Samir Bellabes <sbellabes@n4.mandriva.com> 1.3.5-1mdv2007.0
- new release
- desactive patch ipp2p
- new kernel-headers

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 1.3.3-6mdk
- convert parallel init to LSB
- mkrel
- Requires(post), Requires(preun)
- remove requires-on-release

* Sat Dec 31 2005 Couriousous <couriousous@mandriva.org> 1.3.3-5mdk
- Add parallel init info

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.3.3-4mdk
- Rebuild

* Wed Aug 10 2005 Samir Bellabes <sbellabes@mandriva.com> 1.3.3-3mdk
- rebuild with new kernel headers 2.6.12-9mdk.

* Wed Aug 03 2005 Samir Bellabes <sbellabes@mandriva.com> 1.3.3-2mdk
- IFWLOG target

* Fri Jul 29 2005 Samir Bellabes <sbellabes@mandriva.com> 1.3.3-1mdk
- update to version 1.3.3

* Wed Jul 27 2005 Samir Bellabes <sbellabes@mandriva.com> 1.3.2-2mdk
- update kernel headers to lastest versions (2.6.12-8mdk) and fix 
  malformed path in iptables-kernel-headers.tar.bz2
- fix lot of extensions test : Makefile check for $KERNEL_DIR/net/*/*/*.c
  but we provide only headers files ($KERNEL_DIR/include/linux/*/*.h)
  So test failed every time, and we don't get extension.
- add ipp2p extension, that is not in upstream iptables-1.3.2
- deleted extensions for linux-2.4 ( obsolete by now )

* Wed Jul 13 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 1.3.2-1mdk
- new upstream version: 1.3.2.
- redid stealth patch.
- obsoleted patch CAN-2004-0986.
- updated kernel headers to latest versions (2.6.12.2 & 2.4.31).

* Sat Apr 02 2005 Luca Berra <bluca@vodka.it> 1.2.9-8mdk 
- update kernel headers, we now have 4 flavors
- update initscript to test all flavors

* Tue Nov 02 2004 Vincent Danen <vdanen@mandrakesoft.com> 1.2.9-7.1.101mdk
- security fix for CAN-2004-0986

* Wed Jun 02 2004 Florin <florin@mandrakesoft.com> 1.2.9-7mdk
- add new extenions: see the kernel changelog here below
- netfilter (CLASSIFY CONNMARK IPMARK TARPIT addrtype condition 
	connbytes h323-conntrack-nat owner-socketlookup pptp-conntrack-nat 
	connlimit dstlimit iprange mport nth osf quota random time 
	rtsp-conntrack)

* Wed Jun 02 2004 Florin <florin@mandrakesoft.com> 1.2.9-6mdk
- add the devel package

* Sun Feb 15 2004 Luca Berra <bluca@vodka.it> 1.2.9-5mdk
- fix detection of iptables version at boot (again)

* Wed Jan 28 2004 Marcel Pol <mpol@mandrake.org> 1.2.9-4mdk
- update-alternatives seems unreliable, sorry

* Sun Jan 25 2004 Marcel Pol <mpol@mandrake.org> 1.2.9-3mdk
- doh, I can't read

* Sun Jan 25 2004 Luca Berra <bluca@vodka.it> 1.2.9-2mdk 
- compatible with both 2.4 and 2.6 (with and without pptp_conntrack)
- added check option to initscripts
- use alternatives (mpol)

* Fri Nov 28 2003 Juan Quintela <quintela@mandrakesoft.com> 1.2.9-1mdk
- IMQ should work now (cross fingers).
- reddiff stealth patch.
- 1.2.9.

* Wed Oct 08 2003 Juan Quintela <quintela@mandrakesoft.com> 1.2.9-0rc1mdk
- 1.2.9rc1.

* Tue Aug 26 2003 Juan Quintela <quintela@mandrakesoft.com> 1.2.8-2mdk
- added imq support.

