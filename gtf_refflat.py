#!/usr/bin/env python3

"""
Convert GTF to UCSC's "refFlat" format, as required by CollectRnaSeqMetrics.

Description from UCSC schema documentation:

  **Gene Predictions and RefSeq Genes**

  The following definition is used for gene prediction tables. In alternative-splicing situations, each transcript has a row in this table.

  A version of genePred that associates the gene name with the gene prediction information. In alternative splicing situations each transcript has a row in this table.

  **table refFlat**

  ::

    'A gene prediction with additional geneName field.'

      string  geneName;           "Name of gene as it appears in Genome Browser."
      string  name;               "Name of gene"
      string  chrom;              "Chromosome name"
      char[1] strand;             "+ or - for strand"
      uint    txStart;            "Transcription start position"
      uint    txEnd;              "Transcription end position"
      uint    cdsStart;           "Coding region start"
      uint    cdsEnd;             "Coding region end"
      uint    exonCount;          "Number of exons"
      uint[exonCount] exonStarts; "Exon start positions"
      uint[exonCount] exonEnds;   "Exon end positions"

  notes:
    - for transcripts without cds regions, refFlat outputs 'txEnd' for both 'cdsStart' and 'cdsEnd'
    - exon position lists have a trailing ',' for some reason
    - exons need to be sorted by start position (this only cost me 2 days of my life)

"""

__author__ = 'Dmitri Bichko, Rob Moccia'
__version__ = '0.1'

import gtf
import argparse
import sys
from itertools import chain


def configure_args(parser):
    parser.add_argument('--input', required=True, help='GTF file')
    parser.add_argument('--output', required=True, help='output file')
    parser.add_argument('--version', action='version',
        version='%(prog)s {version}'.format(version=__version__))

def process(args):

    num_records = 0
    num_written = 0
    num_gene = 0
    num_tran = 0
    num_exon = 0
    num_cds = 0

    tran = None

    # ensembl gtf files are sorted by gene_id and transcript_id
    with open(args.output, 'w') as writer:
        with open(args.input, 'r') as reader:
            for rec in chain(gtf.open(reader, 'ensembl'), [None]):

                # chained end marker to flush the last record
                if not rec or (tran and tran.id != rec.transcript_id):

                    if not tran.cds_start:
                        tran.cds_start, tran.cds_stop = tran.stop, tran.stop
                    else:
                        num_cds += 1

                    tran.exons.sort(key=lambda e: e.start)
                    flat = [tran.gene_id, tran.transcript_id, tran.chr, tran.strand, tran.start, tran.stop, tran.cds_start, tran.cds_stop]
                    flat += [len(tran.exons)]
                    flat += [','.join(str(e.start) for e in tran.exons) + ',']
                    flat += [','.join(str(e.stop) for e in tran.exons) + ',']
                    writer.write('\t'.join(str(f) for f in flat) + '\n')

                    num_written += 1
                    if not rec:
                        break

                # ucsc is "half-open" zero index
                rec.start = rec.start - 1
                num_records += 1

                if rec.feature == 'gene':
                    num_gene += 1
                    tran = None
                elif rec.feature == 'transcript':
                    num_tran += 1
                    tran = rec
                    tran.exons = []
                    tran.cds_start = None
                    tran.cds_stop = None
                elif rec.feature == 'CDS':
                    if not tran.cds_start or rec.start < tran.cds_start:
                        tran.cds_start = rec.start
                    if not tran.cds_stop or rec.stop > tran.cds_stop:
                        tran.cds_stop = rec.stop

                elif rec.feature == 'exon':
                    num_exon += 1
                    tran.exons.append(rec)

    return dict(records=num_records, written=num_written, genes=num_gene, transcripts=num_tran, exons=num_exon, cds=num_cds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    configure_args(parser)
    res = process(parser.parse_args())
    print(res, file=sys.stderr)
