%define _disable_ld_no_undefined 1

%define major 2
%define libname %mklibname iptables %{major}
%define develname %mklibname -d iptables

%define iptc_major 0
%define iptc_libname %mklibname iptc %{iptc_major}
%define iptc_develname %mklibname -d iptc

Summary:	Tools for managing Linux kernel packet filtering capabilities
Name:		iptables
Version:	1.4.3.2
Release:	%manbo_mkrel 3
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://netfilter.org/
Source:		http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
Source1:	iptables.init
Source2:	ip6tables.init
Source3:	iptables.config
Source4:	ip6tables.config
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
Provides:	userspace-ipfilter
Requires(post): rpm-helper
Requires(preun): rpm-helper
Obsoletes:	%{name} < 1.4.3.2
Obsoletes:	%{name}-ipv6 < 1.4.1.1-0.5
Provides:	%{name}-ipv6
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

Install iptables if you need to set up firewalling for your network.

%package -n	%{libname}
Summary:	Shared iptables library
Group:          System/Libraries
Conflicts:	%mklibname %{name} 1

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
Provides:	iptables-iptc-devel = %{version}

%description -n	%{iptc_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IPTC library.

%prep

%setup -q

cp %{SOURCE1} iptables.init
cp %{SOURCE2} ip6tables.init
cp %{SOURCE3} iptables.sample
cp %{SOURCE4} ip6tables.sample

# fix libdir
perl -pi -e "s|\@lib\@|%{_lib}|g" iptables.init

%patch0 -p0 -b .libiptc

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

autoreconf -fis

export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export FFLAGS="$FFLAGS -fPIC"

%configure2_5x \
    --bindir=/sbin \
    --sbindir=/sbin \
    --enable-devel \
    --enable-libipq \
    --with-ksource=%{_prefix}/src/linux \
    --with-xtlibdir=/%{_lib}/iptables

make

# make more devel libs (debian)
ar rcs libiptables.a iptables.o
ar rcs libip6tables.a ip6tables.o

# hmm...
ar rcs libiptc/libiptc.a libiptc/.libs/libip4tc.o libiptc/.libs/libip6tc.o

%install
rm -rf %{buildroot}

%makeinstall_std

# (oe) this in conjunction with the mandriva initscript will make it possible 	 
# to use development versions of the netfilter modules and with different 	 
# api:s. (according to blino) 	 
install -d %{buildroot}/%{_lib}/iptables.d 	 
mv %{buildroot}/%{_lib}/iptables %{buildroot}/%{_lib}/iptables.d/linux-2.6-main

# move the shared libs
mv %{buildroot}%{_libdir}/libxtables.so.%{major}* %{buildroot}/%{_lib}/
ln -snf /%{_lib}/libxtables.so.%{major} %{buildroot}%{_libdir}/libxtables.so

mv %{buildroot}%{_libdir}/libiptc.so.* %{buildroot}/%{_lib}/
ln -snf /%{_lib}/libiptc.so.0 %{buildroot}%{_libdir}/libiptc.so

# static development files
install -d %{buildroot}%{_libdir}
install -m0644 libiptc/libiptc.a %{buildroot}%{_libdir}/libiptc.a
install -m0644 libiptables.a %{buildroot}%{_libdir}/
install -m0644 libip6tables.a %{buildroot}%{_libdir}/

# header development files
install -d %{buildroot}%{_includedir}/{libipq,libiptc,libipulog}
install -m0644 include/libipq/*.h %{buildroot}%{_includedir}/libipq/
install -m0644 include/libiptc/*.h %{buildroot}%{_includedir}/libiptc/
install -m0644 include/libipulog/*.h %{buildroot}%{_includedir}/libipulog/

install -d %{buildroot}%{_initrddir}
install -m0755 iptables.init %{buildroot}%{_initrddir}/iptables
install -m0755 ip6tables.init %{buildroot}%{_initrddir}/ip6tables

%post
%_post_service iptables
%_post_service ip6tables
/sbin/service iptables check

%preun
%_preun_service iptables
%_preun_service ip6tables

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc INSTALL INCOMPATIBILITIES iptables.sample ip6tables.sample
%attr(0755,root,root) %{_initrddir}/ip*
/sbin/iptables
/sbin/iptables-multi
/sbin/iptables-restore
/sbin/iptables-save
/sbin/iptables-xml
# ipv6
/sbin/ip6tables
/sbin/ip6tables-multi
/sbin/ip6tables-restore
/sbin/ip6tables-save
%dir /%{_lib}/iptables.d
%dir /%{_lib}/iptables.d/linux-2.6-main
/%{_lib}/iptables.d/linux-2.6-main/libipt_addrtype.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_ah.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_CLUSTERIP.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_DNAT.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_ecn.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_ECN.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_icmp.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_IFWLOG.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_LOG.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_MASQUERADE.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_MIRROR.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_NETMAP.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_policy.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_psd.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_realm.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_REDIRECT.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_REJECT.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_SAME.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_set.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_SET.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_SNAT.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_ttl.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_TTL.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_ULOG.so
/%{_lib}/iptables.d/linux-2.6-main/libipt_unclean.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CLASSIFY.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_comment.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_connbytes.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_connlimit.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_connmark.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CONNMARK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_CONNSECMARK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_conntrack.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_dccp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_dscp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_DSCP.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_esp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_hashlimit.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_helper.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_iprange.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_length.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_limit.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_mac.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_mark.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_MARK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_multiport.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_NFLOG.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_NFQUEUE.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_NOTRACK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_owner.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_physdev.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_pkttype.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_quota.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_rateest.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_RATEEST.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_recent.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_sctp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_SECMARK.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_socket.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_standard.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_state.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_statistic.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_string.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_tcpmss.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TCPMSS.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TCPOPTSTRIP.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_tcp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_time.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_tos.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TOS.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TPROXY.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_TRACE.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_u32.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_udp.so
%{_mandir}/*/iptables*
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
/%{_lib}/iptables.d/linux-2.6-main/libip6t_policy.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_REJECT.so
/%{_lib}/iptables.d/linux-2.6-main/libip6t_rt.so
%{_mandir}/*/ip6tables*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/libxtables.so.%{major}*

%files -n %{develname}
%defattr(-, root, root)
%{_includedir}/*.h
%dir %{_includedir}/libipq
%dir %{_includedir}/libipulog
%{_includedir}/libipq/*.h
%{_includedir}/libipulog/*.h
%{_libdir}/libxtables.so
%{_libdir}/libxtables.*a
%{_libdir}/libipq.*a
%{_libdir}/libiptables.*a
%{_libdir}/libip6tables.*a
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%files -n %{iptc_libname}
%defattr(-,root,root)
/%{_lib}/libiptc.so.*

%files -n %{iptc_develname}
%defattr(-, root, root)
%{_includedir}/*.h
%dir %{_includedir}/libiptc
%{_includedir}/libiptc/*.h
%{_libdir}/libiptc.so
%{_libdir}/libiptc.*a
