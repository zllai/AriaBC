# AriaBC

This repository contains the source code of AriaBC, i.e., the Aria deterministic concurrency control implemented on PostgreSQL.

## Compile and install

```sh
./configure
make -j
make install
```

## Run a sample workload (single machine)

1. Prepare the blockchain database file

```sh
initdb -D /tmp/ycsb
```

2. Launch the database engine

```sh
postgres -D /tmp/ycsb
```

3. Create the database and initialize the state

```sh
createdb ycsb
psql -d ycsb < src/benchmark/samples/ycsb_setup
```

4. Run the workload

```sh
psql -d ycsb < src/benchmark/samples/ycsb_tx_blocks
```

See src/benchmark/samples/ycsb_tx_blocks for more details on how to submit a block of transactions.