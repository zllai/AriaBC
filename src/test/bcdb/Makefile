#
# Makefile for bcdb programs
#

subdir = src/test/bcdb
top_builddir = ../../..
include $(top_builddir)/src/Makefile.global

ifeq ($(PORTNAME), win32)
LDFLAGS += -lws2_32
endif

override CPPFLAGS :=  -I $(top_builddir)/src/common/liblfds/inc $(CPPFLAGS)
LDFLAGS_INTERNAL += $(top_builddir)/src/backend/bcdb/utils/concurrent_queue.o

PROGS = flex_buffer

all: $(PROGS)

clean distclean maintainer-clean:
	rm -f $(PROGS) *.o
