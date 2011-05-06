Name:           ec2-api-tools
Version:        1.4.2.4
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
Requires:       jakarta-commons-cli 
Requires:       commons-codec 
Requires:       jakarta-commons-discovery 
Requires:       commons-httpclient 
Requires:       jakarta-commons-logging 
Requires:       jaf 
Requires:       bcprov 
Requires:       bea-stax-api 
Requires:       javamail 
Requires:       jdom 
Requires:       log4j 
Requires:       wsdl4j 
Requires:       xalan-j2 
Requires:       ws-jaxme

BuildArch:      noarch

%description
The command-line tools serve as the client interface to the Amazon EC2 web
service. Use these tools to register and launch instances, manipulate
security groups, and more.


%prep
%setup -q


%build
# Drop jars that are distributable by Fedora
xargs rm -f <<EOF
lib/activation-1.1.jar
lib/commons-cli-1.1.jar
lib/commons-codec-1.3.jar
lib/mail-1.4.jar
lib/stax-api-1.0.1.jar
lib/log4j-1.2.14.jar
lib/commons-logging-api-1.1.1.jar
lib/commons-httpclient-3.1.jar
lib/bcprov-jdk15-145.jar
lib/commons-discovery.jar
lib/commons-logging-adapters-1.1.1.jar
lib/jaxb-api.jar
lib/jdom.jar
lib/wsdl4j.jar
lib/xalan.jar
lib/serializer.jar
EOF

: TODO <<EOF
lib/wss4j-1.5.3.jar
lib/wstx-asl-3.2.7.jar
lib/xfire-all-1.2.6.jar
lib/xfire-jsr181-api-1.0-M1.jar
lib/xml-apis.jar
lib/XmlSchema-1.4.5.jar
lib/xmlsec.jar
lib/jets3t-0.8.0.jar
lib/j2ee_mail.jar
lib/java-xmlbuilder-0.4-SNAPSHOT.jar
lib/jaxb-impl.jar
lib/xercesImpl.jar
lib/jaxws-api.jar
EOF


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
* Fri May 06 2011 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.4.2.4-1
- New version

* Thu Apr 07 2011 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.3.53907-4
- Add a missing dependency

* Sat Aug 21 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.53907-3
- rebuilt

* Mon Aug 09 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.3.53907-2
- Reuse distribution JARs wherever possible

* Mon Aug 09 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.3.53907-1
- Update to 53907, support for Cluster Compute instances

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
