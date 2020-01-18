Name:    opa-ff
Version: 10.1.0.0
Release: 127%{?dist}
Summary: Intel Omni-Path basic tools and libraries for fabric management
Group: System Environment/Libraries
License: BSD
Url: https://github.com/01org/opa-ff
# tarball created by:
# git clone https://github.com/01org/opa-ff.git
# cd opa-ff
# git archive --format=tar --prefix=opa-ff-10.1.0.0/ 25636a4fa3d1785f776197498059ade2fef19d52 | xz > opa-ff-10.1.0.0.tar.xz
Source: %{name}-%{version}.tar.xz

# RHEL packaging rules do not allow install files in /opt.
Patch0001: 0001-Replace-hardcode-path-opt-opafm-with-usr-lib-opa-fm.patch
Patch0002: 0002-Replace-var-opt-opafm-with-var-lib-opa-fm.patch
Patch0003: 0003-Replace-var-opt-opa-with-var-lib-opa-ff.patch
Patch0004: 0004-Replace-opt-opa-with-usr-lib-opa-ff.patch

Patch0005: 0001-Add-literal-format-strings-into-snprintf-function.patch
Patch0006: 0001-Add-shebang-for-exp-scripts.patch

BuildRequires: autoconf, automake, gcc-c++
BuildRequires: zlib-devel, openssl-devel, tcl-devel, ncurses-devel
BuildRequires: libibumad-devel, libibverbs-devel, libibmad-devel, ibacm-devel, expat-devel

ExclusiveArch: x86_64

%description
Intel Omni-Path basic tools and libraries for fabric management.

%package -n opa-basic-tools
Summary: OPA management level tools and scripts
Group: System Environment/Libraries

%description -n opa-basic-tools
Contains basic tools for fabric management necessary on all compute nodes.

%package -n opa-address-resolution
Summary: OPA Address Resolution manager
Group: System Environment/Libraries
Requires: opa-basic-tools%{?_isa} = %{version}-%{release}

%description -n opa-address-resolution
OPA Address Resolution manager.

%package -n opa-fastfabric
Summary: Management level tools and scripts
Group: System Environment/Libraries
Requires: opa-basic-tools%{?_isa} = %{version}-%{release}

%description -n opa-fastfabric
Contains tools for managing fabric on a management node.

%prep
%setup -q
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1

find . -type f -name '*.[ch]' -exec 'chmod' 'a-x' '{}' ';'
find . -type f -name '*.exp'  -exec 'chmod' 'a+x' '{}' ';'

# Make it possible to override hardcoded compiler flags
sed -i -r -e 's/(release_C(C)?OPT_Flags\s*)=/\1?=/' Makerules/Target.LINUX.GNU.*

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
export release_COPT_Flags='%{optflags}'
export release_CCOPT_Flags='%{optflags}'
./ff_build.sh %{_builddir} $FF_BUILD_ARGS


%install
%global basic_tools_sbin opacapture opafabricinfo opagetvf opagetvf_env opahfirev opapacketcapture opaportinfo oparesolvehfiport opasaquery opasmaquery opainfo opatmmtool

%global basic_tools_sbin_sym opapmaquery opaportconfig

%global basic_tools_opt setup_self_ssh usemem opaipcalc

%global basic_mans opacapture.1 opaconfig.1 opafabricinfo.1 opagetvf.1 opagetvf_env.1 opahfirev.1 opainfo.1 opapacketcapture.1 opapmaquery.1 opaportconfig.1 opaportinfo.1 oparesolvehfiport.1 opasaquery.1 opashowmc.1 opasmaquery.1 opatmmtool.1

%global ff_tools_opt opaswquery opaswconfigure opaswfwconfigure opaswfwupdate opaswfwverify opaswping opaswreset

%global ff_tools_exp basic.exp chassis.exp chassis_configure.exp chassis_fmconfig.exp chassis_fmcontrol.exp chassis_fmgetconfig.exp chassis_getconfig.exp chassis_reboot.exp chassis_fmgetsecurityfiles.exp chassis_fmsecurityfiles.exp chassis_upgrade.exp common_funcs.exp configipoib.exp extmng.exp ff_function.exp ib.exp opa_to_xml.exp ibtools.exp install.exp ipoibping.exp load.exp mpi.exp mpiperf.exp mpiperfdeviation.exp network.exp proc_mgr.exp reboot.exp sacache.exp sm_control.exp switch_capture.exp switch_configure.exp switch_dump.exp switch_fwverify.exp switch_getconfig.exp switch_hwvpd.exp switch_info.exp switch_ping.exp switch_reboot.exp switch_upgrade.exp target.exp tools.exp upgrade.exp tclIndex tcl_proc comm12 front

