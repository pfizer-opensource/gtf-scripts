#!/usr/bin/env python3

"""
Create tx2gene.csv for TxImport.

"""

__author__ = 'Rob Moccia'
__version__ = '0.1'

import gtf
import argparse
import sys


def configure_args(parser):
    parser.add_argument('--input', required=True, help='GTF file')
    parser.add_argument('--output', required=True, help='output file')
    parser.add_argument('--version', action='version',
        version='%(prog)s {version}'.format(version=__version__))


def process(args):

    num_records = 0
    num_written = 0

    with open(args.output, 'w') as writer:
        writer.write('transcript_id,gene_id\n')
        with open(args.input, 'r') as reader:
            for rec in gtf.open(reader, 'ensembl'):
                num_records += 1

                if rec.feature == 'transcript':
                    writer.write(rec.meta['transcript_id'] + ',' + rec.meta['gene_id'] + '\n')
                    num_written += 1

    return dict(records=num_records, written=num_written)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    configure_args(parser)
    res = process(parser.parse_args())
    print(res, file=sys.stderr)
