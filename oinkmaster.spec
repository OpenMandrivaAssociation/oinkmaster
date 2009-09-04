Summary:	A script that will help you update and manage your Snort rules
Name:		oinkmaster
Version:	2.1
Release:	%mkrel 2.20080218.2
License:	BSD
Group:		Networking/Other
URL:		http://oinkmaster.sourceforge.net/
Source0:	%{name}-%{version}-20080218.tar.gz
Source1:	oinkmaster-update
Source2:	oinkmaster.sysconfig
Patch0:		oinkmaster-man_page_fix.diff
Patch1:		oinkmaster-mdv_conf.diff
Requires:	openssh-clients
Requires:	snort
Requires:	snort-rules
Requires:	wget
Requires:	perl(IO::Zlib)
Requires:	perl(Archive::Tar)
Requires:	perl(LWP::UserAgent)
BuildArch:	noarch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Oinkmaster is a script that will help you update and manage your Snort rules.
It is released under the BSD license and will work on most platforms that can
run Perl scripts, e.g. Linux, *BSD, Windows, Mac OS X, Solaris, etc. Oinkmaster
can be used to update and manage the VRT licensed rules, the community rules,
the bleeding-snort rules and other third party rules, including your own local
rules. 

%package	gui
Summary:	A graphical front-end to Oinkmaster
Group:		Networking/Other
Requires:	%{name} >= %{version}

%description	gui
A graphical front-end to Oinkmaster written in Perl/Tk. See README.gui for
complete documentation.

%prep

%setup -q
%patch0 -p0
%patch1 -p0

cp %{SOURCE1} oinkmaster-update
cp %{SOURCE2} oinkmaster.sysconfig

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/cron.daily
install -d %{buildroot}%{_sysconfdir}/snort/backup
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}%{_mandir}/man1

install -m0755 %{name}.pl %{buildroot}%{_sbindir}/%{name}
install -m0640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -m0644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

install -m0755 oinkmaster-update %{buildroot}%{_sysconfdir}/cron.daily/oinkmaster-update
install -m0640 oinkmaster.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/oinkmaster

pushd contrib
    for i in *.pl; do
	new_name=`echo $i|sed -e 's/\.pl//'`
	install -m0755 $i %{buildroot}%{_sbindir}/%{name}-$new_name
    done
popd

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root)
%doc ChangeLog FAQ INSTALL LICENSE README README.templates template-examples.conf UPGRADING contrib/README*
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755,root,root) %{_sysconfdir}/cron.daily/oinkmaster-update
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/oinkmaster
%attr(0755,root,root) %dir %{_sysconfdir}/snort/backup
%{_sbindir}/%{name}
%{_sbindir}/%{name}-addmsg
%{_sbindir}/%{name}-addsid
%{_sbindir}/%{name}-create-sidmap
%{_sbindir}/%{name}-makesidex
%{_mandir}/man1/oinkmaster.1*
%attr(0755,root,root) %dir %{_localstatedir}/lib/%{name}

%files gui
%defattr(-,root,root)
%doc README.gui
%{_sbindir}/%{name}-oinkgui

