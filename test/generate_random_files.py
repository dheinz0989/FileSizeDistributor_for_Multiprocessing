from string import ascii_lowercase, digits
from pathlib import Path
import random
import argparse
from multiprocessing import cpu_count


n_CPU = cpu_count()
alphanumeric = list(ascii_lowercase + digits)


def create_random_file(chars, idx=0):
    with open(f'data/data_source_{idx}.txt', 'w+') as file:
        random_string = ''
        for i in range(1,chars):
            random_string += random.choice(alphanumeric)
        file.write(random_string)

def create_n_files(n=10,min_chars=100,max_chars=1000):
    for i in range(n):
        size = random.randint(min_chars,max_chars)
        create_random_file(size,i)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs the script to process all files.')
    parser.add_argument(
        "--directory",
        "-d",
        required=False,
        default='data',
        type=str,
        help="A flag indicating the directory with all files"
    )
    parser.add_argument(
        "--number",
        "-n",
        default=10,
        type=int,
        help="Number of random files to generate"
    )
    parser.add_argument(
        "--min_chars",
        "-min",
        default=100,
        type=int,
        help="Determines how many characters a text file must have at least"
    )
    parser.add_argument(
        "--max_chars",
        "-max",
        default=1000,
        type=int,
        help="Determines how many characters a text file must have at maximum"
    )
    args = parser.parse_args()
    create_n_files(args.number,args.min_chars,args.max_chars)