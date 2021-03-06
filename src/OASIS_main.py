#! /usr/bin/env python
"""
OASIS
Created by David Robinson
8/11/08

OASIS is a module designed for IS element annotation for prokaryote genomes.

This is the main module, which uses other modules to perform the annotation.
"""

#imports

import getopt
import sys
import os
import time

from .OASIS import AnnotatedGenome
from .OASIS.OASIS_functions import *
from .OASIS.Constants import *

time1 = time.time()


#functions
def die(err=None, code=2):
	"""print help information and exit"""
	if err:
		print(err)
		print()
	print("./OASIS [options]\n")
	print("OASIS options:")
	print()
	print(" -f folder [String]")
	print(" -g genbank_file [String]")
	print(" -o output_file [String]")
	sys.exit(code)

def bool_translate(a):
	if a.lower() not in ("t", "f", "true", "false"):
		die("argument must be T/F: " + a)
	return {"t":True, "f":False, "true":False, "false":False}[a.lower()]

#classes


def main():
    #Main
    #command line
    args = sys.argv[1:]

    #defaults
    folder, genbank, output, backup = None, None, None, None
    annotated = True
    singles = False
    data_folder = None

    try:
            opts, args = getopt.getopt(sys.argv[1:], "hf:g:o:a:s:r:b:s:d:",
                                       ["help", "folder=", "genbank="])
    except getopt.GetoptError as err:
            die(err)
    for o, a in opts:
            if o in ("-h", "--help"):
                    die()
            elif o in ("-f", "--folder"):
                    folder = a
            elif o in ("-g", "--genbank"):
                    genbank = a
            elif o in ("-o", "--output"):
                    output = a
            elif o in ("-d", "--datafolder"):
                    data_folder = a
            else:
                    assert False, "unhandled option"

    if not folder and not genbank:
            die("Either a genbank file or a folder must be specified")
    if not output:
            die("No output file or folder specified")

    if folder:
            #create output folder if it doesn't exist
            if output not in os.listdir(os.getcwd()):
                    os.mkdir(output)
            for file in os.listdir(folder):
                    # skip non-genbank files
                    if not any(file.endswith(x) for x in [".gb", ".genbank", ".gbk"]): continue

                    fname = os.path.join(folder, file)
                    genome = AnnotatedGenome.AnnotatedGenome(genome_file=fname,
                                                             annotated=annotated)
                    genome.write_annotations(os.path.splitext(fname)[0].split("/")[-1], folder=output)
    elif genbank:

            if not output:
                    die("Output file not specified")
            genome = AnnotatedGenome.AnnotatedGenome(genome_file=genbank,
                                                     annotated=annotated,
                                                     data_folder=data_folder)
            genome.write_annotations(output)


    time2 = time.time()

    difference = time2 - time1

    minutes = int(difference / 60)
    seconds = (difference / 60 - minutes) * 60

    print("Total time:", str(minutes) + ":" + str(seconds))
