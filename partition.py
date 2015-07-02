#!/usr/bin/env python

import sys
import os
from itertools import starmap, chain, imap
from operator import itemgetter

from jbio.io.file import iterator_over_file_from_extension as ioffe
from jbio.fasta import record_to_string as fasta_record_to_string
from jbio.functional import compose

if not len(sys.argv) >=4:
    sys.exit("partition.py <reads_per_file (int)> <files_per_dir (int)> file1.fa [file2.fa ...]")

def pstr(num):
    return "%04d" % num

(rpf,fpd) = map(int,sys.argv[1:3])

in_files = sys.argv[3:]

openers = map(ioffe,in_files)

input_data = chain.from_iterable(openers)
total_reads = 0
dnum = 0
fnum = 0
fh = None
readidx_fh = open("ReadIndex.txt", "w")

for record in input_data:
    if total_reads % rpf == 0:
        if total_reads % (rpf * fpd) == 0:
            dnum += 1
            fnum = 0
            os.mkdir(pstr(dnum))
        fnum += 1
        if fh:
            fh.close()
        current_file ="%s/p%s" % (pstr(dnum),pstr(fnum))
        fh = open(current_file, "w") 

    clean_name = str(record.name).split()[0]
    clean_record = record._replace(name=clean_name)
    readidx_fh.write(clean_name +"\t" + current_file + "\n")
    
    fh.write(fasta_record_to_string(clean_record))
    fh.write("\n")

    total_reads += 1

readidx_fh.close()
fh.close()

