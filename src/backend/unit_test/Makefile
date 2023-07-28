#
# Makefile for bcdb programs
#

subdir = src/backend/unit_test
top_builddir = ../../..
include $(top_builddir)/src/Makefile.global
include $(top_builddir)/src/backend/common.mk

SUBDIRS = ../access ../bcdb ../bootstrap ../catalog ../parser ../commands ../executor ../foreign ../lib ../libpq \
	../nodes ../optimizer ../partitioning ../port ../postmaster \
	../regex ../replication ../rewrite \
	../statistics ../storage ../tcop ../tsearch ../utils $(top_builddir)/src/timezone \
	../jit ../main

OBJS_ALL = $(call expand_subsys, $(SUBDIROBJS))

override CPPFLAGS :=  -I $(top_builddir)/src/common/liblfds/inc $(CPPFLAGS)
LDFLAGS_INTERNAL += -g -z muldefs $(OBJS_ALL) -L$(top_builddir)/src/interfaces/libpq -L$(top_builddir)/src/common -lpgport -lpgcommon -lpq 

PROGS = concurrent_queue

all: $(PROGS)

clean distclean maintainer-clean:
	rm -f $(PROGS) *.o
