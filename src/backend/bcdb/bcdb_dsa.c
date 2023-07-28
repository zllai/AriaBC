#include "bcdb/bcdb_dsa.h"
#include "bcdb/globals.h"
#include "storage/lwlock.h"
#include "storage/shmem.h"

dsa_area    *bcdb_dsa_area;
void        *bcdb_dsa_shm;

void
attach_bcdb_dsa(void)
{
    Assert(bcdb_dsa_shm != NULL);
    bcdb_dsa_area = dsa_attach_in_place(bcdb_dsa_shm, NULL);
}

Size
bcdb_dsa_shm_size(void)
{
    return BCDB_DSA_SHM_SIZE;
}

void
create_bcdb_dsa(void)
{
    bool found;
	bcdb_dsa_shm = ShmemInitStruct("BCDB_DSA_SHM", bcdb_dsa_shm_size(), &found);
    bcdb_dsa_area = dsa_create_in_place(bcdb_dsa_shm, BCDB_DSA_SHM_SIZE, LWTRANCHE_BCDB_DSA, NULL);
}
