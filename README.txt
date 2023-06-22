# gtf-scripts
A collection of scripts that perform various processing tasks on GTF/GFF files.

## gtf.py
GTF parser written by Dmitri Bichko

## gtf_metadata.py
Converts a GTF file to a tsv with each row representing a gene and associated metadata. This file is useful for annotating downstream analyses.

Usage: python gtf_metadata.py --help

## gtf_tx2gene.py
Converts a GTF file to a two column tsv file associating every transcript ID to its associated gene ID. Used in downstream analysis by tximport.

Usage: python gtf_tx2gene.py --help

## gtf_refflat.py
Converts a GTF file into refflat format. Used by Picard Tools.

## gtf_rrna.py
Converts a GTF file into a ribosomal RNA file required by Picard Tools.

## generate_gtf_entry.py
Creates a new gtf entry for a gene as defined by a simple yaml file. Used by genome_manager.py (separate project -- TODO: add link)

## gtf2gff3.pl / gtf2gff3.cfg
Open source script to convert a GTF file into GFF3 format. The .pl file is the perl script and the .cfg is a default config file that can be used in most cases.