%global ff_tools_sbin opacabletest opacheckload opaextracterror opaextractlink opaextractperf opaextractstat opaextractstat2 opafindgood opafirmware opagenchassis opagenesmchassis opagenswitches opalinkanalysis opareport opareports opasorthosts opatop opaxlattopology opaxlattopology_cust opaxmlextract opaxmlfilter opaxmlgenerate opaxmlindent opaallanalysis opacaptureall opachassisanalysis opacmdall opadownloadall opaesmanalysis opafabricanalysis opafastfabric opahostsmanalysis opadisablehosts opadisableports opaenableports opaledports opaexpandfile opaextractbadlinks opaextractlids opaextractsellinks opaswenableall opaswdisableall opaverifyhosts opahostadmin opachassisadmin opaswitchadmin opapingall opascpall opasetupssh opashowallports opauploadall opapaquery opashowmc opafequery

%global ff_tools_misc ff_funcs opachassisip opagenswitcheshelper chassis_setup switch_setup opagetipaddrtype opafastfabric.conf.def show_counts

%global ff_tools_fm config_generate config_diff config_check config_convert

%global ff_libs_misc libqlgc_fork.so

%global ff_mans opaallanalysis.8 opacabletest.8 opacaptureall.8 opachassisadmin.8 opachassisanalysis.8 opacheckload.8 opacmdall.8 opadisablehosts.8 opadisableports.8 opadownloadall.8 opaenableports.8 opaledports.8 opaesmanalysis.8 opaexpandfile.8 opaextractbadlinks.8 opaextracterror.8 opaextractlids.8 opaextractlink.8 opaextractperf.8 opaextractsellinks.8 opaextractstat.8 opaextractstat2.8 opafabricanalysis.8 opafastfabric.8 opafequery.8 opafindgood.8 opafmconfigcheck.8 opafmconfigdiff.8 opagenchassis.8 opagenesmchassis.8 opagenswitches.8 opagentopology.8 opahostadmin.8 opahostsmanalysis.8 opalinkanalysis.8 opapaquery.8 opapingall.8 opareport.8 opareports.8 opascpall.8 opasetupssh.8 opashowallports.8 opasorthosts.8 opaswitchadmin.8 opatop.8 opauploadall.8 opaverifyhosts.8 opaxlattopology.8 opaxlattopology_cust.8 opashowmc.8 opaxmlextract.8 opaxmlfilter.8 opaxmlgenerate.8 opaxmlindent.8 opaswdisableall.8 opaswenableall.8

%global ff_iba_samples hostverify.sh opatopology_FIs.txt opatopology_links.txt opatopology_SMs.txt opatopology_SWs.txt linksum_swd06.csv linksum_swd24.csv README.topology README.xlat_topology topology_cust.xlsx topology.xlsx allhosts-sample chassis-sample hosts-sample switches-sample ports-sample opaff.xml-sample mac_to_dhcp filterFile.txt triggerFile.txt opamon.conf-sample opamon.si.conf-sample opafastfabric.conf-sample opa_ca_openssl.cnf-sample opa_comp_openssl.cnf-sample opagentopology esm_chassis-sample

%global help_doc opatop_group_bw.hlp opatop_group_config.hlp opatop_group_err.hlp opatop_group_focus.hlp opatop_group_info_sel.hlp opatop_img_config.hlp opatop_pm_config.hlp opatop_port_stats.hlp opatop_summary.hlp opatop_vf_bw.hlp opatop_vf_info_sel.hlp opatop_vf_config.hlp

%global opasadb_bin opa_osd_dump opa_osd_exercise opa_osd_perf opa_osd_query

%global opasadb_header opasadb_path.h opasadb_route.h opasadb_route2.h

%global opasadb_mans opa_osd_dump.1 opa_osd_exercise.1 opa_osd_perf.1 opa_osd_query.1

%global shmem_apps_files Makefile mpi_hosts.sample prepare_run README select_mpi run_barrier run_get_bibw run_get_bw run_get_latency run_put_bibw run_put_bw run_put_latency run_reduce run_hello run_alltoall run_rand shmem-hello.c

%global release_string IntelOPA-Tools-FF.$BUILD_TARGET_OS_ID.$MODULEVERSION

#rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/usr/lib/opa-ff/{tools,fm_tools,help,samples}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ibacm
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rdma
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/opa
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/opa
mkdir -p $RPM_BUILD_ROOT%{_includedir}/infiniband
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8


#Binaries and scripts installing (basic tools)
#cd builtbin.OPENIB_FF.release
cd $(cat %{_builddir}/RELEASE_PATH)

