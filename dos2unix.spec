Summary: Text file format converter
Name: dos2unix
Version: 3.1
Release: 37%{?dist}
Group: Applications/Text
License: BSD

# There is no upstream for this.
Source: %{name}-%{version}.tar.bz2

Patch0: %{name}-%{version}.patch
Patch1: dos2unix-3.1-segfault.patch
Patch2: dos2unix-3.1-safeconv.patch
Patch3: dos2unix-3.1-manpage-update-57507.patch
Patch4: dos2unix-3.1-preserve-file-modes.patch
Patch5: dos2unix-3.1-tmppath.patch
Patch6: dos2unix-c-missing-arg.patch
Patch7: dos2unix-missing-proto.patch
Patch8: dos2unix-manpage.patch
Patch9: dos2unix-preserve-file-modes.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Dos2unix converts DOS or MAC text files to UNIX format.

%prep
%setup -q
# Fix makefile and use mkstemp.
%patch0 -p1 -b .orig

# Check for errors when creating temporary file.
%patch1 -p1 -b .segfault

# Safer conversion with mac2unix.
%patch2 -p1 -b .safeconv

# Manual page fixes.
%patch3 -p1 -b .manpage-update-57507

# Preserve file modes when creating new files.
%patch4 -p1 -b .preserve-file-modes

# Don't just delete original file.
%patch5 -p1 -b .tmppath

# Fail gracefully when incorrect command line used.
%patch6 -p1 -b .c-missing-arg

# Include io.h and unistd.h.
%patch7 -p1 -b .missing-proto

# Fixed typo in man page.
%patch8 -p1 -b .manpage

# Preserve file modes.
%patch9 -p1 -b .preserve-file-modes

for I in *.[ch]; do
	sed -e 's,#endif.*,#endif,g' -e 's,#else.*,#else,g' $I > $I.new
	mv -f $I.new $I
done
make clean

%build
make CFLAGS="$RPM_OPT_FLAGS -D_LARGEFILE_SOURCE $(getconf LFS_CFLAGS)" \
  %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install -p -m755 dos2unix $RPM_BUILD_ROOT%{_bindir}
ln -s dos2unix $RPM_BUILD_ROOT%{_bindir}/mac2unix
install -p -m644 dos2unix.1 $RPM_BUILD_ROOT%{_mandir}/man1
ln -s dos2unix.1 $RPM_BUILD_ROOT%{_mandir}/man1/mac2unix.1

%files
%defattr(-,root,root,0755)
%doc COPYRIGHT
%{_bindir}/dos2unix
%{_bindir}/mac2unix
%{_mandir}/*/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> 3.1-37
- Added comments for all patches.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 3.1-36.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 24 2008 Tim Waugh <twaugh@redhat.com> 3.1-34
- Moved 'make clean' to prep section and added comment about there
  being no upstream (bug #225706).

* Mon Sep  8 2008 Tim Waugh <twaugh@redhat.com> 3.1-33
- Preserve file modes (bug #437465).
- Fixed manpage grammar (bug #460731).

* Mon Apr 14 2008 Tim Waugh <twaugh@redhat.com> 3.1-32
- Adjust license tag (bug #225706).
- Fix missing prototype (bug #225706).
- Install copy as symbolic links (bug #225706).

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 3.1-31
- Rebuild for GCC 4.3.

* Fri Jan 18 2008 Tim Waugh <twaugh@redhat.com> 3.1-30
- Applied patch from bug #292100 to fix segfault with missing -c argument.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 3.1-29
- Rebuild.

* Tue Feb  6 2007 Tim Waugh <twaugh@redhat.com> 3.1-28
- Fixed build root (bug #225706).
- Build with SMP flags (bug #225706).
- Use dist in release tag (bug #225706).
- Fixed macros in changelog (bug #225706).
- Preserve timestamps when using install (bug #225706).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.1-27.1
- rebuild

* Mon Jul 10 2006 Tim Waugh <twaugh@redhat.com> 3.1-27
- Re-encoded spec file in UTF-8 (bug #197817).

* Mon Jun  5 2006 Tim Waugh <twaugh@redhat.com> 3.1-26
- Rebuilt.

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 3.1-25
- Build with large file support.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.1-24.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.1-24.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Apr 13 2005 Tim Waugh <twaugh@redhat.com> 3.1-24
- Fixed tmppath patch (bug #150277).

* Thu Mar  3 2005 Mike A. Harris <mharris@redhat.com> 3.1-23
- Bump and rebuild for FC4, using gcc 4.

* Tue Feb  8 2005 Mike A. Harris <mharris@redhat.com> 3.1-22
- Bump and rebuild for FC4

* Wed Oct 20 2004 Miloslav Trmac <mitr@redhat.com> - 3.1-21
- Don't just delete the original file when destination and current directory
  are on different filesystems (#65548, #123069, patch by James Antill)
- Fix return type of StripDelimiter in dos2unix-3.1-safeconv.patch (#136148)

* Wed Oct  6 2004 Mike A. Harris <mharris@redhat.com> 3.1-20
- Added dos2unix-3.1-manpage-update-57507.patch to fix manpage (#57507)
- Added dos2unix-3.1-preserve-file-modes.patch to properly preserve file
  permissions (#91331,55183,112710,132145)

* Sun Sep 26 2004 Rik van Riel <riel@redhat.com> 3.1-19
- safer conversion w/ mac2unix (fix from bz #57508)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 05 2003 Elliot Lee <sopwith@redhat.com> 3.1-15
- Remove build dependency on perl, since perl BuildRequires: dos2unix,
  and there's no good reason not to just use sed here.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Oct  7 2002 Mike A. Harris <mharris@redhat.com> 3.1-13
- All-arch rebuild
- Added BuildRequires: perl

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.1-10
- Build in new environment

* Thu Jan 17 2002 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix bug #57700 (segfault)
- Add the mac2unix symlink recommended in README
- Fix compiler warnings

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jan 10 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- shut up rpmlint

* Fri Nov 17 2000 Tim Powers <timp@redhat.com>
- use mkstemp instead of mktemp. Not much needed to change.

* Thu Nov 16 2000 Tim Powers <timp@redhat.com>
- cleaned up specfile a bit
- built for 7.1

* Tue Jul 07 1999 Peter Soos <sp@osb.hu> 
- Added Hungarian "Summary:" and "%%description" 
- Corrected the file and directory attributes to rebuild the package 
  under RedHat Linux 6.0
