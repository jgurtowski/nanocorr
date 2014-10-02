#!/usr/bin/env python

import sys
import os

def runfail(cmd):
    print "Running : %s" % cmd
    if not 0 == os.system(cmd):
        sys.exit("Failed : %s " % cmd)

if not len(sys.argv) == 3:
    sys.exit("blast.py query.fa reference.fa")

query_file, ref_file = sys.argv[1:3]
start_path = os.getcwd()

if not os.path.exists(query_file):
    sys.exit("Missing Query File")
if not os.path.isabs(query_file):
    query_file = os.path.join(start_path, query_file)
if not os.path.isabs(ref_file):
    ref_file = os.path.join(start_path, ref_file)


tmp_dir = os.environ["TMPDIR"]
task_id = int(os.environ["SGE_TASK_ID"])

start_file = "p%04d" % task_id

os.chdir(tmp_dir)

runfail("cp {} . ".format(os.path.join(start_path, start_file)))

runfail("makeblastdb -dbtype nucl -in {}".format(start_file))

blast6_out = start_file + ".blast6"
runfail("blastn -db {db} -query {query} -outfmt \"6 std qlen slen qseq sseq\" -dust no -task blastn -reward 5 -penalty -4 -gapopen 8 -gapextend 6 -evalue 1e-15 -num_threads 3 | sort -k 2,2 -k 9,9n > {outfile}".format(db=start_file, query=query_file, outfile=blast6_out))

runfail("cp {} {} ".format(blast6_out, start_path))

blast6_filter_out = start_file +".blast6.r"
runfail("blast6Filter r_experimental {} > {}".format(blast6_out, blast6_filter_out))

runfail("cp {} {} ".format(blast6_filter_out, start_path))

correct_fa = start_file + ".blast6.r.fa"
correct_log = start_file + ".blast6.r.log"

cor_params = {"raw_reads": start_file,
          "filter_out": blast6_filter_out,
          "cor_fa" : correct_fa,
          "cor_log" : correct_log}

runfail("correctOxford {raw_reads} {filter_out} > {cor_fa} 2> {cor_log}".format(**cor_params))
runfail("cp {} {} {}".format(correct_fa,correct_log,start_path))


refblast_out = start_file + ".blast6.r.refblast6"
ref_blast_params = {"reference": ref_file,
                "cor_query": correct_fa,
                "ref_blast_out": refblast_out}

runfail("blastn -db {reference} -query {cor_query} -outfmt \"6 std qlen slen\" -evalue 1e-10 -reward 5 -penalty -4 -gapopen 8 -gapextend 6 -dust no -task blastn -out {ref_blast_out}".format(**ref_blast_params))


refblast_filter_out = start_file + ".blast6.r.refblast6.q"
runfail("blast6Filter q {} > {}".format(refblast_out, refblast_filter_out))

runfail("cp {} {} ".format(refblast_filter_out, start_path)) 











