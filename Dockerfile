FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main

RUN apt-get install -y curl unzip libz-dev

# Kaiju installation
RUN curl -L \
    https://github.com/bioinformatics-centre/kaiju/releases/download/v1.9.0/kaiju-v1.9.0-linux-x86_64.tar.gz -o kaiju-v1.9.0.tar.gz &&\
    tar -xvf kaiju-v1.9.0.tar.gz

ENV PATH /root/kaiju-v1.9.0-linux-x86_64-static:$PATH

# Krona installation
RUN curl -L \
    https://github.com/marbl/Krona/releases/download/v2.8.1/KronaTools-2.8.1.tar \
    -o KronaTools-2.8.1.tar &&\
    tar -xvf KronaTools-2.8.1.tar &&\
    cd KronaTools-2.8.1 &&\
    ./install.pl

# Install Prodigal
RUN curl -L https://github.com/hyattpd/Prodigal/releases/download/v2.6.3/prodigal.linux -o prodigal &&\
    chmod +x prodigal

# Get miniconda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
ENV CONDA_DIR /opt/conda
RUN bash miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Get MegaHIT and Quast
RUN conda create -y -n metassembly python=3.6
RUN conda install -y -n metassembly -c bioconda megahit quast
ENV META_ENV /opt/conda/envs/metassembly/bin

# Create symlink
RUN ln -s $META_ENV/megahit /root/megahit
RUN ln -s $META_ENV/metaquast.py /root/metaquast.py 

# Install metabat2

RUN conda install -y -c bioconda metabat2

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root

