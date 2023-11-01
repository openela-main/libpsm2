#
#  This file is provided under a dual BSD/GPLv2 license.  When using or
#  redistributing this file, you may do so under either license.
#
#  GPL LICENSE SUMMARY
#
#  Copyright(c) 2015 Intel Corporation.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of version 2 of the GNU General Public License as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  Contact Information:
#  Intel Corporation, www.intel.com
#
#  BSD LICENSE
#
#  Copyright(c) 2015 Intel Corporation.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#    * Neither the name of Intel Corporation nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2014-2015 Intel Corporation. All rights reserved.
#
Summary: Intel PSM Libraries
Name: libpsm2
Version: 11.2.230
Release: 1%{?dist}.1
License: BSD or GPLv2
URL: https://github.com/cornelisnetworks/opa-psm2/

Source0: https://github.com/cornelisnetworks/opa-psm2/archive/refs/tags/PSM2_%{version}.tar.gz

# The OPA product is supported on x86_64 only:
ExclusiveArch: x86_64
BuildRequires: libuuid-devel
BuildRequires: numactl-devel
BuildRequires: systemd
BuildRequires: gcc
BuildRequires: make
Obsoletes: hfi1-psm < 1.0.0

%package devel
Summary: Development files for Intel PSM
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libuuid-devel

%package compat
Summary: Compat library for Intel PSM
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: systemd-udev

%global _privatelibs libpsm_infinipath[.]so[.]1.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
The PSM Messaging API, or PSM API, is the low-level
user-level communications interface for the Intel OPA
family of products. PSM users are enabled with mechanisms
necessary to implement higher level communications
interfaces in parallel environments.

%description devel
Development files for the Intel PSM library

%description compat
Support for MPIs linked with PSM versions < 2

%prep
%setup -q -n opa-psm2-PSM2_%{version}

%build
%{set_build_flags}
%{make_build}

%install
%if 0%{?fedora}
export DISTRO=fedora
%endif
%if 0%{?rhel}
export DISTRO=rhel
%endif
%make_install
rm -f %{buildroot}%{_libdir}/*.a

%ldconfig_scriptlets

%files
%license COPYING
%{_libdir}/libpsm2.so.2.*
%{_libdir}/libpsm2.so.2
%if 0%{?rhel} >= 8
%{_udevrulesdir}/40-psm.rules
%endif


%files devel
%{_libdir}/libpsm2.so
%{_includedir}/psm2.h
%{_includedir}/psm2_mq.h
%{_includedir}/psm2_am.h
%{_includedir}/hfi1diag

%files compat
%{_libdir}/psm2-compat
%{_udevrulesdir}/40-psm-compat.rules
%{_prefix}/lib/libpsm2
%if 0%{?fedora}
%{_prefix}/lib/modprobe.d/libpsm2-compat.conf
%endif
%if 0%{?rhel} >= 8
%{_sysconfdir}/modprobe.d/libpsm2-compat.conf
%endif

%changelog
* Wed Feb 08 2023 Michal Schmidt <mschmidt@redhat.com> - 11.2.230-1.1
- Disable the gating test that does not work without hfi1 hardware.
- Resolves: rhbz#2110923

* Fri Feb 03 2023 Michal Schmidt <mschmidt@redhat.com> - 11.2.230-1
- Rebase to upstream release 11.2.230
- Resolves: rhbz#2110923

* Tue Dec 07 2021 Honggang Li <honli@redhat.com> - 11.2.206-1
- Rebase to latest upstream release 11.2.206
- Resolves: bz1989162

* Wed Oct 28 2020 Honggang Li <honli@redhat.com> - 11.2.185-1
- Rebase to latest upstream release 11.2.185
- Resolves: bz1821736

* Thu Apr 09 2020 Honggang Li <honli@redhat.com> - 11.2.91-1
- Rebase to latest upstream release 11.2.91
- Resolves: bz1739284

* Tue Oct 29 2019 Honggang Li <honli@redhat.com> - 11.2.86-1
- Rebase to latest upstream release 11.2.86
- Resolves: bz1719681

* Mon Sep 24 2018 Honggang Li <honli@redhat.com> - 10.3.58-2
- Fix corrupted libpsm2 debuginfo file
- Resolves: bz1630766

* Fri Jun 22 2018 Honggang Li <honli@redhat.com> - 10.3.58-1
- Rebase to latest upstream release 10.3.58.
- Resolves: bz1594073

* Thu Mar 15 2018 - 10.3.8-5
- Fix partial injection of Fedora build flags.
- Double the sizeof array fdesc to fix a gcc compiling issue.
- Resolves: bz1556062

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan  4 2018 Honggang Li <honli@redhat.com> - 10.3.8-3
- Filter PSM1 library as private library
- Resolves: bz1530979

* Fri Dec 15 2017 Honggang Li <honli@redhat.com> - 10.3.8-2
- Minor enhancement
- Resolves: bz1526261

* Tue Dec 12 2017 Honggang Li <honli@redhat.com> - 10.3.8-1
- Rebase to latest upstream release
- Resolves: bz1524846

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.103_1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.103_1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 13 2017 Honggang Li <honli@redhat.com> - 10.2.103_1-1
- Rebase to latest upstream master branch.
- Fix build failures caught by gcc 7.x.
- Resolves: bz1423872

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 13 2016 Michal Schmidt <mschmidt@redhat.com> - 10.2.2-2
- Remove redundant %%setup -n argument.
- Packaging Guidelines: Never use "(R)" in description.

* Tue Jun 07 2016 Paul Reger <paul.j.reger@intel.com> - 10.2.2-1
- Fix build failures only.

* Tue Apr 05 2016 Paul Reger <paul.j.reger@intel.com> - 10.2.1-1
- Upstream PSM2 source code for Fedora.
