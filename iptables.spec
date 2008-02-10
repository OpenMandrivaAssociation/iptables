%define build_devel 1

Summary:	Tools for managing Linux kernel packet filtering capabilities
Name:		iptables
Version:	1.4.0
Release:	%mkrel 0.6
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
Patch0:		iptables-1.2.8-libiptc.h.patch 
Patch100:	iptables-imq.diff
Patch101:	iptables-IFWLOG_extension.diff
# (oe) this comes from iptables-1.3.7, was removed in iptables-1.3.8
Patch102:	iptables-psd.diff
BuildRequires:	perl-base
BuildRequires:  kernel-source
Provides:	userspace-ipfilter
Requires(post): rpm-helper
Requires(preun): rpm-helper
Conflicts:	ipchains
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
iptables controls the Linux kernel network packet filtering code.
It allows you to set up firewalls and IP masquerading, etc.

Install iptables if you need to set up firewalling for your
network.

%package	ipv6
Summary:	IPv6 support for iptables
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description	ipv6
IPv6 support for iptables.

iptables controls the Linux kernel network packet filtering code.
It allows you to set up firewalls and IP masquerading, etc.

IPv6 is the next version of the IP protocol.

Install iptables-ipv6 if you need to set up firewalling for your
network and you're using ipv6.

%if %{build_devel}
%package	devel
Summary:	Development package for iptables
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	kernel-headers

%description devel
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.
%endif

%prep

%setup -q

cp %{SOURCE1} iptables.init
cp %{SOURCE2} ip6tables.init
cp %{SOURCE3} iptables.sample
cp %{SOURCE4} ip6tables.sample

%patch0 -p1 -b .libiptc

# extensions
install -m0644 %{SOURCE100} extensions/
install -m0644 %{SOURCE101} extensions/

%patch100 -p0
%patch101 -p0
# (oe) P10 comes from iptables-1.3.7, was removed in iptables-1.3.8
%patch102 -p1 -b .psd

chmod +x extensions/.*-test

find . -type f | xargs perl -pi -e "s,/usr/local,%{_prefix},g"

%build
%serverbuild
export CFLAGS="${CFLAGS:-%{optflags}}"
export OPT="$CFLAGS -DNDEBUG -DNETLINK_NFLOG=5"

# (cg) the old kernel-headers tarball contained the folder
# linux-2.6-pom so we emulate that here...
# Can we tidy this whole thing up and not use a /lib/iptables symplink?
for i in linux-2.6-pom
	do find extensions -name '*.[ao]' -o -name '*.so' | xargs rm -f
	make LD=gcc COPT_FLAGS="$OPT" KBUILD_OUTPUT=/usr/src/linux KERNEL_DIR=/usr/src/linux LIBDIR=/lib all
	rm -fr $i/extensions
	mkdir -p $i/extensions
	mv extensions/*.so $i/extensions
done

# make more devel libs (debian)
ar rcs libiptables.a iptables.o
ar rcs libip6tables.a ip6tables.o

%install
rm -rf %{buildroot}
%serverbuild
export CFLAGS="${CFLAGS:-%{optflags}}"
export OPT="$CFLAGS -DNDEBUG -DNETLINK_NFLOG=5"

# Dunno why this happens. -- Geoff
%makeinstall_std \
    COPT_FLAGS="$OPT" \
    LD=gcc \
    BINDIR=/sbin \
    LIBDIR=/lib \
    MANDIR=%{_mandir} \
    KERNEL_DIR=%{_prefix} \
    install install-experimental

%if %{build_devel}
make \
    DESTDIR=%{buildroot} \
    COPT_FLAGS="$OPT" \
    LD=gcc \
    BINDIR=/sbin \
    LIBDIR=%{_libdir} \
    INCDIR=%{_includedir} \
    MANDIR=%{_mandir} \
    KERNEL_DIR=%{_prefix} \
    install-devel 

# static development files
install -d %{buildroot}%{_libdir}
install -m0644 libiptc/libiptc.a %{buildroot}%{_libdir}/libiptc.a
install -m0644 libiptables.a %{buildroot}%{_libdir}/
install -m0644 libip6tables.a %{buildroot}%{_libdir}/

# header development files
install -d %{buildroot}%{_includedir}/{libipq,libiptc,libipulog}
install -m0644 include/ip6tables.h %{buildroot}%{_includedir}/
install -m0644 include/xtables.h %{buildroot}%{_includedir}/
install -m0644 include/iptables.h %{buildroot}%{_includedir}/
install -m0644 include/libipq/*.h %{buildroot}%{_includedir}/libipq/
install -m0644 include/libiptc/*.h %{buildroot}%{_includedir}/libiptc/
install -m0644 include/libipulog/*.h %{buildroot}%{_includedir}/libipulog/
%endif

rm -rf %{buildroot}/lib/iptables
for i in linux-2.6-pom; do
	mkdir -p %{buildroot}/lib/iptables.d/$i
done
for i in linux-2.6-pom/extensions/*.so; do
	for j in %{buildroot}/lib/iptables.d/*; do
		if [ -e %{buildroot}/lib/iptables.d/${i%%%/*}/${i##*/} ]; then
			:
		elif cmp -s $i $j/${i##*/}; then
			ln $j/${i##*/} %{buildroot}/lib/iptables.d/${i%%%/*}/
		else
			cp $i %{buildroot}/lib/iptables.d/${i%%%/*}/
		fi
	done
done

install -d %{buildroot}%{_initrddir}
install -m0755 iptables.init %{buildroot}%{_initrddir}/iptables
install -m0755 ip6tables.init %{buildroot}%{_initrddir}/ip6tables

%clean
rm -rf %{buildroot}

%post
%_post_service iptables
# run only on fresh installation
if [ $1 = 1 ]; then
    /sbin/service iptables check
fi

%triggerpostun -- iptables < 1.2.9-8mdk
# fix upgrade from mdk < 10.2
/sbin/service iptables check

%preun
%_preun_service iptables

%post ipv6
%_post_service ip6tables

%preun ipv6
%_preun_service ip6tables

%files
%defattr(-,root,root,0755)
%doc INSTALL INCOMPATIBILITIES iptables.sample
%{_initrddir}/iptables
/sbin/iptables
/sbin/iptables-save
/sbin/iptables-restore
/sbin/iptables-xml
%{_mandir}/*/iptables*
%dir /lib/iptables.d
%dir /lib/iptables.d/*
/lib/iptables.d/*/libipt*
/lib/iptables.d/*/libxt*

%files ipv6
%defattr(-,root,root,0755)
%doc INSTALL INCOMPATIBILITIES ip6tables.sample
%{_initrddir}/ip6tables
/sbin/ip6tables
/sbin/ip6tables-save
/sbin/ip6tables-restore
%{_mandir}/*/ip6tables*
%dir /lib/iptables.d
%dir /lib/iptables.d/*
/lib/iptables.d/*/libip6t*

%if %{build_devel}
%files devel
%defattr(-,root,root,0755)
%{_includedir}/*.h
%dir %{_includedir}/libipq/
%dir %{_includedir}/libiptc/
%dir %{_includedir}/libipulog/
%{_includedir}/libipq/*.h
%{_includedir}/libiptc/*.h
%{_includedir}/libipulog/*.h
%{_libdir}/libipq.a
%{_libdir}/libiptc.a
%{_libdir}/libiptables.a
%{_libdir}/libip6tables.a
%{_mandir}/man3/*
%endif
