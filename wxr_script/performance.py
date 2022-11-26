import os
import argparse
import time
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("file_size", type=int)
parser.add_argument("primer", type=int)
args = parser.parse_args()

def print_run_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print(f"[{func.__name__}] duration time: {time.time()-local_time:.4f}s")
    return wrapper

@print_run_time
def generate_data(size:int) -> bool:
    path = f"data/data_{size}GB"
    if os.path.exists(path):
        print(f"file exist: {path}")
        return False
    assert(size > 0)
    for i in range(size):
        os.system(f"dd if=/dev/urandom of={path} bs=1G count=1 conv=notrunc iflag=fullblock oflag=append")
    return True

# buf_size: 单位为 MB
def do_write(buf_size: int, file_size: int, p: int):
    os.system('echo -n "| write "')
    local_time = time.time()
    os.system(f"./time_check write ../wxr_script/data/data_{file_size}GB {p} {buf_size}")
    return time.time() - local_time


def read_normal(file_size:int) -> float:
    os.system('echo -n "| read normal "')
    path = f"../wxr_script/data/data_{file_size}GB"
    dst_path = f"./test_data/data_{file_size}GB_read_0"
    local_time = time.time()
    os.system(f"./evenodd read {path} {dst_path}")
    return time.time() - local_time

# miss p-2
def read_miss_data_one(file_size:int, p:int) -> float:
    os.system('echo -n "| read miss one data "')
    path = f"../wxr_script/data/data_{file_size}GB"
    dst_path = f"./test_data/data_{file_size}GB_read_11"
    os.rename(f'disk_{p-2}', f'_disk_{p-2}')
    local_time = time.time()
    os.system(f"./evenodd read {path} {dst_path}")
    t = time.time() - local_time
    os.rename(f'_disk_{p-2}', f'disk_{p-2}')
    return t


def read_miss_rd(file_size:int, p:int) -> float:
    os.system('echo -n "| read miss row and diagonal "')
    path = f"../wxr_script/data/data_{file_size}GB"
    dst_path = f"./test_data/data_{file_size}GB_read_21"
    os.rename(f'disk_{p}', f'_disk_{p}')
    os.rename(f'disk_{p+1}', f'_disk_{p+1}')
    local_time = time.time()
    os.system(f"./evenodd read {path} {dst_path}")
    t = time.time() - local_time
    os.rename(f'_disk_{p}', f'disk_{p}')
    os.rename(f'_disk_{p+1}', f'disk_{p+1}')
    return t

def read_miss_data_r(file_size:int, p:int) -> float:
    os.system('echo -n "| read miss data and row "')
    path = f"../wxr_script/data/data_{file_size}GB"
    dst_path = f"./test_data/data_{file_size}GB_read_22"
    os.rename(f'disk_{p-2}', f'_disk_{p-2}')
    os.rename(f'disk_{p}', f'_disk_{p}')
    local_time = time.time()
    os.system(f"./evenodd read {path} {dst_path}")
    t = time.time() - local_time
    os.rename(f'_disk_{p-2}', f'disk_{p-2}')
    os.rename(f'_disk_{p}', f'disk_{p}')
    return t

def read_miss_data_d(file_size:int, p:int) -> float:
    os.system('echo -n "| read miss data and diagonal "')
    path = f"../wxr_script/data/data_{file_size}GB"
    dst_path = f"./test_data/data_{file_size}GB_read_23"
    os.rename(f'disk_{p-3}', f'_disk_{p-3}')
    os.rename(f'disk_{p+1}', f'_disk_{p+1}')
    local_time = time.time()
    os.system(f"./evenodd read {path} {dst_path}")
    t = time.time() - local_time
    os.rename(f'_disk_{p-3}', f'disk_{p-3}')
    os.rename(f'_disk_{p+1}', f'disk_{p+1}')
    return t  

def read_miss_data_two(file_size:int, p:int) -> float:
    os.system('echo -n "| read miss two data "')

    path = f"../wxr_script/data/data_{file_size}GB"
    dst_path = f"./test_data/data_{file_size}GB_read_24"
    os.rename(f'disk_{p-1}', f'_disk_{p-1}')
    os.rename(f'disk_{p-3}', f'_disk_{p-3}')
    local_time = time.time()
    os.system(f"./evenodd read {path} {dst_path}")
    t = time.time() - local_time
    os.rename(f'_disk_{p-1}', f'disk_{p-1}')
    os.rename(f'_disk_{p-3}', f'disk_{p-3}')
    return t  

if __name__ == '__main__':
    # 固定测试 file_size = 4GB, primer = 13
    # 测试不同 buffer_size 对于 read 性能的影响

    os.system("./start.sh")
    generate_data(args.file_size)
    file_size = args.file_size
    p = args.primer 
    os.chdir("../build")
    buf_size_list = [pow(2, i+1) for i in range(10)] # from 1MB to 1GB
    time_list = [0] * 7

    
    buf_size_list = [16] #[1, 16, 256]
    time_list = [[0]*7 for _ in range(len(buf_size_list))]
    for i, buf_size in enumerate(buf_size_list):
        t = time_list[i]

        print(f"|buf={buf_size}, fs={file_size}, p={p} | total_cost | xor | io | write | read |")
        print("| -- | -- | -- | -- | -- | -- |")

        t[0] = do_write(buf_size, file_size, 13)

        t[1] = read_normal(file_size)

        # t[2] = read_miss_data_one(file_size, p)

        # t[3] = read_miss_rd(file_size, p)

        # t[4] = read_miss_data_r(file_size, p)

        # t[5] = read_miss_data_d(file_size, p)

        # t[6] = read_miss_data_two(file_size, p)

        print()
        # os.system("rm -rf disk_*")
        # os.system("rm -r test_data/*")
    
    