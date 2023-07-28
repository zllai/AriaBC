//
// Created by Chris Liu on 2/6/2020.
//

#include "bcdb/func.h"
#include "bcdb/middleware.h"
#include "bcdb/worker.h"
#include "bcdb/shm_block.h"
#include "stdio.h"

#include <openssl/aes.h>
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/ssl.h>
#include <openssl/bio.h>
#include <openssl/err.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "utils/builtins.h"

static RSA *createPublicRSA(char *key);
static bool RSAVerifySignature(RSA *rsa, unsigned char *MsgHash, size_t MsgHashLen, const char *Msg, size_t MsgLen, bool *Authentic);
static void Base64Decode(const char *b64message, unsigned char **buffer, size_t *length);
static bool verifySignature(char *publicKey, char *plainText, char *signatureBase64);
static size_t calcDecodeLength(const char *b64input);

RSA *createPublicRSA(char *key)
{
  RSA *rsa = NULL;
  BIO *keybio;
  keybio = BIO_new_mem_buf(key, -1);
  if (keybio == NULL)
  {
    return 0;
  }
  rsa = PEM_read_bio_RSA_PUBKEY(keybio, &rsa, NULL, NULL);
  return rsa;
}

bool RSAVerifySignature(RSA *rsa,
                        unsigned char *MsgHash,
                        size_t MsgHashLen,
                        const char *Msg,
                        size_t MsgLen,
                        bool *Authentic)
{
  EVP_PKEY *pubKey = EVP_PKEY_new();
  EVP_MD_CTX *m_RSAVerifyCtx = EVP_MD_CTX_create();
  int AuthStatus;
  EVP_PKEY_assign_RSA(pubKey, rsa);
  *Authentic = false;

  if (EVP_DigestVerifyInit(m_RSAVerifyCtx, NULL, EVP_sha256(), NULL, pubKey) <= 0)
  {
    return false;
  }
  if (EVP_DigestVerifyUpdate(m_RSAVerifyCtx, Msg, MsgLen) <= 0)
  {
    return false;
  }
  AuthStatus = EVP_DigestVerifyFinal(m_RSAVerifyCtx, MsgHash, MsgHashLen);
  if (AuthStatus == 1)
  {
    *Authentic = true;
    EVP_MD_CTX_destroy(m_RSAVerifyCtx);
    return true;
  }
  else if (AuthStatus == 0)
  {
    *Authentic = false;
    EVP_MD_CTX_destroy(m_RSAVerifyCtx);
    return true;
  }
  else
  {
    *Authentic = false;
    EVP_MD_CTX_destroy(m_RSAVerifyCtx);
    return false;
  }
}

size_t calcDecodeLength(const char *b64input)
{
  size_t len = strlen(b64input), padding = 0;

  if (b64input[len - 1] == '=' && b64input[len - 2] == '=') //last two chars are =
    padding = 2;
  else if (b64input[len - 1] == '=') //last char is =
    padding = 1;
  return (len * 3) / 4 - padding;
}

void Base64Decode(const char *b64message, unsigned char **buffer, size_t *length)
{
  BIO *bio, *b64;

  int decodeLen = calcDecodeLength(b64message);
  *buffer = (unsigned char *)malloc(decodeLen + 1);
  (*buffer)[decodeLen] = '\0';

  bio = BIO_new_mem_buf(b64message, -1);
  b64 = BIO_new(BIO_f_base64());
  BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
  bio = BIO_push(b64, bio);

  *length = BIO_read(bio, *buffer, strlen(b64message));
  BIO_free_all(bio);
}

bool verifySignature(char *publicKey, char *plainText, char *signatureBase64)
{
  RSA *publicRSA = createPublicRSA(publicKey);
  unsigned char *encMessage;
  size_t encMessageLength;
  bool authentic;
  Base64Decode(signatureBase64, &encMessage, &encMessageLength);
  bool result = RSAVerifySignature(publicRSA, encMessage, encMessageLength, plainText, strlen(plainText), &authentic);
  return result & authentic;
}

