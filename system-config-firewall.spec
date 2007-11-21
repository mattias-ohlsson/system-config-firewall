Summary: A graphical interface for basic firewall setup
Name: system-config-firewall
Version: 1.0.11
Release: 1%{?dist}
URL: http://fedora.redhat.com/projects/config-tools/
License: GPLv2+
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Source0: %{name}-%{version}.tar.bz2
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: intltool
Obsoletes: system-config-securitylevel
Provides: system-config-securitylevel = 1.7.0
Requires: pygtk2
Requires: python
Requires: usermode >= 1.36
Requires: system-config-firewall-tui = %{version}-%{release}
Requires: hicolor-icon-theme
Requires: pygtk2-libglade
Requires: gtk2 >= 2.6

%description
system-config-firewall is a graphical user interface for basic firewall setup.

%package tui
Summary: A text interface for basic firewall setup
Group: System Environment/Base
Obsoletes: lokkit
Obsoletes: system-config-securitylevel-tui
Provides: lokkit = 1.7.0
Provides: system-config-securitylevel-tui = 1.7.0
Requires: iptables >= 1.2.8
Requires: iptables-ipv6
Requires: system-config-network-tui
Requires: rhpl
Requires: newt
Requires: libselinux >= 1.19.1

%description tui
system-config-firewall-tui is a text and commandline user
interface for basic firewall setup.

%prep
%setup -q

%install
rm -rf %{buildroot}

make install INSTROOT=%{buildroot}

desktop-file-install --vendor system --delete-original \
	--dir %{buildroot}%{_datadir}/applications \
	--add-category X-Red-Hat-Base \
	%{buildroot}%{_datadir}/applications/system-config-firewall.desktop

