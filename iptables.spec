# libip4tc and libip6tc are used by systemd,
# libsystemd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%global optflags %{optflags} -fno-strict-aliasing

# install init scripts to /usr/libexec with systemd
%global script_path %{_libexecdir}/iptables

%define major 12
%define libname %mklibname xtables %{major}
%define iptlibname %mklibname iptables %{major}
%define develname %mklibname -d iptables
%define iptdevelname %mklibname -d iptables
%define lib32name libxtables%{major}
%define iptlib32name libiptables%{major}
%define devel32name libiptables-devel

%define iptc_develname %mklibname -d iptc
%define iptc_devel32name libiptc-devel

%define ipq_major 0
%define ipq_libname %mklibname ipq %{ipq_major}
%define ipq_develname %mklibname -d ipq
%define ipq_lib32name libipq%{ipq_major}
%define ipq_devel32name libipq-devel

%define ip4tc_major 2
%define ip4tc_libname %mklibname ip4tc %{ip4tc_major}
%define ip4tc_develname %mklibname -d ip4tc
%define ip4tc_lib32name libip4tc%{ip4tc_major}
%define ip4tc_devel32name libip4tc-devel

%define ip6tc_major 2
%define ip6tc_libname %mklibname ip6tc %{ip6tc_major}
%define ip6tc_develname %mklibname -d ip6tc
%define ip6tc_lib32name libip6tc%{ip6tc_major}
%define ip6tc_devel32name libip6tc-devel

Name: iptables
Summary: Tools for managing Linux kernel packet filtering capabilities
URL: http://www.netfilter.org/projects/iptables
Version:	1.8.6
Release:	1
Source: %{url}/files/%{name}-%{version}.tar.bz2
Source1: iptables.init
Source2: iptables-config
Source3: iptables.service
Source4: sysconfig_iptables
Source5: sysconfig_ip6tables
Source6: arptables-nft-helper

Patch2:	iptables-1.2.8-libiptc.h.patch
# pf.os: ISC license
# iptables-apply: Artistic Licence 2.0
License: GPLv2 and Artistic Licence 2.0 and ISC

# libnetfilter_conntrack is needed for xt_connlabel
BuildRequires: pkgconfig(libnetfilter_conntrack)
# libnfnetlink-devel is requires for nfnl_osf
BuildRequires: pkgconfig(libnfnetlink)
BuildRequires: selinux-devel
BuildRequires: kernel-headers
BuildRequires: systemd
# libmnl, libnftnl, bison, flex for nftables
BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc
BuildRequires: pkgconfig(libmnl) >= 1.0
BuildRequires: pkgconfig(libnftnl) >= 1.1.5
# libpcap-devel for nfbpf_compile
BuildRequires: pcap-devel
BuildRequires: autogen
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
Requires: %{libname} = %{EVRD}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides:	userspace-ipfilter = %{version}
Requires:	%{name}-services
%if %{with compat32}
BuildRequires:	devel(libmnl)
BuildRequires:	devel(libnftnl)
BuildRequires:	devel(libnfnetlink)
BuildRequires:	devel(libnetfilter_conntrack)
%endif

%description
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.

%package -n	%{libname}
Summary:	Shared iptables library
Group:          System/Libraries
Conflicts:	%mklibname %{name} 1
# Some other distros name the libxtables package libiptables.
# Let's remain compatible...
# (rename = Obsoletes + Provides)
%rename %{iptlibname}

