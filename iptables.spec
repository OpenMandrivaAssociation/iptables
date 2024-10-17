%global optflags %{optflags} -Oz -fno-strict-aliasing
%define dont_relink 1

# install init scripts to /usr/libexec with systemd
%global script_path %{_libexecdir}/iptables

%define major 12
%define libname %mklibname xtables %{major}
%define iptlibname %mklibname iptables %{major}
%define develname %mklibname -d iptables
%define iptdevelname %mklibname -d iptables


%define iptc_develname %mklibname -d iptc
%define iptc_devel32name libiptc-devel

%define ipq_major 0
%define ipq_libname %mklibname ipq %{ipq_major}
%define ipq_develname %mklibname -d ipq

%define ip4tc_major 2
%define ip4tc_libname %mklibname ip4tc %{ip4tc_major}
%define ip4tc_develname %mklibname -d ip4tc

%define ip6tc_major 2
%define ip6tc_libname %mklibname ip6tc %{ip6tc_major}
%define ip6tc_develname %mklibname -d ip6tc

Name:		iptables
Summary:	Tools for managing Linux kernel packet filtering capabilities
URL:		https://www.netfilter.org/projects/iptables
Version:	1.8.10
Release:	1
# pf.os: ISC license
# iptables-apply: Artistic Licence 2.0
License:	GPLv2 and Artistic Licence 2.0 and ISC
Group:		System/Kernel and hardware
Source0:	%{url}/files/%{name}-%{version}.tar.xz
Source1:	iptables.init
Source2:	iptables-config
Source3:	iptables.service
Source4:	sysconfig_iptables
Source5:	sysconfig_ip6tables
Source6:	arptables-nft-helper
Patch2:		iptables-1.2.8-libiptc.h.patch
Patch3:		iptables-1.8.2-dont_read_garbage.patch
# libnetfilter_conntrack is needed for xt_connlabel
BuildRequires:	pkgconfig(libnetfilter_conntrack)
# libnfnetlink-devel is requires for nfnl_osf
BuildRequires:	pkgconfig(libnfnetlink)
BuildRequires:	selinux-devel
BuildRequires:	kernel-headers
BuildRequires:	systemd
# libmnl, libnftnl, bison, flex for nftables
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(libmnl) >= 1.0
BuildRequires:	pkgconfig(libnftnl) >= 1.1.5
# libpcap-devel for nfbpf_compile
BuildRequires:	pcap-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Requires:	%{libname} = %{EVRD}
Requires:	%{name}-xtables = %{EVRD}
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives
Provides:	userspace-ipfilter = %{version}
Obsoletes:	libxtables12 < 1.8.9-1
Obsoletes:	libiptables12 < 1.8.9-1
Obsoletes:	libiptables-devel < 1.8.9-1
Obsoletes:	libipq0 < 1.8.9-1
Obsoletes:	libipq-devel < 1.8.9-1
Obsoletes:	libip4tc2 < 1.8.9-1
Obsoletes:	libip4tc-devel < 1.8.9-1
Obsoletes:	libip6tc2 < 1.8.9-1
Obsoletes:	libip6tc-devel < 1.8.9-1

%description
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.

%package -n %{libname}
Summary:	Shared iptables library
Group:		System/Libraries
Conflicts:	%mklibname %{name} 1
# Some other distros name the libxtables package libiptables.
# Let's remain compatible...
# (rename = Obsoletes + Provides)
%rename %{iptlibname}

