#-------------------------------------------------------------------------
#
# Makefile for the bcdb module
#
# src/backend/bcdb/Makefile
#
#-------------------------------------------------------------------------

subdir = src/backend/bcdb/utils
top_builddir = ../../../..
include $(top_builddir)/src/Makefile.global

override CPPFLAGS := -I $(top_builddir)/src/common/liblfds/inc -I$(libpq_srcdir) $(CPPFLAGS)

OBJS = \
	sysinfo.o \
	cJSON.o \
	aligned_heap.o \
	func.o


include $(top_srcdir)/src/backend/common.mk
