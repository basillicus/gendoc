#!/usr/bin/python3

''' reads the <input_file> file and generates a beamer presentation with the images in that file (one slide per image)
and with the information (INCAR and NOTES files) contained in the image's folder.
INPUT:
    - No input required, but input_file files has to exist in the current folder.
    - files file: Path to the images to be included in the presentantion
       Hint: <input_file> can be generated wiht locate or find -name
            - Use # for coments
            - section|sec "Name of the section" generates a section
            - subsection|ssec "Name of the subsection" generates a subsection
TODO:
    - Add -i input_file and -o output_file when calling the script
    - Add the option to autocompile the document
'''

import os
import sys
import subprocess
import doctools
# import filetools

# TODO: 
# import argparse
# 
# parser = argparse.ArgumentParser(description='Generates a document gathering the information from input file')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
# 
# args = parser.parse_args()
# print args.accumulate(args.integers)

output_file = "documentation.tex"
input_file  = "tip_files"
compile_doc = True
f = open(output_file, "w")

# Files imported this way are Bytes, not strings --> Need to be converted to UTF-8 (decode('UTF-8') function)
cmd = 'cat ' + input_file
files = subprocess.check_output(cmd, shell=True).decode('UTF-8').split("\n") # Stores the output of the cmd
files=files[:-1] # Removing the last item (blank one due to spliting with \n)

# Generate the title, author, institute
doctools.add_header (f,
                     # title           = "NC-AFM Tips Exploration with DFT calculations",
                     # title_short     = "AFM Tips" ,
                     author          = "David Abbasi Pérez",
                     author_short    = "D. Abbasi-Pérez" ,
                     institute       = """King's College London

                     Department of Physics""",
                     institute_short = "KCL")

doctools.add_cover (f)
for file_path in files:
    # Coments will be ignored
    # Ignore commented and empty lines
    # TODO: A line with only blanks breaks the program --> Fix
    if file_path.strip()[0] == "#": continue
    if file_path.strip().split()[0] == "sec" or file_path.strip().split()[0] == "section" :
        sec_name = file_path.strip().split('"')[1]
        doctools.add_section(f,sec_name)
        # KKK
        print ("Section added: " + sec_name )
        continue
    if file_path.strip().split()[0] == "ssec" or file_path.strip().split()[0] == "subsection":
        subsec_name = file_path.strip().split('"')[1]
        # KKK
        print ("subsection added: " + subsec_name)
        doctools.add_subsection(f,subsec_name)
        continue
    # Does nothing in the beamer. AFAIK
    if file_path.strip().split()[0] == "sssec" or file_path.strip().split()[0] == "subsubsection" :
        subsubsec_name = file_path.strip().split('"')[1]
        doctools.add_subsubsection(f,subsubsec_name)
        # KKK
        print ("Subsubection added: " + sec_name )
        continue
    # print ("add slide: " + file_path )
    doctools.add_slide (f,file_path)
doctools.end_document(f)

if compile_doc:
    doctools.compile_doc(output_file)


