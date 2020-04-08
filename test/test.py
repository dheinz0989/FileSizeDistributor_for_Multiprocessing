from multithread_for_file_processor import FilesDistributor
from multiprocessing import cpu_count, Process, Manager
import time
from asammdf import MDF


class MDF_Reader:
    def __init__(self, mdf_file):
        self.mdf = MDF(mdf_file)
        self.info = self.mdf.info()
        self.signal_list = list(self.mdf.channels_db.keys())
        self._freq_dict = {0: '1Hz', 1: '5Hz', 2: '10Hz'}
        self._reversed_freq_dict = {'1Hz': 0, '5Hz': 1, '10Hz': 2}

    def get_signal_group(self, signal):
        assert signal in self.signal_list
        self.groups = self.mdf.channels_db[signal]

    def get_signal_values(self, signal, frequency):
        assert frequency in list(self._reversed_freq_dict.keys())
        i = self._reversed_freq_dict[frequency]
        self.mdf_values = self.mdf.get(name=signal, group=self.groups[i][0], index=self.groups[i][1])


def read_file_in_diretory(file_list):
    for f in file_list:
        print(f'Reading file: {f}')
        mdf = MDF_Reader(f)

def parallelize_work(file_directory):
    files_distributor = FilesDistributor(file_directory,'mf4')
    distribution = files_distributor.distribute_list_of_tuples_evenly()
    proc = [Process(target=read_file_in_diretory,args=(file,)) for file in distribution]
    for p in proc:
        p.start()
    for p in proc:
        p.join()


if __name__ =="__main__":
    paths_to_file = r'C:\Daten\Projekte\2018\02_Daimler\Evobus\EvoBus_Delivery\Archive_data\00_ALL_RAW\EDB_till_20181025\201807'
    parallelize_work(paths_to_file)