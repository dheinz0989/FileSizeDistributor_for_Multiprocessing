# FileSizeDistributor
This module contains a class which can be use to split all files in a given directory in separate bucket (as a Python list) such that the sum of all the bucket's file size
are highly equally distributed. The initial idea of this class was to enhance processing speed for a script, in which a huge number of files was processed in a long "for" loop containing many checks,
branches, exception, etc.. Instead of iterating over all files in the directory in one loop, the intention was to select different subsets of files and send them to a CPU for processing. The files are thus processed in parallel. At the end, all files are processed,
Therefore, for each CPU, a subset of files is selected such that each CPU receives a list of files whose sum of sizes near to those of other CPUs and therefore obtain a high CPU
workload for a long time.

It is like a MapReduce approach for a single machine with each CPU as a worker.

Please note that this module only works for a processing task without interdependency but only for tasks that can be executed in parallel.

Its recommended use case is for processing a large list of files where each process can run in parallel and the execution steps are identical for all files

# Prerequisits
The source code is written in [Python 3.8](https://www.python.org/). It use some of the standard libraries which are included in the most Python environments.
Those standard libraries are:
    - pathlib
    - os 
    - operator

# Installation
You can clone this repository by running:
	
	git clone https://github.com/dheinz0989/FileSizeDistributor_for_Multiprocessing

# Usage
Windows user are highly recommend to use a (__name__=="__main__")[https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/] statement in order to guarantee all processes are cirretly set up. 

An example usage is found in the [test](https://github.com/dheinz0989/FileSizeDistributor_for_Multiprocessing/tree/master/test) directory in this repo.
In this example, a variety of random .txt files are generated. They contain a sequence of alphanumeric values. 
The files processor script reads each one of these files and processes them. In this example, it retrieves all integer values inside and calculates a final value:
    - for each value > 0, the log is added to the sum
    - for each value = 0, the current value is divided by 10
Please note, that this formula is totally random. It just has two attributes for which this use case scipt might be interest:
    - tasks are highly able to run in parallel
    - A lot of files are read to process

Before generating the random text files, assume that you have an /data direcotry in the test directory (This will be implemented automatically in future versions)
To setup 100 random text files with  at least 1.000.000 and 5.000.000 character each (Caution, the generating of this text files can take quite a long time):

```
python test/generate_random_files.py -n 100 -min 1000000 -max 5000000
```

For run the testing, you can then run the two different version. For the single loop version call 

```
python test/test.py -d ./test/data -p n -l y
```

For the parallel testing version, call:

```
python test/test.py -d ./test/data -p y
```
This yields a run time of appr 1:40

# To Do
This repository has several things which are not implemented yet. Amongs others, the following implementation are planned:
1. Implement the functionality as a Decorator
2. Implement directory write in the test script
3. add recursive file finding 
4. Add additional parser and attributes. 