import argparse
import os
import random
import numpy

from common.framework import Benchmark

from functools import reduce
import random 
import bisect 
import math 
import logging

class ZipfGenerator: 
    def __init__(self, n, alpha): 
        tmp = [1. / (math.pow(float(i), alpha)) for i in range(1, n+1)] 
        zeta = reduce(lambda sums, x: sums + [sums[-1] + x], tmp, [0]) 
        self.distMap = [x / zeta[-1] for x in zeta] 

    def next(self, r): 
        return bisect.bisect(self.distMap, r) - 1
    


def get_string_by_idx(target_string, idxs):
    ret = ""
    for idx in idxs:
        ret += target_string[idx]
    return ret


def get_init_keys_values(num_key:int, num_field:int, opt, field_length=10):
    ret = numpy.empty((num_key, num_field+1), dtype=f'<U{field_length}')
    alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rng = numpy.random.default_rng(opt.seed+2)
    random_arrays = rng.integers(len(alpha), size=(num_key, num_field, field_length))
    for x in range(num_key):
        user_key = f"user{x}"
        ret[x,0] = user_key
        for y in range(num_field):
            field_value = get_string_by_idx(alpha, random_arrays[(x, y)])
            ret[x,y+1] = field_value
    return ret


def get_sql_inserts_init_items(table_name:str, field_names:list, key_name:str, items):
    field_names = [key_name] + field_names
    column_string = ",".join(field_names)
    values = []
    for key_fields in items:
        key_fields_with_quote = [f"'{x}'" for x in key_fields]
        values.append(f"({','.join(key_fields_with_quote)})")
    values = ",".join(values)
    ret = f"INSERT INTO {table_name} ({column_string}) VALUES {values};"
    return ret


def setup(opt):
    table_name = opt.table_name
    numfield = opt.num_field
    key_name = opt.key_name

    fields = [f"FIELD{x}" for x in range(numfield)]
    stmt_field_create = [f"{field} TEXT" for field in fields]
    stmt_field_create = ",".join(stmt_field_create)

    print(f"""
    CREATE TABLE {table_name} (
        {key_name} VARCHAR(255) PRIMARY KEY,
        {stmt_field_create}
    );
    CREATE INDEX hash_usertable ON usertable using hash ({key_name});
    """)

    # insert remote procedure
    with open(os.path.join(os.path.dirname(__file__), "ycsb.sql"), 'r') as f:
        print(f.read())

    # insert init record
    item = get_init_keys_values(opt.num_key, opt.num_field, opt)
    print(get_sql_inserts_init_items(table_name, fields, key_name, item))


def teardown(opt):
    usertable = opt.table_name
    print(f'''
      DROP TABLE {usertable};
    ''')


class YSCBBenchmark(Benchmark):
    def __init__(self):
        super(YSCBBenchmark).__init__()

    def init_args(self, parser):
        parser.add_argument("--read_proportion", type=float, default=0.8)
        parser.add_argument("--num_key", type=int, default=40000)
        parser.add_argument("--num_tx", type=int, default=40000)
        parser.add_argument("--operation_per_tx", type=int, default=10)
        parser.add_argument("--operation_per_tx_var", type=float, default=0)
        parser.add_argument("--table_name", type=str, default="usertable")
        parser.add_argument("--num_field", type=int, default=10)
        parser.add_argument("--key_name", type=str, default="YCSB_KEY")
        parser.add_argument("--skew", type=float, default=0)
        parser.add_argument("--hotspot_accounts", type=float, default=0)
        parser.add_argument("--hotspot_prob", type=float, default=0)
        parser.add_argument("--mode", type=str, default='A')

    def gen_tx_sql(self, read_user_ids, write_user_ids):
        sql = f"SELECT read_modify_write(ARRAY[{','.join(read_user_ids)}]::varchar[], ARRAY[{','.join(write_user_ids)}]::varchar[]);"
        return sql

    def gen_list_tx(self, opt):
        tx_list = []

        zipf_gen = ZipfGenerator(opt.num_key, opt.skew)
        random_operation_type = numpy.random.default_rng(seed=opt.seed+1)
        random_user_id = numpy.random.default_rng(seed=opt.seed)
        random_op_num = numpy.random.default_rng(seed=opt.seed+2)
        random_hotspot = numpy.random.default_rng(seed=opt.seed+3)
        random_hotspot_account = numpy.random.default_rng(seed=opt.seed+4)

        for i in range(opt.num_blocks * opt.num_tx_per_block):
            if opt.operation_per_tx_var == 0:
                operation_per_tx = opt.operation_per_tx
            else:
                operation_per_tx = max(1, round(random_op_num.normal(opt.operation_per_tx, opt.operation_per_tx_var)))

            opreation_type = random_operation_type.uniform(0, 1, operation_per_tx)

            read_user_ids = []
            write_user_ids = []
            for val in opreation_type:
                if val < opt.read_proportion:
                    while True:
                        user_id = f"\'user{zipf_gen.next(random_user_id.random(1)[0])}\'"
                        if user_id not in read_user_ids:
                            break
                    read_user_ids.append(user_id)
                else:
                    while True:
                        if opt.hotspot_accounts == 0 or random_hotspot.uniform(0, 1) >= opt.hotspot_prob:
                            user_id = f"\'user{zipf_gen.next(random_user_id.random(1)[0])}\'"
                        else:
                            user_id = f"\'user{random_hotspot_account.integers(low=0, high=(opt.num_key * opt.hotspot_accounts))}\'"
                        if user_id not in write_user_ids:
                            break
                    write_user_ids.append(user_id)
            if opt.mode == "B":
                if len(read_user_ids) < len(write_user_ids):
                    read_user_ids = (read_user_ids + write_user_ids)[:5]
                write_user_ids = random.sample(read_user_ids, opt.operation_per_tx - len(read_user_ids))
            tx_list.append(self.gen_tx_sql(read_user_ids, write_user_ids))

        return tx_list

    def setup(self, opt):
        setup(opt)

    def teardown(self, opt):
        teardown(opt)


if __name__ == "__main__":
    benchmark = YSCBBenchmark()
    benchmark.main()
