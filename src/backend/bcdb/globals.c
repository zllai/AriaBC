/*-------------------------------------------------------------------------
 *
 * bcdb_global.c
 *    global variables for blockchainDB
 *
 *
 * IDENTIFICATION
 *	  src/backend/bcdb/bcdb.c
 *
 *-------------------------------------------------------------------------
 */
#include "bcdb/globals.h"
#include <time.h>
#include <openssl/bio.h>
#include <openssl/evp.h>
#include <openssl/buffer.h>
#include <stdint.h>

bool    is_bcdb_master = false;
bool    is_bcdb_worker = false;
bool    skip_conflict_checking = false;
int     gdb_pause_sig = 0;
char*   bcdb_host;
char*   bcdb_port;
bool    OEP_mode = false;
pid_t   pid;
BcdbIsolationLevel BcdbCurrentIsolationLevel = BCDB_SERIALIZABLE;
int32         worker_id;

uint64
bcdb_get_time()
{
    struct timespec time_spec;
    uint64 ret;
    clock_gettime(CLOCK_REALTIME, &time_spec);
    ret = (uint64)(time_spec.tv_sec) * (uint64)1e6; 
    ret += (uint64)time_spec.tv_nsec / (uint64)1e3;
    return ret;
}

int Base64Encode(const unsigned char* buffer, size_t length, char** b64text) 
{ 
	BIO *bio, *b64;
	BUF_MEM *bufferPtr;

	b64 = BIO_new(BIO_f_base64());
	bio = BIO_new(BIO_s_mem());
	bio = BIO_push(b64, bio);

	BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL);
	BIO_write(bio, buffer, length);
	BIO_flush(bio);
	BIO_get_mem_ptr(bio, &bufferPtr);
    *b64text = (char*) palloc((bufferPtr->length + 1) * sizeof(char));
    memcpy(*b64text, bufferPtr->data, bufferPtr->length);
    (*b64text)[bufferPtr->length] = '\0';
	BIO_set_close(bio, BIO_CLOSE);
	BIO_free_all(bio);

	return (0); //success
}
