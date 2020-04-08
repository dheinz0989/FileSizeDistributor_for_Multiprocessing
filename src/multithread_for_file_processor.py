'''
This module contains a class which can be use to split all files in a given directory in separate bucket such that the sum of all the bucket's file size
are highly equally distributed. The initial idea of this class was script, in which a huge number of files was processed in a long "for" loop containing many checks,
branches, exception, etc.. Instead of iterating over all files in the directory in one loop, the intention was to select different subset of files and send it to a CPU for processing.
Therefore, for each CPU, a subset of files is selected such that each CPU receives a list of files whose sum of sizes near to those of other CPUs and therefore obtain a high CPU
workload for a long time.
It is like a MapReduce approach for a single machine with each CPU as a worker.

Please note that this module only works for a processing task without interdependency but only for tasks that can be executed in parallel.

Its recommended use case is for processing a large list of files where each process can run in parallel and the execution steps are identical for all files
'''

from pathlib import Path
from os import stat
from operator import itemgetter



class FilesDistributor:
    def __init__(self,file_dir,file_format="*"):
        """
        Initilizes a FilesDistributor object.

        :param file_dir: The directory in which are all files to process
        :type: str
        :param file_format: a string indicating which format of files are to be processed. By default, '*' selects all files
        :type: str
        """
        self.file_dir = file_dir
        self._file_format = file_format

    @property
    def files(self) -> list:
        """
        Retrieves a list of all files found in the file_directory.

        :return: a list of all files in the directory
        :rtype: list
        """
        files = Path(self.file_dir).glob(f'*.{self._file_format}')
        return [x for x in files if x.is_file()]

    @property
    def file_sizes(self):
        """
        For each file in the directory, retrieves the file size. They are saved in a list of tuples where the first entry is the file name and the second the file size

        :return: list
        """
        return [(x, self.get_file_size(x, byte_prefix=False)) for x in self.files]

    @staticmethod
    def get_file_size(file: str, byte_prefix=True):
        """
        A function which indicates a file's size.

        :param str file: file whose size is to be identified
        :type file: str
        :param byte_prefix: a flag indicating if the file size shall be expressed in an integer number of with kb, mb, gb, etc. prefixes
        :type byte_prefix: bool
        :return: the file's size
        :rtype: str
        """

        def convert_bytes(num: float) -> str:
            """
            Helper function which takes a number of bytes and converts it into a human readable information size unit.

            :param float num: the number of byte
            :return: a human readable string indicating the size in bytes with prefixes
            :rtype: str
            """
            for x in ["bytes", "KB", "MB", "GB", "TB", "PB"]:
                if num < 1024.0:
                    return "%3.2f %s" % (num, x)
                num /= 1024.0

        file_info = stat(file)
        return convert_bytes(file_info.st_size) if byte_prefix else file_info.st_size

    def distribute_list_of_tuples_evenly(self,n):
        """
        Distributes the files found in the ``file_sizes`` across n different buckets while the difference of total size across the buckets
        is tried to be minimized. Returns a list of n list, where sum(size(n)) is tried to be equal across the the n-th entry

        :param n: number of buckets in which the files are to distributed
        :type n: int
        :return: a list of n entries with files inside them
        :rtype: list
        """
        buckets = [[] for i in range(n)]
        weights = [[0, i] for i in range(n)]
        for item in sorted(self.file_sizes, key=itemgetter(1), reverse=True):
            key, value = item[0], item[1]
            idx = weights[0][1]
            buckets[idx].append(key)
            weights[0][0] += value
            weights = sorted(weights)
        return buckets
