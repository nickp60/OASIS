"""Profile.py
Created by David Robinson
10/22/08

Represents a profile of ISFinder IS families"""

#imports
import os
import re
import shutil
import subprocess
from Bio import SeqRecord
# from Bio.Blast import NCBIStandalone
# from Bio.Blast import NCBIXML
from Bio import SeqIO

from .OASIS_functions import *
from .Constants import *
from . import my_SW

#classes

class Profile:
    """
    describes a profile of ISFinder transposases that can identify their
    gene
    """
    def __init__(self, main_transposase_file):
        """initialized with a fasta file of ISfinder transposases"""
        #save file for future reference
        self.tpase_file = os.path.join(TEMPORARY_DIRECTORY, "aa_db.fasta")

        # copy into local directory
        shutil.copy(main_transposase_file, self.tpase_file)
        os.system(FORMAT_EXE + " -p T -i " + self.tpase_file)

    def identify_family(self, aaseq):
        """given an amino acid sequence, identify its family"""
        blast_file = os.path.join(TEMPORARY_DIRECTORY, "profile_temp.fasta")
        outf = open(blast_file, "w")

        temp_record = SeqRecord.SeqRecord(id="temp", seq=aaseq)

        SeqIO.write([temp_record], outf, "fasta")
        outf.close()

        blast_cmd = "{exe} -p blastn -d {db} -i {query} -m 7".format(
            exe=BLAST_EXE, db=blast_db, query=blast_file)
        result_handle = subprocess.run(blast_cmd,
                                       shell=sys.platform != "win32",
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       check=True)

        try:
            record = next(NCBIXML.parse(result_handle))
        except ValueError:
            raise Exception("BLAST Error")

        best_hsp = None
        best_alignment = None

        #perform blast
        for alignment in record.alignments:
            for hsp in alignment.hsps:
                if hsp.expect < TPASE_MAX_E_VALUE:
                    if best_hsp:
                        if hsp.score > best_hsp.score:
                            best_alignment = alignment
                            best_hsp = hsp
                    else:
                        best_alignment = alignment
                        best_hsp = hsp

        #find family and group
        family = None
        group = None

        if best_hsp:
            fields = re.split("[\s\t]+", best_alignment.title)[1].split("|")
            #best_IS = self.__fetch_by_name(fields[0])
            family, group = fields[2], fields[3]

        #clean up by removing temporary blast file
        os.remove(blast_file)

        return family, group
