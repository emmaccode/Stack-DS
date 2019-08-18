## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = stackds.ui


## The main script
bin_SCRIPTS = stackds.py

## Directory where .class files will be installed
stackdsdir = $(pythondir)/stackds


stackds_PYTHON = \
	stackds.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)
