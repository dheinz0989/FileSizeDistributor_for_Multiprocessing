import sys
from multiprocessing import cpu_count, Process
from pathlib import Path
import time
import argparse
import re
from math import log
sys.path.append("../src")
sys.path.append("./src")
from multithread_for_file_processor import FilesDistributor


#insert = Path(__file__).resolve().parent.parent.joinpath('src')
#print(insert)
n_CPU = cpu_count()

# TODO : Run time decorator is still not running
# solution: https://stackoverflow.com/questions/9336646/python-decorator-with-multiprocessing-fails
def run_time(func):
    """
    When decorating a function with this decorator, it indicates the function's run time in a hh:mm:ss after
    the function returns

    :param func: function to decorate
    :return: decorated function which indicates function run time
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        m, s = divmod(end - start, 60)
        h, m = divmod(m, 60)
        ms = int(s % 1 * 1000)
        s, m, h = int(round(s, 0)), int(round(m, 0)), int(round(h, 0))
        log.info(
            f'Execution Time (hh:mm:sec) for function "{func.__name__}": {h:02d}:{m:02d}:{s:02d},{ms:03d}'
        )
        return ret
    return wrapper

def workaround_run_time(start,end):
    m, s = divmod(end - start, 60)
    h, m = divmod(m, 60)
    ms = int(s % 1 * 1000)
    s, m, h = int(round(s, 0)), int(round(m, 0)), int(round(h, 0))
    print(f'Execution Time (hh:mm:sec): {h:02d}:{m:02d}:{s:02d},{ms:03d}')

def process_file(file):
    """
    An example file that processes all integer values in a text file. If it is greater than 0, the value's log is added. If not, the whole result is divided by 0.

    :param file: an example testfile
    :return:
    """
    with open(file, 'r') as f:
        print(f'Reading file {file} and process it')
        content = f.read()
        integers = [int(x) for x in re.findall(r'\d+', content)]
        total = 0
        for i in integers:
            if i > 0:
                total += log(i)
            else:
                total /= 10
        print(f'Result for {file}: {total}')


def process_all_files_in_dir(files_directory):
    """
    The main loop whose work can be split upon parallel threads

    :param files_directory:
    :return:
    """
    start = time.time()
    for file in files_directory:
        process_file(file)
    end = time.time()
    print('Finished processing.')
    workaround_run_time(start,end)


def parallel_processing(file_directory,n):
    start = time.time()
    files_distributor = FilesDistributor(file_directory, 'txt')
    distribution = files_distributor.distribute_list_of_tuples_evenly(n)
    proc = [Process(target=process_all_files_in_dir, args=(file,)) for file in distribution]
    for p in proc:
        p.start()
    for p in proc:
        p.join()
    end = time.time()
    print('Finished the distributed processing')
    workaround_run_time(start,end)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs the script to process all files.')
    parser.add_argument(
        "--file_format",
        "-f",
        required=False,
        default ='*',
        type=str,
        help="A string to identify which file are to be processed. Use '*' for all files"
    )
    parser.add_argument(
        "--directory",
        "-d",
        required=False,
        default='',
        type=str,
        help="A flag indicating the directory with all files"
    )
    parser.add_argument(
        "--parallel_process",
        "-p",
        default="y",
        type=str,
        choices=["n","y"],
        help="A flag use to determine if the parallel version of the script is run"
    )
    parser.add_argument(
        "--buckets",
        "-b",
        default=n_CPU,
        type=int,
        help="Determines in how many buckets the files are going to distributed"
    )
    parser.add_argument(
        "--single_process",
        "-s",
        default="n",
        type=str,
        choices=["n","y"],
        help="A flag use to determine if the parallel version of the script is run"
    )
    args = parser.parse_args()

    if args.single_process == "y":
        print('Processes all files in a single for loop')
        p = Path(args.directory).glob('**/*')
        files_directory = [x for x in p if x.is_file()]
        process_all_files_in_dir(files_directory)

    if args.parallel_process == 'y':
        print('Runs all file in a parallel version')
        parallel_processing(args.directory,args.buckets)


