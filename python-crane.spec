%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

# The release number 
%global release_number 0.1.alpha

# Create tag for the Source0 and setup
%global git_tag %{name}-%{version}-%{release_number}

Name: python-crane
Version: 2.2.0
Release: %{release_number}%{?dist}
Summary: docker-registry-like API with redirection, as a wsgi app

License: GPLv2
URL: https://github.com/pulp/crane
Source0: https://codeload.github.com/pulp/crane/tar.gz/%{git_tag}#/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools

Requires: python-flask >= 0.9
Requires: python-setuptools
Requires: python-rhsm
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
This wsgi application exposes a read-only API similar to docker-registry, which
docker can use for "docker pull" operations. Requests for actual image files
are responded to with 302 redirects to a URL formed with per-repository
settings.


%prep
%setup -q -n crane-%{git_tag}


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

mkdir -p %{buildroot}/%{_usr}/share/crane/
mkdir -p %{buildroot}/%{_var}/lib/crane/metadata/

cp deployment/crane.wsgi %{buildroot}/%{_usr}/share/crane/

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
cp deployment/apache24.conf %{buildroot}/%{_usr}/share/crane/apache.conf
cp deployment/crane.wsgi %{buildroot}/%{_usr}/share/crane/
%else
cp deployment/apache22.conf %{buildroot}/%{_usr}/share/crane/apache.conf
cp deployment/crane_el6.wsgi %{buildroot}/%{_usr}/share/crane/crane.wsgi
%endif

rm -rf %{buildroot}%{python2_sitelib}/tests


%files
%defattr(-,root,root,-)
%{python2_sitelib}/crane
%{python2_sitelib}/crane*.egg-info
%{_usr}/share/crane/
%dir %{_var}/lib/crane/
%dir %{_var}/lib/crane/metadata/
%doc AUTHORS COPYRIGHT LICENSE README.rst


%post
if /usr/sbin/selinuxenabled ; then
  if [ -d "%{_var}/lib/crane" ]; then
    semanage fcontext -a -t httpd_sys_content_t '%{_var}/lib/crane(/.*)?'
    restorecon -R -v %{_var}/lib/crane
  fi
fi

%postun
if [ $1 -eq 0 ] ; then  # final removal
  if /usr/sbin/selinuxenabled ; then
    if [ -d "%{_var}/lib/crane" ]; then
      semanage fcontext -d -t httpd_sys_content_t '%{_var}/lib/crane(/.*)?'
      restorecon -R -v %{_var}/lib/crane
    fi
  fi
fi


%changelog
* Mon Mar 14 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-1
- Bumping version to 2.0.0-1 (dkliban@redhat.com)

* Tue Mar 08 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-0.9.rc
- Bumping version to 2.0.0-0.9.rc (dkliban@redhat.com)

* Fri Mar 04 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-0.8.beta
- Bumping version to 2.0.0-0.8.beta (dkliban@redhat.com)

* Thu Mar 03 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-0.7.beta
- Bumping version to 2.0.0-0.7.beta (dkliban@redhat.com)

* Wed Mar 02 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-0.6.beta
- Fix bash syntax on selinuxenabled check (pcreech@redhat.com)
- Bumping version to 2.0.0-0.6.beta (dkliban@redhat.com)

* Fri Feb 19 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-0.5.beta
- Merge branch '2.0_release_notes' (rbarlow@redhat.com)
- Don't run selinux commands if selinux is disabled (pcreech@redhat.com)
- Add release notes for Crane 2.0. (rbarlow@redhat.com)
- Merge pull request #53 from twaugh/polling-dirs (rbarlow@redhat.com)
- Bumping version to 2.0.0-0.5.beta (dkliban@redhat.com)
- monitor: fix race condition (twaugh@redhat.com)
- Set followlinks=True when using os.walk() in monitor (twaugh@redhat.com)
- Fix data_dir polling when there are subdirectories (twaugh@redhat.com)

* Thu Jan 28 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-0.4.beta
- Bumping version to 2.0.0-0.4.beta (dkliban@redhat.com)

* Tue Jan 19 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-0.3.beta
- Bumping version to 2.0.0-0.3.beta (dkliban@redhat.com)

