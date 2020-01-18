Name:    opa-ff
Epoch: 1
Version: 10.7.0.0.133
Release: 1%{?dist}
Summary: Intel Omni-Path basic tools and libraries for fabric management
License: BSD or GPLv2
Url: https://github.com/01org/opa-ff
# tarball created by:
# git clone https://github.com/01org/opa-ff.git
# cd opa-ff
# git archive --format=tar --prefix=opa-ff-%{version}/ \
# c6b993a4c724f7f3dd3f62a8a5371b0d170b7334 | xz > opa-ff-%{version}.tar.xz
Source: %{name}-%{version}.tar.xz

Patch0005: 0001-Add-literal-format-strings-into-snprintf-function.patch
Patch0006: 0001-Add-shebang-for-exp-scripts.patch
Patch0007: update-ff-install-script.patch

BuildRequires: gcc-c++
BuildRequires: openssl-devel, tcl-devel, ncurses-devel
BuildRequires: libibumad-devel, rdma-core-devel, libibmad-devel, ibacm-devel, expat-devel
BuildRequires: perl

ExclusiveArch: x86_64

%description
Intel Omni-Path basic tools and libraries for fabric management.

%package -n opa-basic-tools
Summary: OPA management level tools and scripts
Requires: rdma
Requires: bc
Requires: tcl%{?_isa}

%description -n opa-basic-tools
Contains basic tools for fabric management necessary on all compute nodes.

%package -n opa-address-resolution
Summary: OPA Address Resolution manager
Requires: opa-basic-tools%{?_isa}
Requires: ibacm

%description -n opa-address-resolution
This package contains the ibacm distributed SA provider (dsap) for
name and address resolution on OPA platform. It also contains the
library and tools to access the shared memory database exported
by dsap.

%package -n opa-fastfabric
Summary: Management level tools and scripts
Requires: opa-basic-tools%{?_isa}

%description -n opa-fastfabric
Contains tools for managing fabric on a management node.

%package -n opa-libopamgt
Summary: Omni-Path management API library
Requires: libibumad

%description -n opa-libopamgt
This package contains the library necessary to build applications
that interface with an Omni-Path FM.

%package -n opa-libopamgt-devel
Summary: Omni-Path library development headers
Requires: opa-libopamgt%{?_isa}

%description -n opa-libopamgt-devel
This package contains the necessary headers for opamgt development.

%prep
%setup -q
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
./ff_build.sh %{_builddir} $BUILD_ARGS


%install
BUILDDIR=%{_builddir} DESTDIR=%{buildroot} LIBDIR=%{_libdir} DSAP_LIBDIR=%{_libdir} ./OpenIb_Host/ff_install.sh

%post -n opa-address-resolution -p /sbin/ldconfig
%postun -n opa-address-resolution -p /sbin/ldconfig

%post -n opa-libopamgt -p /sbin/ldconfig
%postun -n opa-libopamgt -p /sbin/ldconfig

%files -n opa-basic-tools
%license LICENSE
%{_sbindir}/opacapture
%{_sbindir}/opafabricinfo
%{_sbindir}/opagetvf
%{_sbindir}/opagetvf_env
%{_sbindir}/opahfirev
%{_sbindir}/opaportinfo
%{_sbindir}/oparesolvehfiport
%{_sbindir}/opasaquery
%{_sbindir}/opasmaquery
%{_sbindir}/opainfo
%{_sbindir}/opapmaquery
%{_sbindir}/opaportconfig
%{_prefix}/lib/opa/tools/setup_self_ssh
%{_prefix}/lib/opa/tools/usemem
%{_prefix}/lib/opa/tools/opaipcalc
%{_prefix}/lib/opa/.comp_fastfabric.pl
%{_prefix}/lib/opa/.comp_oftools.pl
%{_mandir}/man1/opacapture.1.gz
%{_mandir}/man1/opaconfig.1.gz
%{_mandir}/man1/opafabricinfo.1.gz
%{_mandir}/man1/opagetvf.1.gz
%{_mandir}/man1/opagetvf_env.1.gz
%{_mandir}/man1/opahfirev.1.gz
%{_mandir}/man1/opainfo.1.gz
%{_mandir}/man1/opapmaquery.1.gz
%{_mandir}/man1/opaportconfig.1.gz
%{_mandir}/man1/opaportinfo.1.gz
%{_mandir}/man1/oparesolvehfiport.1.gz
%{_mandir}/man1/opasaquery.1.gz
%{_mandir}/man1/opasmaquery.1.gz
%{_prefix}/share/opa/samples/opamgt_tls.xml-sample
%config(noreplace) %{_sysconfdir}/opa/opamgt_tls.xml