Datum
bcdb_verify(PG_FUNCTION_ARGS)
{
    
    char   *publicKey = text_to_cstring(PG_GETARG_TEXT_PP(0));
    char   *plainText = text_to_cstring(PG_GETARG_TEXT_PP(1));
    char   *signature = text_to_cstring(PG_GETARG_TEXT_PP(2));
    bool   ret = verifySignature(publicKey, plainText, signature);
    PG_RETURN_BOOL(ret);
}

/*
Datum
bcdb_dummy_block_commit(PG_FUNCTION_ARGS)
{
    char	   *file_path = PG_GETARG_CSTRING(0);
    int32      block_id = PG_GETARG_INT32(1);

    bcdb_middleware_dummy_block(file_path, block_id);

    PG_RETURN_BOOL(true);
}
*/

/*
Datum
bcdb_tx_file_submit(PG_FUNCTION_ARGS)
{
    char	   *file_path = PG_GETARG_CSTRING(0);

    bcdb_middleware_dummy_submit_tx(file_path);

    PG_RETURN_BOOL(true);
}
*/

Datum
bcdb_tx_submit(PG_FUNCTION_ARGS)
{
    char	   *bcdb_query = PG_GETARG_CSTRING(0);
    int32    snapshot;

    snapshot = bcdb_middleware_submit_tx(bcdb_query);

    PG_RETURN_INT32(snapshot);
}

Datum
bcdb_block_submit(PG_FUNCTION_ARGS)
{
    char	   *bcdb_query = PG_GETARG_CSTRING(0);

    bcdb_middleware_submit_block(bcdb_query);

    PG_RETURN_BOOL(true);
}

Datum
bcdb_add_tx_with_block_id(PG_FUNCTION_ARGS)
{
    char	   *tx_hash = PG_GETARG_CSTRING(0);
    int32      block_id = PG_GETARG_INT32(1);

    bcdb_middleware_set_txs_committed_block(tx_hash, block_id);

    PG_RETURN_BOOL(true);

}

Datum
bcdb_allow_txs_commit_by_block_id(PG_FUNCTION_ARGS)
{

    int32      block_id = PG_GETARG_INT32(0);

    bcdb_middleware_allow_txs_exec_write_set_and_commit_by_id(block_id);

    PG_RETURN_BOOL(true);

}

Datum
bcdb_check_txs_result(PG_FUNCTION_ARGS)
{

    char	   *tx_hash = PG_GETARG_CSTRING(0);

    bcdb_wait_tx_finish(tx_hash);

    PG_RETURN_BOOL(bcdb_is_tx_commited(tx_hash));

}

Datum
bcdb_wait_to_finish(PG_FUNCTION_ARGS)
{
    bcdb_middleware_wait_all_to_finish();
    PG_RETURN_BOOL(true);
}

Datum
bcdb_check_block_status(PG_FUNCTION_ARGS)
{

    //char            *ret;

#ifdef LOG_STATUS
    sleep(1); 
    for (int i=block_meta->global_bmin; i < block_meta->global_bmin + CLEANING_DELAY_BLOCKS; i++)
        block_cleaning(i);
    PG_RETURN_CSTRING(block_meta->log);
#endif
#ifndef LOG_STATUS
    PG_RETURN_CSTRING("\0");
#endif
}

Datum
bcdb_num_committed(PG_FUNCTION_ARGS)
{
    ereport(LOG, (errmsg("[ZL] num committed: %d", (int)block_meta->num_committed)));
    PG_RETURN_INT32((int)block_meta->num_committed);
}

Datum
bcdb_reset(PG_FUNCTION_ARGS)
{
    bcdb_clear_block_txs_store();
    PG_RETURN_BOOL(true);
}

Datum
bcdb_init(PG_FUNCTION_ARGS)
{
    bool is_oep_mode = PG_GETARG_BOOL(0);
    int32 block_size = PG_GETARG_INT32(1);
    bcdb_middleware_init(is_oep_mode, block_size);
    PG_RETURN_BOOL(true);
}