%find_lang %{name} --all-name

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/system-config-firewall
%{_bindir}/system-config-securitylevel
%{_datadir}/system-config-firewall/system-config-firewall.py*
%dir %{_datadir}/system-config-securitylevel
%dir %{_datadir}/system-config-securitylevel/pixmaps
%dir %{_datadir}/firstboot/modules
%defattr(0644,root,root)
%{_datadir}/system-config-firewall/fw_gui.*
%{_datadir}/system-config-firewall/gtk_*
%{_datadir}/system-config-firewall/*.glade
%{_datadir}/system-config-firewall/*.png
%{_datadir}/applications/system-config-firewall.desktop
%{_datadir}/icons/hicolor/48x48/apps/system-config-firewall.png
%{_datadir}/icons/hicolor/48x48/apps/system-config-securitylevel.png
%config /etc/security/console.apps/system-config-firewall
%config /etc/security/console.apps/system-config-securitylevel
%config /etc/pam.d/system-config-firewall
%config /etc/pam.d/system-config-securitylevel
%{_datadir}/system-config-securitylevel/*.*
%{_datadir}/system-config-securitylevel/pixmaps/*.*
%{_datadir}/firstboot/modules/firstboot_selinux.py*
%{_datadir}/firstboot/modules/securitylevel.py*

%files -f %{name}.lang tui
%defattr(-,root,root)
%doc COPYING
%{_sbindir}/lokkit
%{_bindir}/system-config-firewall-tui
%dir %{_datadir}/system-config-firewall
%defattr(0644,root,root)
%{_datadir}/system-config-firewall/etc_services.*
%{_datadir}/system-config-firewall/fw_config.*
%{_datadir}/system-config-firewall/fw_functions.*
%{_datadir}/system-config-firewall/fw_iptables.*
%{_datadir}/system-config-firewall/fw_parser.*
%{_datadir}/system-config-firewall/fw_selinux.*
%{_datadir}/system-config-firewall/fw_services.*
%{_datadir}/system-config-firewall/fw_sysconfig.*
%{_datadir}/system-config-firewall/fw_sysctl.*
%{_datadir}/system-config-firewall/fw_tui.*
%ghost %config(missingok,noreplace) /etc/sysconfig/system-config-firewall
%ghost %config(missingok,noreplace) /etc/sysconfig/system-config-securitylevel

%changelog
* Wed Nov 21 2007 Thomas Woerner <twoerner@redhat.com> 1.0.11-1
- fixed crash on startup for network device aliases (rhbz#384891)
  thanks to Loran Freval for the patch
- added port entry max length in other ports dialog (rhbz#385931)
- added version number to about dialog (rhbz#387891)
- improved some english texts (rhbz#383741)
  thanks to Paul W. Frields for the initial patch
- code cleanup with start speedup
- do not allow to add custm rules for ipv6:nat
- also translate parser error messages

* Fri Nov  9 2007 Thomas Woerner <twoerner@redhat.com> 1.0.10-1
- fixed problem with network devices (rhbz#331671)
- dropped obsolete translation no.po (rhbz#332331)

* Mon Nov  5 2007 Thomas Woerner <twoerner@redhat.com> 1.0.9-1
- do not report configuration failed if ipv6 is disabled (rhbz#355561)
- print messages if lokkit failed
- lokkit be more verbose on restarting ipXtables in verbose mode

* Fri Oct 26 2007 Thomas Woerner <twoerner@redhat.com> 1.0.8-2
- lokkit: write new config with nostart option (rhbz#353961)
- translation fixes for de, it, nb, sr@latin

* Mon Oct  1 2007 Thomas Woerner <twoerner@redhat.com> 1.0.8-1
- use extension match for protocols (rhbz#229879)
- use ipv6-icmp instead of icmpv6 (rhbz#291001)
- use ':' in tui as port/proto delimiter for other ports (rhbz#292171)
- some translation fixes

* Tue Sep 25 2007 Thomas Woerner <twoerner@redhat.com> 1.0.7-1
- new translations
- added openvpn to services (rhbz#)
- fixed typo in description text for ipsec
- using port numbers instead of port names for services
- renamed some variables to be consistent
- make tolltip better: bigger text, helper modules
- dropped unused code: inconsistent handling
- make port check button inactive in add_port_cb
- new function _addDevice: code cleanup
- allow to set variables in ipXtablesConfig, which were not set before
- fixed os.system calls in ipXtablesClass to return proper return values
- fixed status funciton in ipXtablesClass
- new _append_unique function in fw_parser to prevent duplicates
- added warning dialog for missing or unusable /etc/sysconfig/ip*tables files
- fixed expand of the warning label in the startup dialog

* Wed Sep 12 2007 Thomas Woerner <twoerner@redhat.com> 1.0.6-1
- dropped --stop option from fw_gui::genArgs
- new translations
- sysctl support for masquerading (net.ipv4.ip_forward will be set)
- glade file: fixed spacings, dropped not needed containers

* Wed Sep  5 2007 Thomas Woerner <twoerner@redhat.com> 1.0.5-4
- fixed problem if /etc/sysconfig/system-config-securtylevel and 
  /etc/sysconfig/system-config-firewall are not readable

* Fri Aug 31 2007 Thomas Woerner <twoerner@redhat.com> 1.0.5-3
- fixed problem if IP*TABLES_MODULES is not set in config files

* Fri Aug 31 2007 Thomas Woerner <twoerner@redhat.com> 1.0.5-2
- fixed lokkit problem if selinux configuration is not available (rhbz#269601)

* Thu Aug 30 2007 Thomas Woerner <twoerner@redhat.com> 1.0.5-1
- more translations
- fixed IPsec description
- fixed po file generation to use xgettext only

* Wed Aug 22 2007 Thomas Woerner <twoerner@redhat.com> 1.0.4-1
- more translations
- build environment changes
- dropped build stage, because it is not needed at all

* Tue Aug 21 2007 Thomas Woerner <twoerner@redhat.com> 1.0.3-1
- added missing system-config-securitylevel compatibility files
- string and documentation fixes
- fixed typos reported by Alain Portal
- more translations
- fixed buildroot
- cleanup and changes according to review (rhbz#253232)
- moved doc to tui sub package

* Fri Aug 17 2007 Thomas Woerner <twoerner@redhat.com> 1.0.2-2
- fixed license headers for GPLv2+

* Thu Aug 16 2007 Thomas Woerner <twoerner@redhat.com> 1.0.2-1
- obsolete and provide system-config-securitylevel package
- added compat files for anaconda, firstboot and system-config-kickstart
- lokkit fixes for nostart option:
  - only write config for iptables and ip6tables if enabled
  - stop iptables and ip6tables if disabled
  - unlink iptables and ip6tables rule files if disabled
- lokkit: new option --update to regenerate firewall configuration if not 
  disabled
- check for include files only when writing firewall configuration
- clean buildroot in install
- made system-config-securitylevel a synonym for system-config-firewall
- ip6tables: reject with icmp6-adm-prohibited instead of icmp6-port-unreachable
  (rhbz#250915)
- moved config files from /etc/sysconfig into tui sub package
- removed x bit from import files

* Mon Jul 23 2007 Thomas Woerner <twoerner@redhat.com> 1.0.1-2
- fixed disabled string in fw_gui
- set mode after copying of ip*tables-config to 0600
- fixed categories in desktop file

* Mon Jun  4 2007 Thomas Woerner <twoerner@redhat.com> 1.0.1-1
- fixed startup and description texts
- added missing requirement for system-config-network-tui
- moved base python files into tui sub package
- fixed requirements
- made package noarch

* Fri Jun  1 2007 Thomas Woerner <twoerner@redhat.com> 1.0.0-1
- initial package
