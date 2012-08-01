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

Summary:	Tools for managing Linux kernel packet filtering capabilities
Name:		iptables
Version:	1.4.15
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://netfilter.org/
Source0:	http://netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
Source1:	http://netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2.sig
Source2:	iptables.init
Source3:	ip6tables.init
Source4:	iptables.config
Source5:	ip6tables.config
# S100 and up used to be in the added patches
Source100:	libipt_IMQ.c
Source101:	libipt_IFWLOG.c
# (oe) psd comes from iptables-1.3.7, was removed in iptables-1.3.8
Source102:	libipt_psd.c
Source103:	libipt_psd.man
Patch0:		iptables-1.2.8-libiptc.h.patch
Patch1:		iptables-1.4.12.2-fix-build-with-3.2.patch
Patch100:	iptables-imq.diff
Patch101:	iptables-IFWLOG_extension.diff
Patch102:	iptables-psd.diff
Provides:	userspace-ipfilter
BuildRequires:	nfnetlink-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Obsoletes:	%{name} < 1.4.3.2
Obsoletes:	%{name}-ipv6 < 1.4.1.1-0.5
Provides:	%{name}-ipv6

%description
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

Install iptables if you need to set up firewalling for your network.

%package -n	%{libname}
Summary:	Shared iptables library
Group:          System/Libraries
Conflicts:	%mklibname %{name} 1
Conflicts:	%mklibname %{name} 4
Conflicts:	%mklibname %{name} 5

%description -n	%{libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the shared iptables library.

%package -n	%{develname}
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
%package -n	%{ipq_libname}
Summary:	Shared iptables library
Group:          System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n	%{ipq_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the ipq library.

%package -n	%{ipq_develname}
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
%package -n	%{iptc_libname}
Summary:	Shared iptables library
Group:          System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n	%{iptc_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IPTC library.

%package -n	%{iptc_develname}
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
%package -n	%{ip4tc_libname}
Summary:	Shared iptables library
Group:          System/Libraries
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
%package -n	%{ip6tc_libname}
Summary:	Shared iptables library
Group:          System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n	%{ip6tc_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IP6TC library.

%package -n	%{ip6tc_develname}
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

#%patch0 -p0 -b .libiptc
%patch1 -p1

# extensions
#install -m0644 %{SOURCE100} extensions/ <- it needs ipt_IMQ.h and we don't have it anymore ?!
install -m0644 %{SOURCE101} extensions/
# (oe) psd comes from iptables-1.3.7, was removed in iptables-1.3.8
install -m0644 %{SOURCE102} extensions/
install -m0644 %{SOURCE103} extensions/

%patch100 -p0
%patch101 -p0
%patch102 -p0

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

make

%install
rm -rf %{buildroot}

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

install -d %{buildroot}%{_initrddir}
install -m0755 iptables.init %{buildroot}%{_initrddir}/iptables
install -m0755 ip6tables.init %{buildroot}%{_initrddir}/ip6tables

# install compatible excutable (since 1.4.11)
ln -sf xtables-multi %{buildroot}/sbin/iptables-multi
ln -sf xtables-multi %{buildroot}/sbin/ip6tables-multi

# nuke *.la and static files
rm -f %{buildroot}/%{_lib}/*.*a

%post
%_post_service iptables
%_post_service ip6tables
/sbin/service iptables check

%preun
%_preun_service iptables
%_preun_service ip6tables

%files
%doc INSTALL INCOMPATIBILITIES iptables.sample ip6tables.sample
%attr(0755,root,root) %{_initrddir}/ip*
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
/%{_lib}/iptables.d/linux-2.6-main/libipt_IFWLOG.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_LOG.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_MASQUERADE.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_MIRROR.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_NETMAP.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_psd.so
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
