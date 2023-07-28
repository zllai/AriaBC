#ifndef BCDB_DSA_H
#define BCDB_DSA_H

#include "postgres.h"
#include "utils/dsa.h"

#define BCDB_DSA_SHM_SIZE 1024 * 1024

extern dsa_area     *bcdb_dsa_area;

/* to create dsa in postmaster, have to let it based on a postmaster SHM */
Size bcdb_dsa_shm_size(void);
void create_bcdb_dsa(void);
void attach_bcdb_dsa(void);

#endif