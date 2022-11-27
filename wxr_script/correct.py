import os
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("file_size", type=int) # unit = GB
parser.add_argument("primer", type=int)
parser.add_argument("buf_size", type=int, default=240) # unit = MB
args = parser.parse_args()

if __name__ == '__main__':
    p = args.primer

    total_file_size = args.file_size * 1024*1024*1024
    args.buf_size *= 1024 * 1024

    split_num, last_file_size = divmod(total_file_size, args.buf_size * p)
    print(f"file per disk: {split_num+1}")

    splited_file_size = args.buf_size * p
    symbol_size, remain_size = divmod(splited_file_size, (p-1)*p)
    col_size = symbol_size * (p-1)
    print(f"col_size = {col_size}, remain_size = {remain_size}")

    last_symbol_size, last_remain_size = divmod(last_file_size, (p-1)*p)
    last_col_size = last_symbol_size * (p-1)
    print(f"last col size = {last_col_size}, last_remain_size = {last_remain_size}")
    

    # 检查 file_id = 0 的第 i 个 col_file 的正确性
    # 测试 normal read 的情况
    for i in range(p):
        print(f" === {i} ===")
        cmd = f"""dd if=./data/data_{args.file_size}GB of=../build/test_data/src bs={col_size} skip={i} count=1 iflag=fullblock
        dd if=../build/test_data/data_read_0 of=../build/test_data/target bs={col_size} skip={i} count=1 iflag=fullblock
        diff ../build/test_data/src ../build/test_data/target
        """

        os.system(cmd)
        time.sleep(5)