%define _disable_ld_no_undefined 1

Summary:	Tools for managing Linux kernel packet filtering capabilities
Name:		iptables
Version:	1.4.1.1
Release:	%manbo_mkrel 1
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
Patch1:		iptables-1.4.1.1-missing-header.patch
Patch100:	iptables-imq.diff
Patch101:	iptables-IFWLOG_extension.diff
Patch102:	iptables-psd.diff
Provides:	userspace-ipfilter
Requires(post): rpm-helper
Requires(preun): rpm-helper
Obsoletes:	%{name}-ipv6 < 1.4.1.1-0.5
Provides:	%{name}-ipv6
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
iptables controls the Linux kernel network packet filtering code.
It allows you to set up firewalls and IP masquerading, etc.

Install iptables if you need to set up firewalling for your
network.

%package	devel
Summary:	Development package for iptables
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	kernel-headers

%description	devel
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.

%prep

%setup -q

cp %{SOURCE1} iptables.init
cp %{SOURCE2} ip6tables.init
cp %{SOURCE3} iptables.sample
cp %{SOURCE4} ip6tables.sample

# fix libdir
perl -pi -e "s|\@lib\@|%{_lib}|g" iptables.init

%patch0 -p1 -b .libiptc
%patch1 -p1 -b .header

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

%build
%serverbuild

autoreconf -fis

export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export FFLAGS="$FFLAGS -fPIC"

# (tpg) be more sane
# XT_LIB_DIR in include/xtables/internal.h should be always same as --with-xtlibdir

sed -i -e 's#/usr/lib/iptables#/%{_lib}/iptables#g' include/xtables/internal.h

%configure2_5x \
    --bindir=/sbin \
    --sbindir=/sbin \
    --enable-devel \
    --enable-libipq \
    --with-ksource=%{_prefix}/src/linux \
    --with-xtlibdir=/%{_lib}/iptables

%make

# make more devel libs (debian)
ar rcs libiptables.a iptables.o
ar rcs libip6tables.a ip6tables.o

%install
rm -rf %{buildroot}

%makeinstall_std

# (oe) this in conjunction with the mandriva initscript will make it possible 	 
# to use development versions of the netfilter modules and with different 	 
# api:s. (according to blino) 	 
install -d %{buildroot}/%{_lib}/iptables.d 	 
mv %{buildroot}/%{_lib}/iptables %{buildroot}/%{_lib}/iptables.d/linux-2.6-main

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
# run only on fresh installation
if [ $1 = 1 ]; then
    /sbin/service iptables check
fi

%preun
%_preun_service iptables
%_preun_service ip6tables

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
/%{_lib}/iptables.d/linux-2.6-main/libipt_recent.so
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
/%{_lib}/iptables.d/linux-2.6-main/libxt_sctp.so
/%{_lib}/iptables.d/linux-2.6-main/libxt_SECMARK.so
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

%files devel
%defattr(-,root,root,0755)
%{_includedir}/*.h
%dir %{_includedir}/libipq
%dir %{_includedir}/libiptc
%dir %{_includedir}/libipulog
%{_includedir}/libipq/*.h
%{_includedir}/libiptc/*.h
%{_includedir}/libipulog/*.h
%{_libdir}/libipq.a
%{_libdir}/libiptc.a
%{_libdir}/libiptables.a
%{_libdir}/libip6tables.a
%{_mandir}/man3/*
