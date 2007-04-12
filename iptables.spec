%define build_devel 1

Name:		iptables
Summary:	Tools for managing Linux kernel packet filtering capabilities
Version:	1.3.5
Release:	%mkrel 3

Source:		http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
Source1:	iptables.init
Source2:	ip6tables.init
Source3:	iptables.config
Source4:	ip6tables.config
# must be in a linux-$kmajor.$kminor-<foo> directory for "service iptables check"
Source5:	iptables-kernel-headers.tar.bz2

Patch1:		iptables-1.3.2-stealth_grsecurity.patch 
Patch2:		iptables-1.2.8-imq.patch 
Patch3:		iptables-1.2.8-libiptc.h.patch 
Patch4:		iptables-1.3.2-fix_extension_test.patch
Patch5:		iptables-1.3.2-ipp2p_extension.patch
Patch6:		iptables-1.3.3-IFWLOG_extension.patch

Group:		System/Kernel and hardware
URL:		http://netfilter.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
License:	GPL
BuildPrereq:	/usr/bin/perl
BuildRequires:  kernel-source >= 2.4.13-3mdk
Requires:	kernel >= 2.4.13
Provides:	userspace-ipfilter
Requires(post):		chkconfig, rpm-helper
Requires(preun):		chkconfig, rpm-helper
Conflicts:	ipchains

%description
iptables controls the Linux kernel network packet filtering code.
It allows you to set up firewalls and IP masquerading, etc.

Install iptables if you need to set up firewalling for your
network.

Install this only if you are using the 2.4 or 2.6 kernels!!

%package ipv6
Summary:	IPv6 support for iptables
Group:		System/Kernel and hardware
Requires:	%name = %version
Requires(post):		chkconfig, rpm-helper
Requires(preun):		chkconfig, rpm-helper

%description ipv6
IPv6 support for iptables.

iptables controls the Linux kernel network packet filtering code.
It allows you to set up firewalls and IP masquerading, etc.

IPv6 is the next version of the IP protocol.

Install iptables-ipv6 if you need to set up firewalling for your
network and you're using ipv6.

%if %{build_devel}
%package devel
Summary: Development package for iptables
Group:  Development/C
Requires: %{name} = %{version}

%description devel
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.
%endif

%prep
%setup -q -a 5
%patch1 -p1 -b .stealth
%patch2 -p1 -b .imq
%patch3 -p1 -b .libiptc
%patch4 -p1 -b .fix_extension_test
#%patch5 -p1 -b .ipp2p
%patch6 -p1 -b .IFWLOG
cp %{SOURCE3} iptables.sample
cp %{SOURCE4} ip6tables.sample

chmod +x extensions/.IMQ-test
#chmod +x extensions/.ipp2p-test
chmod +x extensions/.IFWLOG-test

find . -type f | xargs perl -pi -e "s,/usr/local,%{_prefix},g"

%build
%serverbuild
%ifarch alpha
OPT=`echo $RPM_OPT_FLAGS | sed -e "s/-O./-O1/"`
%else
OPT="$RPM_OPT_FLAGS -DNDEBUG"
%endif
for i in linux-2.6*
	do find extensions -name '*.[ao]' -o -name '*.so' | xargs rm -f
	make COPT_FLAGS="$OPT" KERNEL_DIR=$PWD/$i LIBDIR=/lib all
	rm -fr $i/extensions
	mkdir -p $i/extensions
	mv extensions/*.so $i/extensions
done
%install
rm -rf $RPM_BUILD_ROOT
# Dunno why this happens. -- Geoff
%makeinstall_std BINDIR=/sbin MANDIR=%{_mandir} LIBDIR=/lib COPT_FLAGS="$RPM_OPT_FLAGS -DNETLINK_NFLOG=4" KERNEL_DIR=/usr install-experimental
%if %{build_devel}
make install-devel DESTDIR=%{buildroot} KERNEL_DIR=/usr BINDIR=/sbin LIBDIR=%{_libdir} MANDIR=%{_mandir}
%endif
rm -fr %buildroot/lib/iptables
for i in linux-*; do
	mkdir -p %buildroot/lib/iptables.d/$i
done
for i in linux-*/extensions/*.so; do
	for j in %buildroot/lib/iptables.d/*; do
		if [ -e %buildroot/lib/iptables.d/${i%%%/*}/${i##*/} ]; then
			:
		elif cmp -s $i $j/${i##*/}; then
			ln $j/${i##*/} %buildroot/lib/iptables.d/${i%%%/*}/
		else
			cp $i %buildroot/lib/iptables.d/${i%%%/*}/
		fi
	done
done
install -c -D -m755 %{SOURCE1} %buildroot%{_initrddir}/iptables
install -c -D -m755 %{SOURCE2} %buildroot%{_initrddir}/ip6tables

%clean
rm -rf $RPM_BUILD_ROOT $RPM_BUILD_DIR/file.list.%{name}

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
%_preun_service iptables

%post ipv6
%_post_service ip6tables

%preun ipv6
%_preun_service ip6tables

%files
%defattr(-,root,root,0755)
%config(noreplace) %{_initrddir}/iptables
/sbin/iptables
/sbin/iptables-save
/sbin/iptables-restore
%{_mandir}/*/iptables*
%dir /lib/iptables.d
%dir /lib/iptables.d/*
/lib/iptables.d/*/libipt*
%doc INSTALL INCOMPATIBILITIES iptables.sample

%files ipv6
%defattr(-,root,root,0755)
%config(noreplace) %{_initrddir}/ip6tables
/sbin/ip6tables
/sbin/ip6tables-save
/sbin/ip6tables-restore
%{_mandir}/*/ip6tables*
%dir /lib/iptables.d
%dir /lib/iptables.d/*
/lib/iptables.d/*/libip6t*
%doc INSTALL INCOMPATIBILITIES ip6tables.sample

%if %{build_devel}
%files devel
%defattr(-,root,root,0755)
%{_includedir}/libipq.h
%{_libdir}/libipq.a
%{_libdir}/libiptc.a
%{_mandir}/man3/*
%endif

