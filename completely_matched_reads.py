#!~/bin/python
import os
import argparse
import re

parser=argparse.ArgumentParser(description='count the number of completely matched reads')

parser.add_argument('-i1', type =argparse.FileType('r'),help='reads datasets, a fastq file')
parser.add_argument('-i2', type =argparse.FileType('r'),help='specific sequences, as seed sequence, a fasta file')
parser.add_argument('-o', type =argparse.FileType('w'),help='completely matched reads, a result file')
args=parser.parse_args()
debug=True

#eg: python completely_matched_reads.py -i1 test.fq -i2 sequence.txt -o gene_number.txt

dic = {}
dic['A'] = 'T'
dic['T'] = 'A'
dic['C'] = 'G'
dic['G'] = 'C'


listi = []
listr = []
args.o.write('count1hitreads' + '\t')
for line1 in args.i2:
	if line1[0] == '>':
		args.o.write(line1[1:].strip() + '\t')
	else:
		i = line1.strip()
		newline = i[::-1] 
		listi.append(i)
		r = ''
		for cell in newline:
			r = r + dic[cell]
		#print(r)
		listr.append(r)
loci = len(listi)
#print(listi)

m = []
for j in range(loci):
	m.append(0)
	
n = []
for c in range(loci):
	n.append(0)

for line in args.i1:
	if line[0] == '@' or line[0] == '+' or line[0] == '#':
		continue
	else:
		w = -1
		y = -1
		for k in listi:
			w += 1
			if k in line:
				m[w] = m[w] + 1
		for a in listr:
			y += 1
			if a in line:
				n[y] = n[y] + 1
if len(m) == len(n):
	d = []
	for f in range(len(m)):
		f1 = m[f]+n[f]
		d.append(f1)

newline1 = ''
newline2 = ''
newline3 = ''
for z in m:
	newline1 = newline1 + str(z) + '\t'
for b in n:
	newline2 = newline2 + str(b) + '\t'
for e in d:
	newline3 = newline3 + str(e) + '\t'
args.o.write('\n' + 'positive_strain' + '\t' + newline1 + '\n')
args.o.write('negative_strain' + '\t' + newline2 + '\n')
args.o.write('total1hitnumer' + '\t' + newline3 + '\n')

args.i1.close()
args.i2.close()
args.o.close()