cd bin
cp -t $RPM_BUILD_ROOT%{_sbindir} %basic_tools_sbin 
cp -t $RPM_BUILD_ROOT/usr/lib/opa-ff/tools/ %basic_tools_opt
ln -s ./opaportinfo $RPM_BUILD_ROOT%{_sbindir}/opaportconfig
ln -s ./opasmaquery $RPM_BUILD_ROOT%{_sbindir}/opapmaquery

cd ../opasadb
cp -t $RPM_BUILD_ROOT%{_bindir} %opasadb_bin
cp -t $RPM_BUILD_ROOT%{_includedir}/infiniband %opasadb_header

cd ../bin
cp -t $RPM_BUILD_ROOT/usr/lib/opa-ff/tools/ %ff_tools_opt

cd ../fastfabric
cp -t $RPM_BUILD_ROOT%{_sbindir} %ff_tools_sbin
cp -t $RPM_BUILD_ROOT/usr/lib/opa-ff/tools/ %ff_tools_misc
cp -t $RPM_BUILD_ROOT/usr/lib/opa-ff/help %help_doc

cd ../etc
cp -t $RPM_BUILD_ROOT/usr/lib/opa-ff/fm_tools/ %ff_tools_fm
ln -s /usr/lib/opa-ff/fm_tools/config_check $RPM_BUILD_ROOT%{_sbindir}/opafmconfigcheck
ln -s /usr/lib/opa-ff/fm_tools/config_diff $RPM_BUILD_ROOT%{_sbindir}/opafmconfigdiff

cd ../fastfabric/samples
cp -t $RPM_BUILD_ROOT/usr/lib/opa-ff/samples %ff_iba_samples
cd ..

cd ../fastfabric/tools
cp -t $RPM_BUILD_ROOT/usr/lib/opa-ff/tools/ %ff_tools_exp
cp -t $RPM_BUILD_ROOT/usr/lib/opa-ff/tools/ %ff_libs_misc
cp -t $RPM_BUILD_ROOT/usr/lib/opa-ff/tools/ osid_wrapper
cp -t $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/opa allhosts chassis esm_chassis hosts ports switches opaff.xml
cd ..

cd ../man/man1
cp -t $RPM_BUILD_ROOT%{_mandir}/man1 %basic_mans
cp -t $RPM_BUILD_ROOT%{_mandir}/man1 %opasadb_mans
cd ../man8
cp -t $RPM_BUILD_ROOT%{_mandir}/man8 %ff_mans
cd ..

#Config files
cd ../config
cp -t $RPM_BUILD_ROOT%{_sysconfdir}/rdma dsap.conf
cp -t $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/opa opamon.conf opamon.si.conf

#Libraries installing
#cd ../builtlibs.OPENIB_FF.release
cd $(cat %{_builddir}/LIB_PATH)
cp -t $RPM_BUILD_ROOT%{_libdir} libopasadb.so.*
cp -t $RPM_BUILD_ROOT%{_libdir}/ibacm libdsap.so.*

# Now that we've put everything in the buildroot, copy any default config files to their expected location for user
# to edit. To prevent nuking existing user configs, the files section of this spec file will reference these as noreplace
# config files.
cp $RPM_BUILD_ROOT/usr/lib/opa-ff/tools/opafastfabric.conf.def $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/opa/opafastfabric.conf

#Now we do a bunch of work to build the file listing of what belongs to each RPM

#Basic tools sbin
echo "%{_sbindir}/%{basic_tools_sbin} %{basic_tools_sbin_sym}" > %{_builddir}/basic_sbin_file.list
sed -i 's;[ ];\n%{_sbindir}/;g' %{_builddir}/basic_sbin_file.list 

#Basic tools opt
echo "/usr/lib/opa-ff/tools/%{basic_tools_opt}" > %{_builddir}/basic_opt_file.list
sed -i 's;[ ];\n/usr/lib/opa-ff/tools/;g' %{_builddir}/basic_opt_file.list 

#Basic man pages
echo "%{_mandir}/man1/%{basic_mans}" > %{_builddir}/basic_mans.list
sed -i 's;[ ];\n%{_mandir}/man1/;g' %{_builddir}/basic_mans.list
sed -i 's;\.1;\.1*;g' %{_builddir}/basic_mans.list

#FF tools opt
echo "/usr/lib/opa-ff/tools/%{ff_tools_opt}" > %{_builddir}/ff_opt_file.list
sed -i 's;[ ];\n/usr/lib/opa-ff/tools/;g' %{_builddir}/ff_opt_file.list

#FF exp files opt
echo "/usr/lib/opa-ff/tools/%{ff_tools_exp}" > %{_builddir}/ff_tools_exp.list
sed -i 's;[ ];\n/usr/lib/opa-ff/tools/;g' %{_builddir}/ff_tools_exp.list