%files -n opa-fastfabric
%license LICENSE
%{_sbindir}/opacabletest
%{_sbindir}/opacheckload
%{_sbindir}/opaextracterror
%{_sbindir}/opaextractlink
%{_sbindir}/opaextractperf
%{_sbindir}/opaextractstat
%{_sbindir}/opaextractstat2
%{_sbindir}/opafindgood
%{_sbindir}/opafirmware
%{_sbindir}/opagenchassis
%{_sbindir}/opagenesmchassis
%{_sbindir}/opagenswitches
%{_sbindir}/opalinkanalysis
%{_sbindir}/opareport
%{_sbindir}/opareports
%{_sbindir}/opasorthosts
%{_sbindir}/opatop
%{_sbindir}/opaxlattopology
%{_sbindir}/opaxmlextract
%{_sbindir}/opaxmlfilter
%{_sbindir}/opaxmlgenerate
%{_sbindir}/opaxmlindent
%{_sbindir}/opaallanalysis
%{_sbindir}/opacaptureall
%{_sbindir}/opachassisanalysis
%{_sbindir}/opacmdall
%{_sbindir}/opadownloadall
%{_sbindir}/opaesmanalysis
%{_sbindir}/opafabricanalysis
%{_sbindir}/opafastfabric
%{_sbindir}/opahostsmanalysis
%{_sbindir}/opadisablehosts
%{_sbindir}/opadisableports
%{_sbindir}/opaenableports
%{_sbindir}/opaledports
%{_sbindir}/opaexpandfile
%{_sbindir}/opaextractbadlinks
%{_sbindir}/opaextractlids
%{_sbindir}/opaextractsellinks
%{_sbindir}/opaextractmissinglinks
%{_sbindir}/opaswenableall
%{_sbindir}/opaswdisableall
%{_sbindir}/opaverifyhosts
%{_sbindir}/opahostadmin
%{_sbindir}/opachassisadmin
%{_sbindir}/opaswitchadmin
%{_sbindir}/opapingall
%{_sbindir}/opascpall
%{_sbindir}/opasetupssh
%{_sbindir}/opashowallports
%{_sbindir}/opauploadall
%{_sbindir}/opapaquery
%{_sbindir}/opashowmc
%{_sbindir}/opa2rm
%{_sbindir}/opafmconfigcheck
%{_sbindir}/opafmconfigdiff
%{_prefix}/lib/opa/tools/opaswquery
%{_prefix}/lib/opa/tools/opaswconfigure
%{_prefix}/lib/opa/tools/opaswfwconfigure
%{_prefix}/lib/opa/tools/opaswfwupdate
%{_prefix}/lib/opa/tools/opaswfwverify
%{_prefix}/lib/opa/tools/opaswping
%{_prefix}/lib/opa/tools/opaswreset
%{_prefix}/lib/opa/tools/ff_funcs
%{_prefix}/lib/opa/tools/opachassisip
%{_prefix}/lib/opa/tools/opagenswitcheshelper
%{_prefix}/lib/opa/tools/chassis_setup
%{_prefix}/lib/opa/tools/switch_setup
%{_prefix}/lib/opa/tools/opagetipaddrtype
%{_prefix}/lib/opa/tools/opafastfabric.conf.def
%{_prefix}/lib/opa/tools/show_counts
%{_prefix}/lib/opa/tools/basic.exp
%{_prefix}/lib/opa/tools/chassis.exp
%{_prefix}/lib/opa/tools/chassis_configure.exp
%{_prefix}/lib/opa/tools/chassis_fmconfig.exp
%{_prefix}/lib/opa/tools/chassis_fmcontrol.exp
%{_prefix}/lib/opa/tools/chassis_fmgetconfig.exp
%{_prefix}/lib/opa/tools/chassis_getconfig.exp
%{_prefix}/lib/opa/tools/chassis_reboot.exp
%{_prefix}/lib/opa/tools/chassis_fmgetsecurityfiles.exp
%{_prefix}/lib/opa/tools/chassis_fmsecurityfiles.exp
%{_prefix}/lib/opa/tools/chassis_upgrade.exp
%{_prefix}/lib/opa/tools/common_funcs.exp
%{_prefix}/lib/opa/tools/configipoib.exp
%{_prefix}/lib/opa/tools/extmng.exp
%{_prefix}/lib/opa/tools/ff_function.exp
%{_prefix}/lib/opa/tools/ib.exp
%{_prefix}/lib/opa/tools/opa_to_xml.exp
%{_prefix}/lib/opa/tools/ibtools.exp
%{_prefix}/lib/opa/tools/install.exp
%{_prefix}/lib/opa/tools/ipoibping.exp
%{_prefix}/lib/opa/tools/load.exp
%{_prefix}/lib/opa/tools/mpi.exp
%{_prefix}/lib/opa/tools/mpiperf.exp
%{_prefix}/lib/opa/tools/mpiperfdeviation.exp
%{_prefix}/lib/opa/tools/network.exp
%{_prefix}/lib/opa/tools/proc_mgr.exp
%{_prefix}/lib/opa/tools/reboot.exp
%{_prefix}/lib/opa/tools/sacache.exp
%{_prefix}/lib/opa/tools/sm_control.exp
%{_prefix}/lib/opa/tools/switch_capture.exp
%{_prefix}/lib/opa/tools/switch_configure.exp
%{_prefix}/lib/opa/tools/switch_dump.exp
%{_prefix}/lib/opa/tools/switch_fwverify.exp
%{_prefix}/lib/opa/tools/switch_getconfig.exp
%{_prefix}/lib/opa/tools/switch_hwvpd.exp
%{_prefix}/lib/opa/tools/switch_info.exp
%{_prefix}/lib/opa/tools/switch_ping.exp
%{_prefix}/lib/opa/tools/switch_reboot.exp
%{_prefix}/lib/opa/tools/switch_upgrade.exp
%{_prefix}/lib/opa/tools/target.exp
%{_prefix}/lib/opa/tools/tools.exp
%{_prefix}/lib/opa/tools/upgrade.exp
%{_prefix}/lib/opa/tools/tclIndex
%{_prefix}/lib/opa/tools/tcl_proc
%{_prefix}/lib/opa/tools/comm12
%{_prefix}/lib/opa/tools/front
%{_prefix}/lib/opa/tools/libqlgc_fork.so
%{_prefix}/share/opa/help/opatop_group_bw.hlp
%{_prefix}/share/opa/help/opatop_group_config.hlp
%{_prefix}/share/opa/help/opatop_group_ctg.hlp
%{_prefix}/share/opa/help/opatop_group_focus.hlp
%{_prefix}/share/opa/help/opatop_group_info_sel.hlp
%{_prefix}/share/opa/help/opatop_img_config.hlp
%{_prefix}/share/opa/help/opatop_pm_config.hlp
%{_prefix}/share/opa/help/opatop_port_stats.hlp
%{_prefix}/share/opa/help/opatop_summary.hlp
%{_prefix}/share/opa/help/opatop_vf_bw.hlp
%{_prefix}/share/opa/help/opatop_vf_info_sel.hlp
%{_prefix}/share/opa/help/opatop_vf_config.hlp
%{_prefix}/lib/opa/fm_tools/config_generate
%{_prefix}/lib/opa/fm_tools/config_diff
%{_prefix}/lib/opa/fm_tools/config_check
%{_prefix}/lib/opa/fm_tools/config_convert
%{_prefix}/share/opa/samples/hostverify.sh
%{_prefix}/share/opa/samples/opatopology_FIs.txt
%{_prefix}/share/opa/samples/opatopology_links.txt
%{_prefix}/share/opa/samples/opatopology_SMs.txt
%{_prefix}/share/opa/samples/opatopology_SWs.txt
%{_prefix}/share/opa/samples/linksum_swd06.csv
%{_prefix}/share/opa/samples/linksum_swd24.csv
%{_prefix}/share/opa/samples/README.topology
%{_prefix}/share/opa/samples/README.xlat_topology
%{_prefix}/share/opa/samples/minimal_topology.xlsx
%{_prefix}/share/opa/samples/detailed_topology.xlsx
%{_prefix}/share/opa/samples/allhosts-sample
%{_prefix}/share/opa/samples/chassis-sample
%{_prefix}/share/opa/samples/hosts-sample
%{_prefix}/share/opa/samples/switches-sample
%{_prefix}/share/opa/samples/ports-sample
%{_prefix}/share/opa/samples/mac_to_dhcp
%{_prefix}/share/opa/samples/filterFile.txt
%{_prefix}/share/opa/samples/triggerFile.txt
%{_prefix}/share/opa/samples/opamon.conf-sample
%{_prefix}/share/opa/samples/opamon.si.conf-sample
%{_prefix}/share/opa/samples/opafastfabric.conf-sample
%{_prefix}/share/opa/samples/opa_ca_openssl.cnf-sample
%{_prefix}/share/opa/samples/opa_comp_openssl.cnf-sample
%{_prefix}/share/opa/samples/opagentopology
%{_prefix}/share/opa/samples/esm_chassis-sample
%{_mandir}/man8/opaallanalysis.8.gz
%{_mandir}/man8/opacabletest.8.gz
%{_mandir}/man8/opacaptureall.8.gz
%{_mandir}/man8/opachassisadmin.8.gz
%{_mandir}/man8/opachassisanalysis.8.gz
%{_mandir}/man8/opacheckload.8.gz
%{_mandir}/man8/opacmdall.8.gz
%{_mandir}/man8/opadisablehosts.8.gz
%{_mandir}/man8/opadisableports.8.gz
%{_mandir}/man8/opadownloadall.8.gz
%{_mandir}/man8/opaenableports.8.gz
%{_mandir}/man8/opaledports.8.gz
%{_mandir}/man8/opaesmanalysis.8.gz
%{_mandir}/man8/opaexpandfile.8.gz
%{_mandir}/man8/opaextractbadlinks.8.gz
%{_mandir}/man8/opaextracterror.8.gz
%{_mandir}/man8/opaextractlids.8.gz
%{_mandir}/man8/opaextractlink.8.gz
%{_mandir}/man8/opaextractperf.8.gz
%{_mandir}/man8/opaextractsellinks.8.gz
%{_mandir}/man8/opaextractstat.8.gz
%{_mandir}/man8/opaextractstat2.8.gz
%{_mandir}/man8/opafabricanalysis.8.gz
%{_mandir}/man8/opafastfabric.8.gz
%{_mandir}/man8/opafindgood.8.gz
%{_mandir}/man8/opafmconfigcheck.8.gz
%{_mandir}/man8/opafmconfigdiff.8.gz
%{_mandir}/man8/opagenchassis.8.gz
%{_mandir}/man8/opagenesmchassis.8.gz
%{_mandir}/man8/opagenswitches.8.gz
%{_mandir}/man8/opagentopology.8.gz
%{_mandir}/man8/opahostadmin.8.gz
%{_mandir}/man8/opahostsmanalysis.8.gz
%{_mandir}/man8/opalinkanalysis.8.gz
%{_mandir}/man8/opapaquery.8.gz
%{_mandir}/man8/opapingall.8.gz
%{_mandir}/man8/opareport.8.gz
%{_mandir}/man8/opareports.8.gz
%{_mandir}/man8/opascpall.8.gz
%{_mandir}/man8/opasetupssh.8.gz
%{_mandir}/man8/opashowallports.8.gz
%{_mandir}/man8/opasorthosts.8.gz
%{_mandir}/man8/opaswitchadmin.8.gz
%{_mandir}/man8/opatop.8.gz
%{_mandir}/man8/opauploadall.8.gz
%{_mandir}/man8/opaverifyhosts.8.gz
%{_mandir}/man8/opaxlattopology.8.gz
%{_mandir}/man8/opashowmc.8.gz
%{_mandir}/man8/opaxmlextract.8.gz
%{_mandir}/man8/opaxmlfilter.8.gz
%{_mandir}/man8/opaxmlgenerate.8.gz
%{_mandir}/man8/opaxmlindent.8.gz
%{_mandir}/man8/opaswdisableall.8.gz
%{_mandir}/man8/opaswenableall.8.gz
%{_mandir}/man8/opafirmware.8.gz
%{_mandir}/man8/opaextractmissinglinks.8.gz
%{_mandir}/man8/opa2rm.8.gz
%{_sysconfdir}/opa/opamon.si.conf
# Replace opamon.si.conf, as it's a template config file.
%config(noreplace) %{_sysconfdir}/opa/opafastfabric.conf
%config(noreplace) %{_sysconfdir}/opa/opamon.conf
%config(noreplace) %{_sysconfdir}/opa/allhosts
%config(noreplace) %{_sysconfdir}/opa/chassis
%config(noreplace) %{_sysconfdir}/opa/esm_chassis
%config(noreplace) %{_sysconfdir}/opa/hosts
%config(noreplace) %{_sysconfdir}/opa/ports
%config(noreplace) %{_sysconfdir}/opa/switches
%config(noreplace) %{_prefix}/lib/opa/tools/osid_wrapper


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

%files -n opa-libopamgt
%{_prefix}/lib/libopamgt.*


%files -n opa-libopamgt-devel
%{_includedir}/opamgt


%changelog
* Thu Apr 19 2018 Honggang Li <honli@redhat.com> - 10.7.0.0.133-1
- Rebase to upstream release v10.7.0.0.133
- Delete opapacketcapture
- Resolves: bz1483552, bz1457762

* Thu Dec 28 2017 Honggang Li <honli@redhat.com> - 10.5.0.0.140-2
- Don't require a specific build version of opa-basic-tools.
- Resolves: bz1528687

* Thu Oct 19 2017 Honggang Li <honli@redhat.com> - 10.5.0.0.140-1
- Rebase to upstream release 10.5.0.0.140.
- Resolves: bz1452784

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
