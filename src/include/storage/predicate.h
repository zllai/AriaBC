/*-------------------------------------------------------------------------
 *
 * predicate.h
 *	  POSTGRES public predicate locking definitions.
 *
 *
 * Portions Copyright (c) 1996-2019, PostgreSQL Global Development Group
 * Portions Copyright (c) 1994, Regents of the University of California
 *
 * src/include/storage/predicate.h
 *
 *-------------------------------------------------------------------------
 */
#ifndef PREDICATE_H
#define PREDICATE_H

#include "storage/lock.h"
#include "utils/relcache.h"
#include "utils/snapshot.h"
#include "storage/predicate_internals.h"
#include "bcdb/shm_transaction.h"


/*
 * GUC variables
 */
extern int	max_predicate_locks_per_xact;
extern int	max_predicate_locks_per_relation;
extern int	max_predicate_locks_per_page;


/* Number of SLRU buffers to use for predicate locking */
#define NUM_OLDSERXID_BUFFERS	16

#define SxactIsDoomed(sxact) (((sxact)->flags & SXACT_FLAG_DOOMED) != 0)
#define SxactIsRolledBack(sxact) (((sxact)->flags & SXACT_FLAG_ROLLED_BACK) != 0)

/*
 * A handle used for sharing SERIALIZABLEXACT objects between the participants
 * in a parallel query.
 */
typedef void *SerializableXactHandle;

/*
 * function prototypes
 */

/* housekeeping for shared memory predicate lock structures */
extern void InitPredicateLocks(void);
extern Size PredicateLockShmemSize(void);

extern void CheckPointPredicate(void);

/* predicate lock reporting */
extern bool PageIsPredicateLocked(Relation relation, BlockNumber blkno);

/* predicate lock maintenance */
extern Snapshot GetSerializableTransactionSnapshot(Snapshot snapshot);
extern void SetSerializableTransactionSnapshot(Snapshot snapshot,
											   VirtualTransactionId *sourcevxid,
											   int sourcepid);
extern void RegisterPredicateLockingXid(TransactionId xid);
extern void PredicateLockRelation(Relation relation, Snapshot snapshot);
extern void PredicateLockPage(Relation relation, BlockNumber blkno, Snapshot snapshot);
extern void PredicateLockTuple(Relation relation, HeapTuple tuple, Snapshot snapshot);
extern void PredicateLockPageSplit(Relation relation, BlockNumber oldblkno, BlockNumber newblkno);
extern void PredicateLockPageCombine(Relation relation, BlockNumber oldblkno, BlockNumber newblkno);
extern void TransferPredicateLocksToHeapRelation(Relation relation);
extern void ReleasePredicateLocks(bool isCommit, bool isReadOnlySafe);

/* conflict detection (may also trigger rollback) */
extern bool CheckForSerializableConflictOut(bool valid, Relation relation, HeapTuple tuple,
											Buffer buffer, Snapshot snapshot);
extern void CheckForSerializableConflictIn(Relation relation, HeapTuple tuple, Buffer buffer);
extern void CheckTableForSerializableConflictIn(Relation relation);

/* final rollback checking */
extern void PreCommit_CheckForSerializationFailure(void);

/* two-phase commit support */
extern void AtPrepare_PredicateLocks(void);
extern void PostPrepare_PredicateLocks(TransactionId xid);
extern void PredicateLockTwoPhaseFinish(TransactionId xid, bool isCommit);
extern void predicatelock_twophase_recover(TransactionId xid, uint16 info,
										   void *recdata, uint32 len);

/* parallel query support */
extern SerializableXactHandle ShareSerializableXact(void);
extern void AttachSerializableXact(SerializableXactHandle handle);

extern bool RWConflictExists(const SERIALIZABLEXACT *reader, const SERIALIZABLEXACT *writer);
extern void FlagRWConflict(SERIALIZABLEXACT *reader, SERIALIZABLEXACT *writer);
extern void ReleaseRWConflict(RWConflict conflict);
extern void BCDB_FlagRWConflict(SERIALIZABLEXACT *reader, SERIALIZABLEXACT *writer, bool marking_mutual);
extern void set_write_mutual_conflict_with(BCDBShmXact *b, bool enforce);

#endif							/* PREDICATE_H */
