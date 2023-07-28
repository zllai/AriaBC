import argparse
import random
import numpy
from common import util

#todo: fix random seed
numpy.random.seed(0)
random.seed(0)

class Benchmark(object):
    def init_args(self, parser):
        raise NotImplementedError()

    def gen_list_tx(self, opt):
        raise NotImplementedError()

    def setup(self, opt):
        raise NotImplementedError()

    def teardown(self, opt):
        raise NotImplementedError()

    def get_post_test_sql(self, opt):
        return None

    def ibm_wrapper(self, opt, tx_list):
        s = "SELECT bcdb_init();\n"
        cur_snapshot = 0
        cur_commit = 1
        for i, tx in enumerate(tx_list):
            cur_commit = i // opt.num_tx_per_block + 1
            cur_tx_id = i % opt.num_tx_per_block
            if cur_snapshot < cur_commit - 1:
                # delay switching block by some chance
                if random.random() > opt.r_early_snapshot:
                    cur_snapshot += 1
                    tx_hash_list = ["%d_%d" % (cur_commit-1, j) for j in range(opt.num_tx_per_block)]
                    block = ", ".join(['"' + tx + '"' for tx in tx_hash_list])
                    s += "SELECT bcdb_block_submit('{\"bid\": %d, \"txs\": [%s]}');\n" % (cur_commit-1, block)
            s += "SELECT bcdb_tx_submit('{\"snapshot_block\": %d, \"sql\": \"%s\", \"hash\": \"%d_%d\"}'); \n" % (cur_snapshot, util.escape_postgres_sql_str(tx), cur_commit, cur_tx_id)

        # last block
        tx_hash_list = ["%d_%d" % (cur_commit, j) for j in range(opt.num_tx_per_block)]
        block = ", ".join(['"' + tx + '"' for tx in tx_hash_list])
        s += "SELECT bcdb_block_submit('{\"bid\": %d, \"txs\": [%s]}');\n" % (cur_commit, block)
        s += "SELECT bcdb_num_committed();\n"
        return s

    def rand_isolation(self, opt):
        r = random.randint(1, 100)
        if r <= opt.rr_portion * 100:
            return "RR"
        if r <= (opt.rr_portion + opt.si_portion) * 100:
            return "SI"
        if r <= (opt.rr_portion + opt.si_portion + opt.rc_portion) * 100:
            return "RC"
        return "SE"


    # Since Dcc and Aria share the same wrapper, but Aria
    def ours_wrapper(self, opt, tx_list, is_oeip):
        s = f"SELECT bcdb_init({is_oeip}, {opt.num_tx_per_block});\n"
        blocks = [tx_list[i:i+opt.num_tx_per_block] for i in range(0, len(tx_list), opt.num_tx_per_block)]
        delayed_blocks = ""
        num_delayed_blocks = 0
        for i, block in enumerate(blocks):
            packed_txs = []
            for j, tx in enumerate(block):
                tx_hash = "%d_%d" % (i+1, j)
                isolation = self.rand_isolation(opt)
                packed_txs.append("{\"hash\": \"%s\", \"iso\": \"%s\", \"sql\": \"%s\"}" % (tx_hash, isolation, util.escape_postgres_sql_str(tx)))
            block = ",\n\t".join(packed_txs)
            s += "SELECT bcdb_block_submit('{\"bid\": %d, \"txs\": [\n\t%s]}');\n" % (i+1, block)

        s += "SELECT bcdb_wait_to_finish(); \n"
        if opt.insert_status:
            s += "SELECT bcdb_check_block_status(%d);\n" % i

        s += "SELECT bcdb_num_committed(); \n"
        return s


    def process_raw_tx_for_test(self, opt, raw_txt):
        ret = ""
        ret += '\nsession "s1"\n'
        raw_txt = raw_txt.replace("\n\t", "--new-line--\t")
        splitted = raw_txt.split("\n")
        permut = ""
        for i, line in enumerate(splitted):
            line = line.strip().replace("--new-line--", "\n")
            if line != "":
                ret += 'step "s1a%d" { %s }\n' % (i, line)
                permut += ' "s1a%d"' % i


        post_test_sql = self.get_post_test_sql(opt)
        if not (post_test_sql is None or post_test_sql == ""):
            ret += 'step "s1a%d" { %s }' % (i + 1,
                                            self.get_post_test_sql(opt))
            permut += ' "s1a%d"' % (i + 1)

        ret += '\npermutation' + permut
        return ret

    def post_teardown(self):
        print("SELECT bcdb_reset();")

    def main(self):
        parser = argparse.ArgumentParser()
        self.init_args(parser)
        parser.add_argument("--seed", type=int, default=0)
        parser.add_argument("--wrapper", choices=["ibm", "ours_ote", "ours_oeip", "raw", "aria"], default="raw")
        parser.add_argument("--test", action="store_true")
        parser.add_argument("--skip_setup", action="store_true")
        parser.add_argument("--skip_teardown", action="store_true")
        parser.add_argument("--skip_tx", action="store_true")
        parser.add_argument("--insert_status", action="store_true")
        parser.add_argument("--num_blocks", type=int, default=5)
        parser.add_argument("--num_tx_per_block", type=int, default=10)
        parser.add_argument("--rr_portion", type=float, default=0)
        parser.add_argument("--si_portion", type=float, default=0)
        parser.add_argument("--rc_portion", type=float, default=0)
        parser.add_argument("--r_early_snapshot", type=float, default=0.3)
        parser.add_argument("--block_delay", type=int, default=0)
        opt = parser.parse_args()

        random.seed(opt.seed)
        numpy.random.seed(opt.seed)

        if not opt.skip_setup:
            if opt.test:
                print("setup\n{")
            self.setup(opt)

            if opt.test:
                print("}")

        if not opt.skip_teardown and opt.test:
            if opt.test:
                print("teardown\n{")
            self.teardown(opt)
            self.post_teardown()
            if opt.test:
                print("}")

        if not opt.skip_tx:
            tx_list = self.gen_list_tx(opt)

            raw_txt = ""

            if opt.wrapper == "ibm":
                raw_txt = self.ibm_wrapper(opt, tx_list)
            elif opt.wrapper == "ours_ote":
                raw_txt = self.ours_wrapper(opt, tx_list, False)
            elif opt.wrapper == "ours_oeip":
                raw_txt = self.ours_wrapper(opt, tx_list, True)
            elif opt.wrapper == "aria":
                raw_txt = self.ours_wrapper(opt, tx_list)
            elif opt.wrapper == "raw":
                raw_txt = "\n".join(tx_list)

            if opt.test:
                raw_txt = self.process_raw_tx_for_test(opt, raw_txt)

            print(raw_txt)

        if not opt.skip_teardown and not opt.test:
            self.teardown(opt)
            self.post_teardown()