%global Intel_release 8

Name:    opa-ff
Epoch: 1
Version: 10.3.1.0
Release: 11%{?dist}
Summary: Intel Omni-Path basic tools and libraries for fabric management
Group: System Environment/Libraries
License: BSD
Url: https://github.com/01org/opa-ff
# tarball created by:
# git clone https://github.com/01org/opa-ff.git
# cd opa-ff
# git checkout v10_3_1
# git archive --format=tar --prefix=opa-ff-%{version}-%{Intel_release}/ \
# 282ce603a6a6b132e2ca783b349ac501d271fb34 | xz > opa-ff-%{version}-%{Intel_release}.tar.xz
Source: %{name}-%{version}-%{Intel_release}.tar.xz

Patch0005: 0001-Add-literal-format-strings-into-snprintf-function.patch
Patch0006: 0001-Add-shebang-for-exp-scripts.patch
Patch0007: update-ff-install-script.patch

BuildRequires: gcc-c++
BuildRequires: zlib-devel, openssl-devel, tcl-devel, ncurses-devel
BuildRequires: libibumad-devel, libibverbs-devel, libibmad-devel, ibacm-devel, expat-devel
BuildRequires: perl

ExclusiveArch: x86_64

%description
Intel Omni-Path basic tools and libraries for fabric management.

%package -n opa-basic-tools
Summary: OPA management level tools and scripts
Group: System Environment/Libraries
Requires: rdma
Requires: bc
Requires: tcl%{?_isa}

%description -n opa-basic-tools
Contains basic tools for fabric management necessary on all compute nodes.

%package -n opa-address-resolution
Summary: OPA Address Resolution manager
Group: System Environment/Libraries
Requires: opa-basic-tools%{?_isa} = %{epoch}:%{version}-%{release}

%description -n opa-address-resolution
OPA Address Resolution manager.

%package -n opa-fastfabric
Summary: Management level tools and scripts
Group: System Environment/Libraries
Requires: opa-basic-tools%{?_isa} = %{epoch}:%{version}-%{release}

%description -n opa-fastfabric
Contains tools for managing fabric on a management node.

%prep
%setup -q -n %{name}-%{version}-%{Intel_release}
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1

find . -type f -name '*.[ch]' -exec 'chmod' 'a-x' '{}' ';'
find . -type f -name '*.exp'  -exec 'chmod' 'a+x' '{}' ';'

# Make it possible to override hardcoded compiler flags
sed -i -r -e 's/(release_C(C)?OPT_Flags\s*)=/\1?=/' Makerules/Target.LINUX.GNU.*

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
export release_COPT_Flags='%{optflags}'
export release_CCOPT_Flags='%{optflags}'

cd OpenIb_Host
./ff_build.sh %{_builddir} $FF_BUILD_ARGS


%install
BUILDDIR=%{_builddir} DESTDIR=%{buildroot} LIBDIR=%{_libdir} ./OpenIb_Host/ff_install.sh

%post -n opa-address-resolution -p /sbin/ldconfig
%postun -n opa-address-resolution -p /sbin/ldconfig


%files -n opa-basic-tools -f %{_builddir}/basic_file.list
%license LICENSE
%dir %{_prefix}/lib/opa/tools

%files -n opa-fastfabric -f %{_builddir}/ff_file.list
%license LICENSE
%{_sysconfdir}/sysconfig/opa/opamon.si.conf
# Replace opamon.si.conf, as it's a template config file.
%config(noreplace) %{_sysconfdir}/sysconfig/opa/opafastfabric.conf
%config(noreplace) %{_sysconfdir}/sysconfig/opa/opamon.conf
%config(noreplace) %{_sysconfdir}/sysconfig/opa/allhosts
%config(noreplace) %{_sysconfdir}/sysconfig/opa/chassis
%config(noreplace) %{_sysconfdir}/sysconfig/opa/esm_chassis
%config(noreplace) %{_sysconfdir}/sysconfig/opa/hosts
%config(noreplace) %{_sysconfdir}/sysconfig/opa/ports
%config(noreplace) %{_sysconfdir}/sysconfig/opa/switches
%config(noreplace) %{_sysconfdir}/sysconfig/opa/opaff.xml
%config(noreplace) %{_prefix}/lib/opa/tools/osid_wrapper
%dir %{_sysconfdir}/sysconfig/opa
%dir %{_prefix}/lib/opa/*
%{_sbindir}/opafmconfigcheck
%{_sbindir}/opafmconfigdiff


%files -n opa-address-resolution
%license LICENSE
%{_bindir}/opa_osd_dump
%{_bindir}/opa_osd_exercise
%{_bindir}/opa_osd_perf
%{_bindir}/opa_osd_query
%{_libdir}/ibacm
%{_libdir}/libopasadb.so.*
%{_includedir}/infiniband
%{_mandir}/man1/opa_osd_dump.1*
%{_mandir}/man1/opa_osd_exercise.1*
%{_mandir}/man1/opa_osd_perf.1*
%{_mandir}/man1/opa_osd_query.1*
%config(noreplace) %{_sysconfdir}/rdma/dsap.conf

%changelog
* Wed May 17 2017 Honggang Li <honli@redhat.com> - 10.3.1.0-11
- Don't change the hard-coded path names.
- Resolves: bz1450776

* Thu Mar 23 2017 Honggang Li <honli@redhat.com> - 10.3.1.0-10
- Fix dependency issue for opa-fastfabric and opa-address-resolution.
- Resolves: bz1434001

* Fri Mar 17 2017 Honggang Li <honli@redhat.com> - 10.3.1.0-9
- Rebase to latest upstream branch v10_3_1 as required.
- Clean up change log.
- Apply Epoch tag.
- Resolves: bz1382796

* Mon Aug 29 2016 Honggang Li <honli@redhat.com> - 10.1.0.0-127
- Fix one hardcode path issue.
- Resolves: bz1368383

* Thu Aug 18 2016 Honggang Li <honli@redhat.com> - 10.1.0.0-126
- Rebase to latest upstream release.
- Resolves: bz1367938

* Fri May 27 2016 Honggang Li <honli@redhat.com> - 10.0.1.0-2
- Rebase to latest upstream release.
- Related: bz1273153

* Mon Sep 28 2015 Honggang Li <honli@redhat.com> - 10.0.0.0-440
- Fix scripts that use well-known temp files
- Related: bz1262326

* Wed Sep 23 2015 Honggang Li <honli@redhat.com> - 10.0.0.0-439
- Fix various /tmp races
- Resolves: bz1262326

* Tue Sep 15 2015 Michal Schmidt <mschmidt@redhat.com> - 10.0.0.0-438
- Include the LICENSE file in both subpackages.

* Wed Aug 26 2015 Michal Schmidt <mschmidt@redhat.com> - 10.0.0.0-437
- Respect optflags.
- Related: bz1173309

* Tue Aug 25 2015 Michal Schmidt <mschmidt@redhat.com> - 10.0.0.0-436
- Update to new upstream snapshot with unbundled 3rd party software.
- Follow upstream spec file changes.
- Related: bz1173309

* Wed Aug 19 2015 Michal Schmidt <mschmidt@redhat.com> - 10.0.0.0-435
- Initial RHEL package based on upstream spec and input from Honggang Li.

* Fri Oct 10 2014 Erik E. Kahn <erik.kahn@intel.com> - 1.0.0-ifs
- Initial version
