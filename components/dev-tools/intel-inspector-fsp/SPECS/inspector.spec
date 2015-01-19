%{!?PROJ_DELIM: %define PROJ_DELIM %{nil}}
%define pname inspector

Summary:   Intel(R) Inspector XE
Name:      intel-%{pname}%{PROJ_DELIM}
Version:   15.1.2.379161
Source0:   intel-%{pname}%{PROJ_DELIM}-%{version}.tar.gz
Source1:   FSP_macros
Release:   1
License:   Copyright (C) 2014 Intel Corporation. All rights reserved.
Vendor:    Intel Corporation
URL:       http://www.intel.com/software/products/
Group:     Development/Tools
BuildArch: x86_64
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
AutoReq:   no

%include %{_sourcedir}/FSP_macros

%define __spec_install_post /usr/lib/rpm/brp-strip-comment-note /bin/true
%define __spec_install_post /usr/lib/rpm/brp-compress /bin/true
%define __spec_install_post /usr/lib/rpm/brp-strip /bin/true

#!BuildIgnore: post-build-checks rpmlint-Factory
%define debug_package %{nil}

%define package_target /opt/fsp/pub/%{pname}/%{version}

%description

FSP collection of the Intel(R) Inspector memory and thread debugging tools.

%prep

%build

%install

%{__mkdir} -p %{buildroot}/
cd %{buildroot}
%{__tar} xfz %{SOURCE0}
cd -

# FSP module file
%{__mkdir} -p %{buildroot}/%{FSP_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{FSP_MODULES}/%{pname}/%{version}
#%Module1.0#####################################################################
proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the Intel(R) Inspector environment:"
puts stderr " "
puts stderr "Version %{version}"
puts stderr " "

}

module-whatis "Name: Intel(R) Inspector XE"
module-whatis "Version: %{version}"
module-whatis "Category: debug tools"
module-whatis "Description: Intel(R) Inspector memory and thread debugger"
module-whatis "URL: https://software.intel.com/en-us/intel-inspector-xe"

set     version                 %{version}

setenv          INSPECTOR_DIR   %{package_target}
setenv          INSPECTOR_LIB   %{package_target}/lib64
prepend-path    MANPATH         %{package_target}/man 
prepend-path    PATH            %{package_target}/bin64
prepend-path    LD_LIBRARY_PATH %{package_target}/lib64

EOF

%{__cat} << EOF > %{buildroot}/%{FSP_MODULES}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
set     ModulesVersion      "%{version}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{FSP_HOME}

%changelog

