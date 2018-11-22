FROM continuumio/miniconda3
RUN conda install -c bioconda blast-legacy biopython beautifulsoup4
RUN git clone https://github.com/NIckp60/ISfinder_database
WORKDIR ISfinder_database
# taken directly from the README
RUN python ISfiner.step1.py step1
RUN python ISfiner.step2.py step1.IS.ID.list outdir
RUN cat outdir/unfinish.task.list
#RUN rm IS.database.tmp.fa
RUN find outdir/ -type f -name 'IS*.seq.fa'|xargs -L 1 -I {} cat {} >> IS.database.tmp.fa
RUN python check.empty.py IS.database.tmp.fa IS.database.fasta
RUN cachebuster=jasjj git clone https://github.com/nickp60/oasis
WORKDIR oasis
RUN git checkout fordocker
RUN wc /ISfinder_database/IS.database.fasta
RUN cp /ISfinder_database/IS.database.fasta  ISFinder_aa.fasta
ADD ./OASIS/OASIS/AnnotatedGenome.py ./OASIS/OASIS/AnnotatedGenome.py
ADD ./OASIS/OASIS/Profile.py ./OASIS/OASIS/Profile.py
ADD ./OASIS/OASIS_main.py ./OASIS/OASIS_main.py
RUN  python ./setup.py install
ENTRYPOINT [ "OASIS" ]
