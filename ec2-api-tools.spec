%global major_version 1.3
%global minor_version 46266

Name:           ec2-api-tools
Version:        %{major_version}.%{minor_version}
Release:        1%{?dist}
Summary:        Amazon EC2 Command-Line Tools

Group:          Applications/Internet
License:        Redistributable, no modification permitted and LGPLv2 and ASL 2.0 and ASL 1.1 
# Just to avoid confusion, "ASL" above is Apache Software License
# "Redistributable" parts are covered by Amazon Software License
URL:            http://developer.amazonwebservices.com/connect/entry.jspa?externalID=351
Source0:        http://s3.amazonaws.com/ec2-downloads/%{name}.zip

Source1:        ec2-cmd
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       jpackage-utils
Requires:       java >= 1.5

BuildArch:      noarch

%description
The command-line tools serve as the client interface to the Amazon EC2 web
service. Use these tools to register and launch instances, manipulate
security groups, and more.


%prep
%setup -q -n %{name}-%{major_version}-%{minor_version}


%build


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}/ec2-api-tools
install -pm 644 lib/*.jar $RPM_BUILD_ROOT%{_javadir}/ec2-api-tools

install -d $RPM_BUILD_ROOT%{_bindir}

# Rewrite the wrappers
for FILE in $(ls bin/* |grep -v 'cmd$')
do
        TARGET=$RPM_BUILD_ROOT%{_bindir}/$(basename $FILE)
        METHOD=$(awk '/ec2-cmd/ {printf "%s", $2}' $FILE)

cat >$TARGET <<EOF
#!/bin/bash
exec ec2-cmd $METHOD "\$@"
EOF

        chmod 0755 $TARGET
        touch --reference $FILE $TARGET
done

# The bundled ec2-cmd is not suitable for us
install -pm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/ec2-cmd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_javadir}/ec2-api-tools
%doc THIRDPARTYLICENSE.TXT license.txt notice.txt


%changelog
* Fri Dec 18 2009 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.3.46266-1
- Update to 46266

* Wed Jul 15 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.3.36506-1
- Bump to newer upstream version
- Publising, remove profanity
- Don't depend on Sun Java specifically

* Thu Dec 11 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.3.30349-1
- New upstream release, support for European zones

* Tue Oct 7 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.3.24159-2
- Require Sun Java

* Tue Oct 7 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.3.24159-1
- Initial packaging attempt
