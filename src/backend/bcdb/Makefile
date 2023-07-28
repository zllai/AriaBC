#-------------------------------------------------------------------------
#
# Makefile for the bcdb module
#
# src/backend/bcdb/Makefile
#
#-------------------------------------------------------------------------

subdir = src/backend/bcdb
top_builddir = ../../..
include $(top_builddir)/src/Makefile.global

override CPPFLAGS := -I$(srcdir) -I$(libpq_srcdir) $(CPPFLAGS)
SUBDIRS = utils

OBJS = \
	globals.o \
	shm_block.o \
	shm_transaction.o \
	worker_controller.o \
	worker.o \
	middleware.o \
	func.o \
	bcdb_dsa.o

include $(top_srcdir)/src/backend/common.mk

all: submake-libpq