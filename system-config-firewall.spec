Summary: A graphical interface for basic firewall setup
Name: system-config-firewall
Version: 1.2.14
Release: 1%{?dist}
URL: http://fedorahosted.org/system-config-firewall
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
Requires: usermode-gtk >= 1.94
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

%build
%configure

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

desktop-file-install --vendor system --delete-original \
	--dir %{buildroot}%{_datadir}/applications \
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

%triggerpostun -- %{name} < 1.1.0
%{_datadir}/system-config-firewall/convert-config

%triggerpostun -- system-config-securitylevel
%{_datadir}/system-config-firewall/convert-config

%files
%defattr(-,root,root)
%{_bindir}/system-config-firewall
%{_datadir}/system-config-firewall/system-config-firewall.py*
%defattr(0644,root,root)
%{_datadir}/system-config-firewall/fw_gui.*
%{_datadir}/system-config-firewall/gtk_*
%{_datadir}/system-config-firewall/*.glade
%{_datadir}/system-config-firewall/wizard_*.png
%{_datadir}/system-config-firewall/wizard.svg
%{_datadir}/applications/system-config-firewall.desktop
%{_datadir}/icons/hicolor/*/apps/preferences-system-firewall.*
%config /etc/security/console.apps/system-config-firewall
%config /etc/pam.d/system-config-firewall

%files -f %{name}.lang tui
%defattr(-,root,root)
%doc COPYING
%{_sbindir}/lokkit
%{_bindir}/system-config-firewall-tui
%{_datadir}/system-config-firewall/convert-config
%dir %{_datadir}/system-config-firewall
%defattr(0644,root,root)
%{_datadir}/system-config-firewall/etc_services.*
%{_datadir}/system-config-firewall/fw_compat.*
%{_datadir}/system-config-firewall/fw_config.*
%{_datadir}/system-config-firewall/fw_functions.*
%{_datadir}/system-config-firewall/fw_icmp.*
%{_datadir}/system-config-firewall/fw_iptables.*
%{_datadir}/system-config-firewall/fw_parser.*
%{_datadir}/system-config-firewall/fw_selinux.*
%{_datadir}/system-config-firewall/fw_services.*
%{_datadir}/system-config-firewall/fw_sysconfig.*
%{_datadir}/system-config-firewall/fw_sysctl.*
%{_datadir}/system-config-firewall/fw_tui.*
%ghost %config(missingok,noreplace) /etc/sysconfig/system-config-firewall

