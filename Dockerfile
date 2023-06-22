# FROM mambaorg/micromamba@sha256:7358b481a67025cf0356acf9999cca0625b8c6883977d947b164c173471dfcda
FROM micromamba:0.24.0
COPY --chown=$MAMBA_USER:$MAMBA_GROUP env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes
# add base environment to path to ensure this works in Singularity
# without this, singularity exec and shell will not behave correctly
ENV PATH "$MAMBA_ROOT_PREFIX/bin:$PATH"
USER root
RUN apt-get update && apt-get install -y \
    perl \
    perl-doc \
    cpanminus \
    && rm -rf /var/lib/{apt,dpkg,cache,log}
RUN cpanm Getopt::Long
RUN cpanm Config::Std; rm -rf root/.cpanm; exit 0
USER $MAMBA_USER
COPY gtf.py /usr/local/bin
COPY gtf_metadata.py /usr/local/bin
COPY gtf_refflat.py /usr/local/bin
COPY gtf_rrna.py /usr/local/bin
COPY gtf_tx2gene.py /usr/local/bin
COPY generate_gtf_entry.py /usr/local/bin
COPY gtf2gff3.pl /usr/local/bin
COPY gtf2gff3.cfg /usr/local/bin
