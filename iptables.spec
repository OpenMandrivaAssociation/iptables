# because the modules are not libtool aware
%define _disable_ld_no_undefined 1

%define major 10
%define libname %mklibname xtables %{major}
%define devname %mklibname -d iptables

%define ipq_major 0
%define libipq %mklibname ipq %{ipq_major}
%define devipq %mklibname -d ipq

%define iptc_major 0
%define libiptc %mklibname iptc %{iptc_major}
%define deviptc %mklibname -d iptc

%define libip4tc %mklibname ip4tc %{iptc_major}
%define devip4tc %mklibname -d ip4tc

%define libip6tc %mklibname ip6tc %{iptc_major}
%define devip6tcg %mklibname -d ip6tc

# install init scripts to /usr/libexec with systemd
%define script_path %{_libexecdir}

Summary:	Tools for managing Linux kernel packet filtering capabilities
Name:		iptables
Version:	1.4.19.1
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://netfilter.org/
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
#Patch101:	iptables-IFWLOG_extension.diff
#Patch102:	iptables-psd.diff
#Patch103:	iptables-1.4.17-fix-linking.patch

BuildRequires:	pkgconfig(libnfnetlink)
Requires(post,preun):	rpm-helper
Provides:	%{name}-ipv6 = %{version}
Provides:	userspace-ipfilter

%description
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

Install iptables if you need to set up firewalling for your network.

%package -n %{libname}
Summary:	Shared iptables library
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared iptables library.

%package -n %{devname}
Summary:	Development library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}

%description -n	%{devname}
This package contains the shared iptables library.

# ipq
%package -n %{libipq}
Summary:	Shared iptables library
Group:		System/Libraries

%description -n	%{libipq}
This package contains the ipq library.

%package -n %{devipq}
Summary:	Development library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{libipq} = %{version}-%{release}
Provides:	%{name}-ipq-devel = %{version}

%description -n	%{devipq}
This package contains the ipq library.

# iptc
%package -n %{libiptc}
Summary:	Shared iptables library
Group:		System/Libraries

%description -n	%{libiptc}
This package contains the IPTC library.

%package -n %{deviptc}
Summary:	Development library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{libiptc} = %{version}-%{release}
Provides:	%{name}-iptc-devel = %{version}

%description -n	%{deviptc}
This package contains the IPTC library.

# ip4tc
%package -n %{libip4tc}
Summary:	Shared iptables library
Group:		System/Libraries

%description -n	%{libip4tc}
This package contains the IP4TC library.

%package -n	%{devip4tc}
Summary:	Development library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{libip4tc} = %{version}-%{release}
Provides:	%{name}-ip4tc-devel = %{version}

%description -n	%{devip4tc}
This package contains the development files for IPTC library.

# ip6tc
%package -n %{libip6tc}
Summary:	Shared iptables library
Group:		System/Libraries

%description -n	%{libip6tc}
This package contains the IP6TC library.

%package -n %{devip6tcg}
Summary:	Development library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{libip6tc} = %{version}-%{release}
Provides:	%{name}-ip6tc-devel = %{version}

%description -n	%{devip6tcg}
This package contains the development files for IP6TC library.

%prep
%setup -q
cp %{SOURCE2} iptables.init
cp %{SOURCE3} ip6tables.init
cp %{SOURCE4} iptables.sample
cp %{SOURCE5} ip6tables.sample

# fix libdir
sed -i -e "s|\@lib\@|%{_lib}|g" iptables.init

# extensions
#install -m0644 %{SOURCE100} extensions/ <- it needs ipt_IMQ.h and we don't have it anymore ?!
#install -m0644 %{SOURCE101} extensions/
# (oe) psd comes from iptables-1.3.7, was removed in iptables-1.3.8
#install -m0644 %{SOURCE102} extensions/
#install -m0644 %{SOURCE103} extensions/

%apply_patches

find . -type f | xargs perl -pi -e "s,/usr/local,%{_prefix},g"

# don't run /sbin/ldconfig
sed -i -e "s|/sbin/ldconfig|/bin/true|g" Makefile*

%build
export LIBS="-ldl"

%serverbuild

autoreconf -fi

export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export FFLAGS="$FFLAGS -fPIC"

%configure2_5x \
	--disable-static \
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
#install -m0644 include/net/netfilter/*.h %{buildroot}%{_includedir}/net/netfilter/
install -m0644 include/ip*tables.h %{buildroot}%{_includedir}/
install -m0644 include/iptables/internal.h %{buildroot}%{_includedir}/iptables

#Intird not need. TODO drop it!
#install -d %{buildroot}%{_initrddir}
#install -m0755 iptables.init %{buildroot}%{_initrddir}/iptables
#install -m0755 ip6tables.init %{buildroot}%{_initrddir}/ip6tables

# install compatible excutable (since 1.4.11)
ln -sf xtables-multi %{buildroot}/sbin/iptables-multi
ln -sf xtables-multi %{buildroot}/sbin/ip6tables-multi

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
%{script_path}/iptables.init check

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
/%{_lib}/iptables.d/linux-2.6-main/libxt_bpf.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CHECKSUM.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CLASSIFY.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_cluster.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_comment.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_connbytes.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_connlabel.so
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
/%{_lib}/iptables.d/linux-2.6-main/libip6t_DNAT.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_DNPT.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_MASQUERADE.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_NETMAP.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_REDIRECT.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_SNAT.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_SNPT.so    
/%{_lib}/iptables.d/linux-2.6-main/libip6t_rt.so
%{_mandir}/*/ip6tables*
%{_sysconfdir}/xtables

%files -n %{libname}
/%{_lib}/libxtables.so.%{major}*

%files -n %{devname}
%{_includedir}/*.h
%dir %{_includedir}/libipulog
%{_includedir}/libipulog/*.h
%{_includedir}/iptables/*.h
#%{_includedir}/net/netfilter/*.h
/%{_lib}/libxtables.so
%{_libdir}/pkgconfig/xtables.pc

%files -n %{libipq}
/%{_lib}/libipq.so.%{ipq_major}*

%files -n %{devipq}
%{_includedir}/libipq/*.h
%dir %{_includedir}/libipq
/%{_lib}/libipq.so
%{_mandir}/man3/*ipq*
%{_libdir}/pkgconfig/libipq.pc

%files -n %{libiptc}
/%{_lib}/libiptc.so.%{iptc_major}*

%files -n %{deviptc}
%{_includedir}/libiptc/*.h
%dir %{_includedir}/libiptc
/%{_lib}/libiptc.so
%{_libdir}/pkgconfig/libiptc.pc

%files -n %{libip4tc}
/%{_lib}/libip4tc.so.%{iptc_major}*

%files -n %{devip4tc}
/%{_lib}/libip4tc.so
%{_libdir}/pkgconfig/libip4tc.pc

%files -n %{libip6tc}
/%{_lib}/libip6tc.so.%{iptc_major}*

%files -n %{devip6tcg}
/%{_lib}/libip6tc.so
%{_libdir}/pkgconfig/libip6tc.pc

