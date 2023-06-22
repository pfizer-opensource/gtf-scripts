#!/usr/bin/env python3

"""
Select rRNA records from GTF, and output in "interval" format, as required by CollectRnaSeqMetrics.

format description:

  Represents a list of intervals against a reference sequence that can be
  written to and read from a file. The file format is relatively simple and
  reflects the SAM alignment format to a degree. A SAM style header must be
  present in the file which lists the sequence records against which the
  intervals are described. After the header the file then contains records one
  per line in text format with the following values tab-separated: Sequence
  name, Start position (1-based), End position (1-based, end inclusive), Strand
  (either + or -), Interval name (an, ideally unique, name for the interval),

see also: https://www.biostars.org/p/67079/


# @SQ     SN:15   LN:101991189

"""

__author__ = 'Dmitri Bichko, Rob Moccia'
__version__ = '0.1'

import gtf
import argparse
import sys
from pathlib import Path


def configure_args(parser):
    parser.add_argument('--input', required=True, help='GTF file')
    parser.add_argument('--output', required=True, help='output file')
    parser.add_argument('--genome', help='star index to read contig info from')
    parser.add_argument('--faidx', help='genomic fa index to read contig info from')
    parser.add_argument('--version', action='version',
        version='%(prog)s {version}'.format(version=__version__))


def process(args):

    assert args.genome is not None or args.faidx is not None, 'need one of: genome or faidx'


    num_records = 0
    num_written = 0

    with open(args.output, 'w') as writer:
        if args.genome is not None:
            with open(Path(args.genome, 'chrNameLength.txt')) as r:
                for line in r:
                    contig, length = line.strip().split('\t', 1)
                    writer.write(f'@SQ\tSN:{contig}\tLN:{length}\n')
        elif args.faidx is not None:
            with open(Path(args.faidx)) as r:
                for line in r:
                    contig, length, *_ = line.strip().split('\t')
                    writer.write(f'@SQ\tSN:{contig}\tLN:{length}\n')
        with open(args.input,'r') as reader:
            for rec in gtf.open(reader, 'ensembl'):
                num_records += 1
                if rec.feature == 'transcript' and 'rRNA' in rec.meta['transcript_biotype']:
                    num_written += 1
                    inter = (rec.chr, str(rec.start), str(rec.stop), rec.strand, rec.meta['transcript_id'])
                    writer.write('\t'.join(inter) + '\n')

    return dict(records=num_records, written=num_written)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    configure_args(parser)
    res = process(parser.parse_args())
    print(res, file=sys.stderr)