%description -n	%{libname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the shared iptables library.

%package -n	%{develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{libname} = %{EVRD}
Requires:	%{name} = %{EVRD}
Provides:	iptables-devel = %{version}
Obsoletes:	iptables-devel < 1.4.2
# Some other distros name the libxtables package libiptables.
# Let's remain compatible...
# (rename = Obsoletes + Provides)
%rename %{iptdevelname}

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
Provides:	iptables-ipq-devel = %{version}

%description -n	%{ipq_develname}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the ipq library.

#iptc
%package -n	%{iptc_develname}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
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
Provides:	iptables-ip6tc-devel = %{version}

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

%package services
Summary: iptables and ip6tables services for iptables
Requires: %{name} >= %{EVRD}
%{?systemd_ordering}
# obsolete old main package
Obsoletes: %{name} < 1.8.4-1
# obsolete ipv6 sub package
Obsoletes: %{name}-ipv6 < 1.4.11.1

%description services
iptables services for IPv4 and IPv6

This package provides the services iptables and ip6tables that have been split
out of the base package since they are not active by default anymore.

%package utils
Summary: iptables and ip6tables services for iptables
Requires: %{name} = %{version}-%{release}

%description utils
Utils for iptables

This package provides nfnl_osf with the pf.os database and nfbpf_compile,
a bytecode generator for use with xt_bpf.

%package nft
Summary: nftables compatibility for iptables, arptables and ebtables
Requires: %{name} = %{version}-%{release}
Obsoletes: iptables-compat < 1.6.2-4
Provides: arptables-helper

%description nft
nftables compatibility for iptables, arptables and ebtables.

%if %{with compat32}
%package -n	%{lib32name}
Summary:	Shared iptables library (32-bit)
Group:          System/Libraries

%description -n	%{lib32name}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the shared iptables library.

%package -n	%{devel32name}
Summary:	Static library and header files for the iptables library (32-bit)
Group:		Development/C
Requires:	kernel-headers
Requires:	%{develname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n	%{devel32name}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the static iptables library.

# ipq
%package -n	%{ipq_lib32name}
Summary:	Shared iptables library (32-bit)
Group:          System/Libraries

%description -n	%{ipq_lib32name}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the ipq library.

%package -n	%{ipq_devel32name}
Summary:	Static library and header files for the iptables library
Group:		Development/C
Requires:	kernel-headers
Requires:	%{ipq_develname} = %{version}-%{release}
Requires:	%{ipq_lib32name} = %{version}-%{release}

%description -n	%{ipq_devel32name}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the ipq library.

#iptc
%package -n	%{iptc_devel32name}
Summary:	Static library and header files for the iptables library (32-bit)
Group:		Development/C
Requires:	kernel-headers
Requires:	%{iptc_develname} = %{EVRD}

%description -n	%{iptc_devel32name}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IPTC library.

# ip4tc
%package -n	%{ip4tc_lib32name}
Summary:	Shared iptables library (32-bit)
Group:          System/Libraries

%description -n	%{ip4tc_lib32name}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IP4TC library.

%package -n	%{ip4tc_devel32name}
Summary:	Static library and header files for the iptables library (32-bit)
Group:		Development/C
Requires:	kernel-headers
Requires:	%{ip4tc_lib32name} = %{version}-%{release}
Requires:	%{iptc_devel32name} = %{version}-%{release}
Requires:	%{ip4tc_develname} = %{EVRD}

%description -n	%{ip4tc_devel32name}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the development files for IPTC library.

# ip6tc
%package -n	%{ip6tc_lib32name}
Summary:	Shared iptables library (32-bit)
Group:          System/Libraries

%description -n	%{ip6tc_lib32name}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the IP6TC library.

%package -n	%{ip6tc_devel32name}
Summary:	Static library and header files for the iptables library (32-bit)
Group:		Development/C
Requires:	kernel-headers
Requires:	%{ip6tc_develname} = %{EVRD}
Requires:	%{ip6tc_lib32name} = %{version}-%{release}

%description -n	%{ip6tc_devel32name}
iptables controls the Linux kernel network packet filtering code. It allows you
to set up firewalls and IP masquerading, etc.

This package contains the development files for IP6TC library.
%endif

%prep
%autosetup -p1
./autogen.sh
export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--enable-devel \
	--with-xtlibdir=%{_prefix}/lib/xtables \
	--with-ksource=%{_prefix}/src/linux \
	--enable-libipq
cd ..
%endif

mkdir build
cd build
%configure \
	--enable-devel \
	--enable-bpf-compiler \
	--with-xtlibdir=%{_libdir}/xtables \
	--with-ksource=%{_prefix}/src/linux \
	--enable-libipq
# do not use rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool


%build
rm -f include/linux/types.h

%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
# We need only the libs, not the binaries or
# plugins
rm -rf %{buildroot}%{_prefix}/lib/xtables
%endif
%make_install -C build

# install ip*tables.h header files
install -m 644 include/ip*tables.h %{buildroot}%{_includedir}/
install -d -m 755 %{buildroot}%{_includedir}/iptables
install -m 644 include/iptables/internal.h %{buildroot}%{_includedir}/iptables/

# header development files
install -d %{buildroot}%{_includedir}/{libipq,libiptc,libipulog}
install -m0644 include/libipq/*.h %{buildroot}%{_includedir}/libipq/
			       install -m0644 include/libiptc/*.h %{buildroot}%{_includedir}/libiptc/
			       install -m0644 include/libipulog/*.h %{buildroot}%{_includedir}/libipulog/

# install ipulog header file
install -d -m 755 %{buildroot}%{_includedir}/libipulog/
install -m 644 include/libipulog/*.h %{buildroot}%{_includedir}/libipulog/

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

# install iptables-apply with man page
install -m 755 iptables/iptables-apply %{buildroot}%{_sbindir}/
install -m 644 build/iptables/iptables-apply.8 %{buildroot}%{_mandir}/man8/

rm -f %{buildroot}%{_sysconfdir}/ethertypes

install -p -D -m 755 %{SOURCE6} %{buildroot}%{_libexecdir}/
touch %{buildroot}%{_libexecdir}/arptables-helper

# prepare for alternatives
touch %{buildroot}%{_mandir}/man8/arptables.8
touch %{buildroot}%{_mandir}/man8/arptables-save.8
touch %{buildroot}%{_mandir}/man8/arptables-restore.8
touch %{buildroot}%{_mandir}/man8/ebtables.8

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
	$pfx iptables $pfx-nft 5 \
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
	$pfx ebtables $pfx-nft 5 \
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
	$pfx arptables $pfx-nft 5 \
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
%doc INCOMPATIBILITIES
%{_sbindir}/iptables-apply
%{_sbindir}/ip6tables-apply
%{_sbindir}/iptables-legacy*
%{_sbindir}/ip6tables-legacy*
%{_sbindir}/xtables-legacy-multi
%{_bindir}/iptables-xml
%{_mandir}/man1/iptables-xml*
%{_mandir}/man8/iptables*
%{_mandir}/man8/ip6tables*
%{_mandir}/man8/xtables-legacy*
%dir %{_libdir}/xtables
%{_libdir}/xtables/libarpt*
%{_libdir}/xtables/libebt*
%{_libdir}/xtables/libipt*
%{_libdir}/xtables/libip6t*
%{_libdir}/xtables/libxt*
%ghost %{_sbindir}/iptables
%ghost %{_sbindir}/iptables-restore
%ghost %{_sbindir}/iptables-save
%ghost %{_sbindir}/ip6tables
%ghost %{_sbindir}/ip6tables-restore
%ghost %{_sbindir}/ip6tables-save

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
%dir %{_includedir}/libipulog
%{_includedir}/libipq/*.h
%{_includedir}/libipulog/*.h
%{_includedir}/iptables/*.h
%{_libdir}/libxtables.so
%{_libdir}/pkgconfig/xtables.pc

%files -n %{ipq_develname}
%{_includedir}/libipq/*.h
%{_libdir}/pkgconfig/libipq.pc
%dir %{_includedir}/libipq
%{_libdir}/libipq.so
%{_mandir}/man3/*ipq*

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
%{script_path}/iptables.init
%{script_path}/ip6tables.init
%config(noreplace) %{_sysconfdir}/sysconfig/iptables
%config(noreplace) %{_sysconfdir}/sysconfig/ip6tables
%config(noreplace) %{_sysconfdir}/sysconfig/iptables-config
%config(noreplace) %{_sysconfdir}/sysconfig/ip6tables-config
%{_unitdir}/iptables.service
%{_unitdir}/ip6tables.service

%files utils
%{_sbindir}/nfnl_osf
%{_sbindir}/nfbpf_compile
%dir %{_datadir}/xtables
%{_datadir}/xtables/pf.os
%{_mandir}/man8/nfnl_osf*
%{_mandir}/man8/nfbpf_compile*

%files nft
%{_sbindir}/iptables-nft*
%{_sbindir}/iptables-restore-translate
%{_sbindir}/iptables-translate
%{_sbindir}/ip6tables-nft*
%{_sbindir}/ip6tables-restore-translate
%{_sbindir}/ip6tables-translate
%{_sbindir}/ebtables-nft*
%{_sbindir}/arptables-nft*
%{_sbindir}/xtables-nft-multi
%{_sbindir}/xtables-monitor
%{_libexecdir}/arptables-nft-helper
%{_mandir}/man8/xtables-monitor*
%{_mandir}/man8/xtables-translate*
%{_mandir}/man8/*-nft*
%ghost %{_sbindir}/iptables
%ghost %{_sbindir}/iptables-restore
%ghost %{_sbindir}/iptables-save
%ghost %{_sbindir}/ip6tables
%ghost %{_sbindir}/ip6tables-restore
%ghost %{_sbindir}/ip6tables-save
%ghost %{_sbindir}/ebtables
%ghost %{_sbindir}/ebtables-save
%ghost %{_sbindir}/ebtables-restore
%ghost %{_sbindir}/arptables
%ghost %{_sbindir}/arptables-save
%ghost %{_sbindir}/arptables-restore
%ghost %{_libexecdir}/arptables-helper
%ghost %{_mandir}/man8/arptables.8.*
%ghost %{_mandir}/man8/arptables-save.8.*
%ghost %{_mandir}/man8/arptables-restore.8.*
%ghost %{_mandir}/man8/ebtables.8.*

%if %{with compat32}
%files -n %{ipq_lib32name}
%{_prefix}/lib/libipq.so.*

%files -n %{ip4tc_lib32name}
%{_prefix}/lib/libip4tc.so.*

%files -n %{ip6tc_lib32name}
%{_prefix}/lib/libip6tc.so.*

%files -n %{lib32name}
%{_prefix}/lib/libxtables.so.%{major}*

%files -n %{devel32name}
%{_prefix}/lib/libxtables.so
%{_prefix}/lib/pkgconfig/xtables.pc

%files -n %{ipq_devel32name}
%{_prefix}/lib/pkgconfig/libipq.pc
%{_prefix}/lib/libipq.so

%files -n %{iptc_devel32name}
%{_prefix}/lib/pkgconfig/libiptc.pc

%files -n %{ip4tc_devel32name}
%{_prefix}/lib/libip4tc.so
%{_prefix}/lib/pkgconfig/libip4tc.pc

%files -n %{ip6tc_devel32name}
%{_prefix}/lib/libip6tc.so
%{_prefix}/lib/pkgconfig/libip6tc.pc
%endif