* Wed Jan 13 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-0.2.beta
- Bumping version to 2.0.0-0.2.beta (dkliban@redhat.com)

* Mon Jan 11 2016 Dennis Kliban <dkliban@redhat.com> 2.0.0-0.1.beta
- Bumping version to 2.0.0-0.1.beta (dkliban@redhat.com)
- Fix Docker image creation (elyezermr@gmail.com)
- Update Dockerfile (elyezermr@gmail.com)
- Merge branch '1.1-dev' (dkliban@redhat.com)
- Add fc23 to dist_list.txt config and removes fc21. (dkliban@redhat.com)
- Patch M2Crypto in Travis to remove SSLv2. (rbarlow@redhat.com)
- Set the version requirement on mock to be less than 1.1. (rbarlow@redhat.com)
- Merge branch 'path_not_name' (rbarlow@redhat.com)
- Error response for V2 registry (randalap@redhat.com)
- Merge branch '1271' (rbarlow@redhat.com)
- Merge branch 'logger_not_logging' (rbarlow@redhat.com)
- Fix a logging API error. (rbarlow@redhat.com)
- Correct the parameters to a function. (rbarlow@redhat.com)
- Use the data file's version to determine where to put repo data.
  (rbarlow@redhat.com)
- CP-254: Support in Crane for v2 registry support (randalap@redhat.com)

* Fri Nov 21 2014 Chris Duryee <cduryee@redhat.com> 0.2.2-1
- Bump release to 1 (cduryee@redhat.com)

* Wed Oct 22 2014 Chris Duryee <cduryee@redhat.com> 0.2.2-0.3.beta
- the /v1/repositories/<repo_id>/images call now handles the default "library"
  namespace (mhrivnak@redhat.com)
- review improvements (mhrivnak@redhat.com)
- Adding a basic "what is crane?" section to the README (mhrivnak@redhat.com)

* Mon Sep 15 2014 Randy Barlow <rbarlow@redhat.com> 0.2.2-0.2.beta
- Do not run unit tests during RPM build (cduryee@redhat.com)

* Mon Sep 15 2014 Randy Barlow <rbarlow@redhat.com> 0.2.2-0.1.beta
- updating pulp/cranebuilder for centos7 (mhrivnak@redhat.com)
- updating the Dockerfile to use centos7 and add the python-rhsm dependency
  (mhrivnak@redhat.com)

* Mon Jul 28 2014 Michael Hrivnak <mhrivnak@redhat.com> 0.2.1-1.beta
- Add python-rhsm to spec (bcourt@redhat.com)
- Move indirect-requirements needed for the travis environment to a separate
  requirements.txt file (bcourt@redhat.com)

* Fri Jul 25 2014 Michael Hrivnak <mhrivnak@redhat.com> 0.2.0-1.beta
- Monitor the data directory for changes (bcourt@redhat.com)
- ensuring that setuptools excludes tests from a distribution package
  (mhrivnak@redhat.com)
- simplifying the config loading so that it uses a default config file
  (mhrivnak@redhat.com)
- Implementing the search API to use a Google Search Appliance backend.
  (mhrivnak@redhat.com)
- adding Dockerfile for cranebuilder (mhrivnak@redhat.com)
- Add Entitlement support for Crane (bcourt@redhat.com)
- Added Dockerfile for crane (mhrivnak@redhat.com)

* Fri May 02 2014 Michael Hrivnak <mhrivnak@redhat.com> 0.1.0-0.4.beta
- Incrementing the release number. (mhrivnak@redhat.com)
- adding selinux fcontext changes to spec file (mhrivnak@redhat.com)
- Adding comments about how to deploy crane. (mhrivnak@redhat.com)

* Thu May 01 2014 Michael Hrivnak <mhrivnak@redhat.com> 0.1.0-0.3.alpha
- adding metadata dir to rpm spec file (mhrivnak@redhat.com)

* Wed Apr 30 2014 Michael Hrivnak <mhrivnak@redhat.com> 0.1.0-0.2.alpha
- adding wsgi file specifically for el6 to handle python-jinja2-26 weirdness
  (mhrivnak@redhat.com)

* Wed Apr 30 2014 Michael Hrivnak <mhrivnak@redhat.com> 0.1.0-0.1.alpha
- new package built with tito