%changelog
* Fri Mar 27 2009 Thomas Woerner <twoerner@redhat.com> 1.2.14-1
- new build environment using configure, autofoo and intltool
- fixed typo in router-solicitation description (rhbz#490979)
- new themable application icon: preferences-system-firewall (rhbz#454402)
- make backup copies before overwriting files (rhbz#437374)
- updated translations: 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.13-3
- Rebuild for Python 2.6

* Tue Oct 28 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-2
- fixed system-config-firewall-tui path (rhbz#457485)

* Tue Oct 28 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-1
- fixed two typos in fw_icmp (rhbz#467334)
- added ability to sort custom rules files (rhbz#467696)
- fixed modified test in sysctl writer: fixes rhbz#462325
  also removed quotes around values for new keys
- some build fixes
- updated translations for: as, de, fi, fr, he, hi, ko, hu, it, ja, ko, ml,
                            pl, pt_BR, ru, sk, sr, sr@latin, sv, ta, te, 
                            zh_CN, zh_TW

* Tue Oct 21 2008 Thomas Woerner <twoerner@redhat.com> 1.2.12-2
- require usermode-gtk instead of usermode

* Tue Oct  7 2008 Thomas Woerner <twoerner@redhat.com> 1.2.12-1
- only provide lang files in tui sub-package (rhbz#465572)
- updated translations for: as, bn_IN, ca, cs, es, fr, gu, it, ja, kn, mr, nl,
                            pa, or, pl, pt_BR, sk, zh_CN, zh_TW

* Fri Sep 19 2008 Thomas Woerner <twoerner@redhat.com> 1.2.11-1
- use dialogs for parser errors in tui (rhbz#457485)
- enable to add protocol specific (IPv4, IPv6) icmp types for ICMP filtering
- updated translations for he, ja, ko and zh_CN

* Tue Jul  8 2008 Thomas Woerner <twoerner@redhat.com> 1.2.10-1
- lokkit: fixed path for system-config-firewall-tui (rhbz#454108)
- updated translations for: it, fr, nl, ru, sr, sr@latin

* Wed Jun 11 2008 Thomas Woerner <twoerner@redhat.com> 1.2.9-1
- fixed format string to silence inttool
- new remider to check if the ip*tables services are enabled
- use proper dialog functions in the tui
- updated translations: cs, de, es, gu, pl

* Fri May 23 2008 Thomas Woerner <twoerner@redhat.com> 1.2.8-1
- new tui interface
- new system-config-firewall-tui
- new client services for ipp and samba
- lokkit: fixed disabling of firewall in force mode (rhbz#443411)
- disabled port forwarding for IPv6
- some minor fixes and enhancements

* Thu Apr  3 2008 Thomas Woerner <twoerner@redhat.com> 1.2.7-1
- fixed crash if encoding is not UTF-8 (rhbz#439902)
- updated translations: bn_IN, cs, de, es, fi, fr, gu, hi, it, kn, ko, ml,
                        mr, pa, pl, pt_BR, ru, sr, sr@latin, ta, te, zh_CN

* Tue Mar  4 2008 Thomas Woerner <twoerner@redhat.com> 1.2.6-1
- new ICMP filter to block specified ICMP types
- fixed minor problem in lokkit (initialize old_config)
- set starting diretory for custom rules files to /etc/sysconfig
- more build environment changes for git
- use gtk.CellRendererToggle instead of own CellRendererCheck
- several parser changes for transparent error handling and output
- some minor enhancements
- translation updates

* Wed Feb 20 2008 Thomas Woerner <twoerner@redhat.com> 1.2.5-1
- dropped system-config-securitylevel compatibility files
- project moved to git.fedoraproject.org

* Thu Feb 14 2008 Thomas Woerner <twoerner@redhat.com> 1.2.4-1
- fixed overwrite problem if IPTABLES_SAVE_ON_RESTART is set (rhbz#431961)
- use SELECTION_NONE for trustedView 

* Mon Feb 11 2008 Thomas Woerner <twoerner@redhat.com> 1.2.3-2
- fixed usermode version (rhbz#428392)

* Fri Feb  8 2008 Thomas Woerner <twoerner@redhat.com> 1.2.3-1
- fixed traceback for empty configuration use in life installer (rhbz#430963)
- use config-util for userhelper configuration (rhbz#428392)
- mark dirty after applying new default configuration
- do not overwrite attributes filename and converted in config
- use new shared ChooserButton
- fixed forward dialog and labels to use current dialog width
- use tempfile.mkdtemp for better security
- updated translations: fi, fr, it, ja, nl, pt_BR, sr and sr@latin

* Fri Feb  1 2008 Thomas Woerner <twoerner@redhat.com> 1.2.2-1
- fixed icmp handling for ip6tables in FORWARD chain
- do state established, related test early in FORWARD chain
- fixed typo in address for port-forwarding
- added IPv4 only message to masquerading and port-forwarding for lokkit
- updated translations: es, pl

* Thu Jan 31 2008 Thomas Woerner <twoerner@redhat.com> 1.2.1-1
- fixed traceback for clean selinux configuration (rhbz#430963)
- fixed icmp handling for ip6tables
- updated translations: as, de, it, ja, pl, pt_BR, zh_CN

* Fri Jan 25 2008 Thomas Woerner <twoerner@redhat.com> 1.2.0-1
- added port forwarding
- using INPUT chain in table filter instead of RH-Firewall-1-INPUT
- fixed masquerading
- rewrite of firewall generation code
- trusted hosts now also allowed for FORWARD
- lots of bug fixes
- gui enhancements

* Wed Jan 16 2008 Thomas Woerner <twoerner@redhat.com> 1.1.3-2
- added fw_compat files to files section

* Tue Jan 15 2008 Thomas Woerner <twoerner@redhat.com> 1.1.3-1
- new fw_compat, used in config-convert and fw_sysconfig to automatically 
  convert old system-config-securitylevel configurations
- new wizard look
- fixed range check for user defined ports
- some code cleanup
- updated translations for fi, fr and ja

* Mon Jan  7 2008 Thomas Woerner <twoerner@redhat.com> 1.1.2-1
- fw_gui: fixed row activation for masquerading
- fw_gui: fixed _setInterfaces to use internal functions to correctly set
  toggles
- fw_gui: show info dialog if no config exists and firewall gets enabled: new
  function enableFirewall
- fw_gui, fw_tui: disable firewall if no config exists
- fw_gui, fw_tui: do not print traceback if NCDeviceList.getDeviceList raises
  and exception
- forward masqueraded connections
- gtk_cellrenderercheck: fixed size calculations
- fw_sysconfig: set config.filename to None for merged configuration in
  read_sysconfig_config if no configuration exists
- new translations

* Fri Dec 21 2007 Thomas Woerner <twoerner@redhat.com> 1.1.1-1
- use radio buttons for skill menu entries to show active level
- fixed convert-config problem if there is no configuration to convert
  (rhbz#426477)
- minor string changes
- new it and pt_BR translations

* Thu Dec 20 2007 Thomas Woerner <twoerner@redhat.com> 1.1.0-1
- new default configurations: server, desktop
- cleanup of wizard: dropped network connection tab
- new option in wizard to keep configuration or load a default configuration
- new menu entry and dialog to configure iptables and ip6tables service settings
- some enhancements to the gtk_cellrenderercheck for better look and feel

* Fri Dec 14 2007 Thomas Woerner <twoerner@redhat.com> 1.1.0-0
- ports are ports and services are services: there is a new service tag to
  enable services; a port is not enabling a service anymore
- new conversion tool for 1.0.X to 1.1.X configuration
- new version option for lokkit
- wizard
  - dropped network connection selection tab
  - using keep configuration check instead of clear configuration check
  - added default configuration selection
- gui: new menu for skill level and load default configuration
- use choices in optparse, removed obsolete check functions

* Thu Dec 13 2007 Thomas Woerner <twoerner@redhat.com> 1.0.12-2
- fixed lokkit command problem for non english languages
- using latest translations

* Mon Dec 10 2007 Thomas Woerner <twoerner@redhat.com> 1.0.12-1
- allow to activate checkboxes by row activation in treeviews
- code cleanup in view_toggle_cb
- fixed port display for IPSec
- use system icons where possible, new wizard icons
- added fallback for CellRendererCheck if icons are missing, size fixes
- added tooltips for toolbar and menu entries (if needed)
- improved more english texts (rhbz#395801)
  thanks to Paul W. Frields for the initial patch

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
