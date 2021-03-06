%define _bashcompdir %_sysconfdir/bash_completion.d


Name:		the_silver_searcher
Version:	0.24.1
Release:	1%{?dist}
Summary:	A code-searching tool similar to ack, but faster

Group:		Applications/Utilities
License:	Apache v2.0
URL:		https://github.com/ggreer/%{name}
Source0:	https://github.com/downloads/ggreer/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	pcre-devel, xz-devel, zlib-devel
Requires:	pcre, xz, zlib

%description
The Silver Searcher
An attempt to make something better than ack (which itself is better than grep).

Why use Ag?
* It searches code about 3–5× faster than ack.
* It ignores file patterns from your .gitignore and .hgignore.
* If there are files in your source repo you don't want to search, just add their patterns to a .agignore file. *cough* extern *cough*
* The command name is 33% shorter than ack!

How is it so fast?
* Searching for literals (no regex) uses Boyer-Moore-Horspool strstr.
* Files are mmap()ed instead of read into a buffer.
* If you're building with PCRE 8.21 or greater, regex searches use the JIT compiler.
* Ag calls pcre_study() before executing the regex on a jillion files.
* Instead of calling fnmatch() on every pattern in your ignore files, non-regex patterns are loaded into an array and binary searched.
* Ag uses Pthreads to take advantage of multiple CPU cores and search files in parallel.

%prep
%setup -q


%build
aclocal
autoconf
autoheader
automake --add-missing
%configure 
make %{?_smp_mflags}


%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bashcompdir}
install -m 644 ag.bashcomp.sh ${RPM_BUILD_ROOT}%{_bashcompdir}

%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/*
%config %{_bashcompdir}/ag.bashcomp.sh
%config %{_datadir}/%{name}/completions/ag.bashcomp.sh


%changelog
* Thu Dec 5 2013 Emily Strickland <code@emily.st> - 0.18.1-1
- More accurate build and install requirements

* Fri Aug 16 2013 Andrew Seidl <git@aas.io> - 0.15.0-1
- Install bash completion file

* Wed Dec 05 2012 Daniel Nelson <packetcollision@gmail.com> - 0.13.1-1
- Initial Build