#FF misc files opt
echo "/usr/lib/opa-ff/tools/%{ff_tools_misc}" > %{_builddir}/ff_tools_misc.list
sed -i 's;[ ];\n/usr/lib/opa-ff/tools/;g' %{_builddir}/ff_tools_misc.list

#FF libs misc
echo "/usr/lib/opa-ff/tools/%{ff_libs_misc}" > %{_builddir}/ff_libs_misc.list
sed -i 's;[ ];\n/usr/lib/opa-ff/tools/;g' %{_builddir}/ff_libs_misc.list

#FF iba samples
echo "/usr/lib/opa-ff/samples/%{ff_iba_samples}" > %{_builddir}/ff_iba_samples.list
sed -i 's;[ ];\n/usr/lib/opa-ff/samples/;g' %{_builddir}/ff_iba_samples.list

#FF tools to FM configuration
echo "/usr/lib/opa-ff/fm_tools/%{ff_tools_fm}" > %{_builddir}/ff_tools_fm.list
sed -i 's;[ ];\n/usr/lib/opa-ff/fm_tools/;g' %{_builddir}/ff_tools_fm.list

#FF man pages
echo "/usr/share/man/man8/%{ff_mans}" > %{_builddir}/ff_mans.list
sed -i 's;[ ];\n/usr/share/man/man8/;g' %{_builddir}/ff_mans.list
sed -i 's;\.8;\.8*;g' %{_builddir}/ff_mans.list

#Final file listing for 'basic'
cat %{_builddir}/basic_sbin_file.list %{_builddir}/basic_opt_file.list %{_builddir}/basic_mans.list > %{_builddir}/basic_file.list

#FF tools help doc
echo "/usr/lib/opa-ff/help/%{help_doc}" > %{_builddir}/ff_help_file.list
sed -i 's;[ ];\n/usr/lib/opa-ff/help/;g' %{_builddir}/ff_help_file.list

#FF tools sbin
echo "%{_sbindir}/%{ff_tools_sbin}" > %{_builddir}/ff_sbin_file.list
sed -i 's;[ ];\n%{_sbindir}/;g' %{_builddir}/ff_sbin_file.list

#Final file listing for 'ff'
cat %{_builddir}/ff_sbin_file.list %{_builddir}/ff_help_file.list %{_builddir}/ff_tools_exp.list %{_builddir}/ff_tools_misc.list %{_builddir}/ff_libs_misc.list %{_builddir}/ff_iba_samples.list %{_builddir}/ff_mans.list %{_builddir}/ff_tools_fm.list %{_builddir}/ff_opt_file.list > %{_builddir}/ff_file.list


%post -n opa-address-resolution -p /sbin/ldconfig
%postun -n opa-address-resolution -p /sbin/ldconfig


%files -n opa-basic-tools -f %{_builddir}/basic_file.list
%license LICENSE
%dir %{_prefix}/lib/opa-ff/tools

%files -n opa-fastfabric -f %{_builddir}/ff_file.list
%license LICENSE
%{_sysconfdir}/sysconfig/opa/opamon.si.conf
%config(noreplace) %{_sysconfdir}/sysconfig/opa/opafastfabric.conf
%config(noreplace) %{_sysconfdir}/sysconfig/opa/opamon.conf
%config(noreplace) %{_sysconfdir}/sysconfig/opa/allhosts
%config(noreplace) %{_sysconfdir}/sysconfig/opa/chassis
%config(noreplace) %{_sysconfdir}/sysconfig/opa/esm_chassis
%config(noreplace) %{_sysconfdir}/sysconfig/opa/hosts
%config(noreplace) %{_sysconfdir}/sysconfig/opa/ports
%config(noreplace) %{_sysconfdir}/sysconfig/opa/switches
%config(noreplace) %{_sysconfdir}/sysconfig/opa/opaff.xml
%config(noreplace) %{_prefix}/lib/opa-ff/tools/osid_wrapper
%{_sbindir}/opafmconfigcheck
%{_sbindir}/opafmconfigdiff
%dir %{_sysconfdir}/sysconfig/opa
%dir %{_prefix}/lib/opa-ff/*


%files -n opa-address-resolution
%license LICENSE
#Everything under the bin directory belongs exclusively to opasadb at this time.
%{_bindir}/*
%{_libdir}/ibacm/libdsap.so*
%{_libdir}/libopasadb.so*
%{_includedir}/*
%{_mandir}/man1/opa_osd_dump.1*
%{_mandir}/man1/opa_osd_exercise.1*
%{_mandir}/man1/opa_osd_perf.1*
%{_mandir}/man1/opa_osd_query.1*
%config(noreplace) %{_sysconfdir}/rdma/dsap.conf

%changelog
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