%description -n %{libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the shared iptables library.

%package -n %{develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{libname} = %{EVRD}
Requires:	%{name}-xtables = %{EVRD}
Provides:	iptables-devel = %{version}
Obsoletes:	iptables-devel < 1.4.2
# Some other distros name the libxtables package libiptables.
# Let's remain compatible...
# (rename = Obsoletes + Provides)
%rename %{iptdevelname}

%description -n %{develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the static iptables library.

# ipq
%package -n %{ipq_libname}
Summary:	Shared iptables library
Group:		System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n %{ipq_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the ipq library.

%package -n %{ipq_develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{ipq_libname} = %{version}-%{release}
Provides:	iptables-ipq-devel = %{version}

%description -n %{ipq_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the ipq library.

#iptc
%package -n %{iptc_develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Provides:	iptables-iptc-devel = %{version}

%description -n %{iptc_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IPTC library.

# ip4tc
%package -n %{ip4tc_libname}
Summary:	Shared iptables library
Group:		System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n %{ip4tc_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IP4TC library.

%package -n %{ip4tc_develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{ip4tc_libname} = %{version}-%{release}
Requires:	%{iptc_develname} = %{version}-%{release}
Provides:	iptables-ip6tc-devel = %{version}

%description -n %{ip4tc_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the development files for IPTC library.

# ip6tc
%package -n %{ip6tc_libname}
Summary:	Shared iptables library
Group:		System/Libraries
Obsoletes:	%{mklibname iptables 1} < 1.4.3.2

%description -n %{ip6tc_libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IP6TC library.

%package -n %{ip6tc_develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{ip6tc_libname} = %{version}-%{release}
Provides:	iptables-ip6tc-devel = %{version}

%description -n %{ip6tc_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the development files for IP6TC library.

%package services
Summary:	iptables and ip6tables services for iptables
Group:		System/Kernel and hardware
Requires:	%{name} >= %{EVRD}
%{?systemd_ordering}
# obsolete old main package
Obsoletes:	%{name} < 1.8.4-1
# obsolete ipv6 sub package
Obsoletes:	%{name}-ipv6 < 1.4.11.1
BuildArch:	noarch

%description services
iptables services for IPv4 and IPv6.

This package provides the services iptables and ip6tables that have been split
out of the base package since they are not active by default anymore.

%package utils
Summary:	iptables and ip6tables services for iptables
Requires:	%{name} = %{EVRD}

%description utils
Utils for iptables.

This package provides nfnl_osf with the pf.os database and nfbpf_compile,
a bytecode generator for use with xt_bpf.

%package xtables
Summary:	xtables and iptables extensions userspace support
Group:		System/Kernel and hardware

%description xtables
Libxtables provides unified access to iptables extensions in userspace. Data
and logic for those is kept in per-extension shared object files.

%package nft
Summary:	nftables compatibility for iptables, arptables and ebtables
Group:		System/Kernel and hardware
Requires:	%{name}-xtables = %{EVRD}
Requires(post):	coreutils
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives
Obsoletes:	iptables-compat < 1.6.2-4
Provides:	arptables-helper
Provides:	arptables
Provides:	ebtables
Provides:	iptables

%description nft
nftables compatibility for iptables, arptables and ebtables.

%prep
%autosetup -p1
./autogen.sh

%build
%configure \
	--enable-devel \
	--enable-bpf-compiler \
	--with-xtlibdir=%{_libdir}/xtables \
	--with-ksource=%{_prefix}/src/linux \
	--enable-libipq

# do not use rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

rm -f include/linux/types.h

%make_build

%install
%make_install

# install ip*tables.h header files
install -m 644 include/ip*tables.h %{buildroot}%{_includedir}/
install -d -m 755 %{buildroot}%{_includedir}/iptables
install -m 644 include/iptables/internal.h %{buildroot}%{_includedir}/iptables/

# header development files
install -d %{buildroot}%{_includedir}/{libipq,libiptc}
install -m0644 include/libipq/*.h %{buildroot}%{_includedir}/libipq/
install -m0644 include/libiptc/*.h %{buildroot}%{_includedir}/libiptc/

# install init scripts and configuration files
install -d -m 755 %{buildroot}%{script_path}
install -c -m 755 %{SOURCE1} %{buildroot}%{script_path}/iptables.init
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE1} > ip6tables.init
install -c -m 755 ip6tables.init %{buildroot}%{script_path}/ip6tables.init
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -c -m 600 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/iptables-config
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE2} > ip6tables-config
install -c -m 600 ip6tables-config %{buildroot}%{_sysconfdir}/sysconfig/ip6tables-config
install -c -m 600 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/iptables
install -c -m 600 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ip6tables

# install systemd service files
install -d -m 755 %{buildroot}/%{_unitdir}
install -c -m 644 %{SOURCE3} %{buildroot}/%{_unitdir}
sed -e 's;iptables;ip6tables;g' -e 's;IPv4;IPv6;g' -e 's;/usr/libexec/ip6tables;/usr/libexec/iptables;g' < %{SOURCE3} > ip6tables.service
install -c -m 644 ip6tables.service %{buildroot}/%{_unitdir}

rm -f %{buildroot}%{_sysconfdir}/ethertypes

install -p -D -m 755 %{SOURCE6} %{buildroot}%{_libexecdir}/
touch %{buildroot}%{_libexecdir}/arptables-helper

# prepare for alternatives
touch %{buildroot}%{_mandir}/man8/arptables.8
touch %{buildroot}%{_mandir}/man8/arptables-save.8
touch %{buildroot}%{_mandir}/man8/arptables-restore.8
touch %{buildroot}%{_mandir}/man8/ebtables.8

# Drop xtables.conf, it's not used
rm -f %{buildroot}%{_sysconfdir}/xtables.conf
# fix absolute symlink
rm -f %{buildroot}%{_bindir}/iptables-xml
ln -s ../bin/xtables-legacy-multi %{buildroot}%{_bindir}/iptables-xml

%post
pfx=%{_sbindir}/iptables
pfx6=%{_sbindir}/ip6tables
%{_sbindir}/update-alternatives --install \
    $pfx iptables $pfx-legacy 10 \
    --slave $pfx6 ip6tables $pfx6-legacy \
    --slave $pfx-restore iptables-restore $pfx-legacy-restore \
    --slave $pfx-save iptables-save $pfx-legacy-save \
    --slave $pfx6-restore ip6tables-restore $pfx6-legacy-restore \
    --slave $pfx6-save ip6tables-save $pfx6-legacy-save

%postun
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives --remove \
	iptables %{_sbindir}/iptables-legacy
fi

%post services
%systemd_post iptables.service ip6tables.service

%preun services
%systemd_preun iptables.service ip6tables.service

%postun services
%systemd_postun iptables.service ip6tables.service

%post nft
pfx=%{_sbindir}/iptables
pfx6=%{_sbindir}/ip6tables
%{_sbindir}/update-alternatives --install \
    $pfx iptables $pfx-nft 10 \
    --slave $pfx6 ip6tables $pfx6-nft \
    --slave $pfx-restore iptables-restore $pfx-nft-restore \
    --slave $pfx-save iptables-save $pfx-nft-save \
    --slave $pfx6-restore ip6tables-restore $pfx6-nft-restore \
    --slave $pfx6-save ip6tables-save $pfx6-nft-save

pfx=%{_sbindir}/ebtables
manpfx=%{_mandir}/man8/ebtables
for sfx in "" "-restore" "-save"; do
    if [ "$(readlink -e $pfx$sfx)" == $pfx$sfx ]; then
	rm -f $pfx$sfx
    fi
done
if [ "$(readlink -e $manpfx.8%{_extension})" == $manpfx.8%{_extension} ]; then
    rm -f $manpfx.8%{_extension}
fi
%{_sbindir}/update-alternatives --install \
    $pfx ebtables $pfx-nft 10 \
    --slave $pfx-save ebtables-save $pfx-nft-save \
    --slave $pfx-restore ebtables-restore $pfx-nft-restore \
    --slave $manpfx.8%{_extension} ebtables-man $manpfx-nft.8%{_extension}

pfx=%{_sbindir}/arptables
manpfx=%{_mandir}/man8/arptables
lepfx=%{_libexecdir}/arptables
for sfx in "" "-restore" "-save"; do
    if [ "$(readlink -e $pfx$sfx)" == $pfx$sfx ]; then
	rm -f $pfx$sfx
    fi
    if [ "$(readlink -e $manpfx$sfx.8%{_extension})" == $manpfx$sfx.8%{_extension} ]; then
	rm -f $manpfx$sfx.8%{_extension}
    fi
done
if [ "$(readlink -e $lepfx-helper)" == $lepfx-helper ]; then
    rm -f $lepfx-helper
fi
%{_sbindir}/update-alternatives --install \
    $pfx arptables $pfx-nft 10 \
    --slave $pfx-save arptables-save $pfx-nft-save \
    --slave $pfx-restore arptables-restore $pfx-nft-restore \
    --slave $manpfx.8%{_extension} arptables-man $manpfx-nft.8%{_extension} \
    --slave $manpfx-save.8%{_extension} arptables-save-man $manpfx-nft-save.8%{_extension} \
    --slave $manpfx-restore.8%{_extension} arptables-restore-man $manpfx-nft-restore.8%{_extension} \
    --slave $lepfx-helper arptables-helper $lepfx-nft-helper

%postun nft
if [ $1 -eq 0 ]; then
    for cmd in iptables ebtables arptables; do
	%{_sbindir}/update-alternatives --remove \
	$cmd %{_sbindir}/$cmd-nft
    done
fi

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sbindir}/ip{,6}tables-legacy*
%{_sbindir}/xtables-legacy-multi
%{_bindir}/iptables-xml
%doc %{_mandir}/man1/iptables-xml*
%doc %{_mandir}/man8/xtables-legacy*
%{_datadir}/xtables/iptables.xslt
%ghost %{_sbindir}/ip{,6}tables{,-save,-restore}

%files xtables
%dir %{_libdir}/xtables
%{_libdir}/xtables/lib{ip,ip6,x}t*
%doc %{_mandir}/man8/ip{,6}tables.8%{_extension}
%doc %{_mandir}/man8/ip{,6}tables-{extensions,save,restore}.8%{_extension}

%files -n %{ipq_libname}
%{_libdir}/libipq.so.*

%files -n %{ip4tc_libname}
%{_libdir}/libip4tc.so.*

%files -n %{ip6tc_libname}
%{_libdir}/libip6tc.so.*

%files -n %{libname}
%{_libdir}/libxtables.so.%{major}*

%files -n %{develname}
%{_includedir}/*.h
%dir %{_includedir}/libipq
%{_includedir}/libipq/*.h
%{_includedir}/iptables/*.h
%{_libdir}/libxtables.so
%{_libdir}/pkgconfig/xtables.pc

%files -n %{ipq_develname}
%{_includedir}/libipq/*.h
%{_libdir}/pkgconfig/libipq.pc
%dir %{_includedir}/libipq
%{_libdir}/libipq.so
%doc %{_mandir}/man3/*ipq*

%files -n %{iptc_develname}
%{_includedir}/libiptc/*.h
%dir %{_includedir}/libiptc
%{_libdir}/pkgconfig/libiptc.pc

%files -n %{ip4tc_develname}
%{_libdir}/libip4tc.so
%{_libdir}/pkgconfig/libip4tc.pc

%files -n %{ip6tc_develname}
%{_libdir}/libip6tc.so
%{_libdir}/pkgconfig/libip6tc.pc

%files services
%dir %{script_path}
%{script_path}/ip{,6}tables.init
%config(noreplace) %{_sysconfdir}/sysconfig/ip{,6}tables{,-config}
%{_unitdir}/ip{,6}tables.service

%files utils
%{_sbindir}/nfnl_osf
%{_sbindir}/nfbpf_compile
%{_sbindir}/ip{,6}tables-apply
%dir %{_datadir}/xtables
%{_datadir}/xtables/pf.os
%doc %{_mandir}/man8/nfnl_osf*
%doc %{_mandir}/man8/nfbpf_compile*
%doc %{_mandir}/man8/ip{,6}tables-apply*

%files nft
%{_sbindir}/ip{,6}tables-nft*
%{_sbindir}/ip{,6}tables{,-restore}-translate
%{_sbindir}/{eb,arp}tables-nft*
%{_sbindir}/ebtables-translate
%{_sbindir}/xtables-nft-multi
%{_sbindir}/xtables-monitor
%dir %{_libdir}/xtables
%{_libdir}/xtables/lib{arp,eb}t*
%{_libexecdir}/arptables-nft-helper
%doc %{_mandir}/man8/xtables-monitor*
%doc %{_mandir}/man8/xtables-translate*
%doc %{_mandir}/man8/*-nft*
%doc %{_mandir}/man8/ip{,6}tables{,-restore}-translate*
%doc %{_mandir}/man8//ebtables-translate.*
%ghost %{_sbindir}/ip{,6}tables{,-save,-restore}
%ghost %{_sbindir}/{eb,arp}tables{,-save,-restore}
%ghost %{_libexecdir}/arptables-helper
%ghost %{_mandir}/man8/arptables{,-save,-restore}.8%{_extension}
%ghost %{_mandir}/man8/ebtables.8%{_extension}
