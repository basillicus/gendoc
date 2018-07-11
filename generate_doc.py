#!/usr/bin/python3

''' reads the <input_file> file and generates a beamer presentation with the images in that file (one slide per image)
and with the information (INCAR and NOTES files) contained in the image's folder.
<input_files> has to contain the absoulute path to the image to be included in the documentation
INPUT:
    - No input required, but input_file files has to exist in the current folder.
    - files file: Path to the images to be included in the presentantion
       Hint: <input_file> can be generated wiht locate or find -name
            - Use # for coments
            - section|sec "Name of the section" generates a section
            - subsection|ssec "Name of the subsection" generates a subsection
TODO:
    - Add -i input_file and -o output_file when calling the script: Done!
    - Add the option to autocompile the document: Done!
    - Add the option to write the log file
    - FIX: Style compact does not print the last section!!
'''

import os
import sys
import subprocess
import doctools
import argparse
# TODO: 
# import filetools # For mixing two different input_files

parser = argparse.ArgumentParser(description='Generates a document gathering the information from the input file')

parser.add_argument('--infile', '-i',  type=str, nargs='?', default="input_file.txt", dest='input_file',
                     help='''input file containing all the paths to the figures to be included in the document.  # are interpreted as coments.  Sections and subsections can be included as:
                          section|sec "Name of the section"  .or.   subsection|ssec "Name of the subsection"''')
parser.add_argument('--outfile', '-o', type=str, nargs='?', default='documentation.tex', dest='output_file',
                    help='''output .tex file''')
parser.add_argument('--logo', '-l', type=str, nargs='?', default='', dest='logo_file',
                    help='''Include the logo in the cover''')
parser.add_argument('--kind', '-k', type=str, nargs='?', default='general', dest='doc_kind',
                    help='''Defines the kind of document. Opts are: general|compact''')
parser.add_argument( '--compile', '-c', default='True', dest='compile_doc', action='store_true',
                    help='Compile the .tex file to create the .pdf document')
parser.add_argument( '--no-compile', '-nc', dest='compile_doc', action='store_false',
                    help='Do not compile the .tex file ')

# Collecting args into variables
args = parser.parse_args(sys.argv[1:])
compile_doc = args.compile_doc
output_file = args.output_file
input_file  = args.input_file
logo=args.logo_file

doc_kind    = args.doc_kind
file_pile=[] # Used for the compatc kind of document (creats a new slide after 6 images)
force_writing = False

# Checking for errors and consistency
#------------------------------------
if input_file == output_file:
    print ("ERROR: Input file and output file can not be the same.")
    sys.exit()
# Check the input file exists
if not os.path.exists("./"+input_file):
    print ("ERROR: Input file " + input_file + " not found!. Try: ")
    print ("    gendoc -i <input_file> ")
    sys.exit()

# Files imported this way are Bytes, not strings --> Need to be converted to UTF-8 (decode('UTF-8') function)
cmd = 'cat ' + args.input_file
files = subprocess.check_output(cmd, shell=True).decode('UTF-8').split("\n") # Stores the output of the cmd
files=files[:-1] # Removing the last item (blank one due to spliting with \n)

f = open(args.output_file, "w")

# Generate the title, author, institute
doctools.add_header (f,
                     # title           = "NC-AFM Tips Exploration with DFT calculations",
                     # title_short     = "AFM Tips" ,
                     author          = "David Abbasi Pérez",
                     author_short    = "D. Abbasi-Pérez" ,
                     institute       = """King's College London

                     Department of Physics""",
                     institute_short = "KCL")

doctools.add_cover (f,logo)
for file_path in files:
    # Coments will be ignored
    # Ignore commented and empty lines
    # TODO: A line with only blanks breaks the program --> Fix
    if file_path.strip()[0] == "#": continue
    elif file_path.strip().split()[0] == "sec" or file_path.strip().split()[0] == "section" :
        sec_name = file_path.strip().split('"')[1]
        if len(file_pile) > 0:
            doctools.add_compact_slide (f,file_pile,figure_path="", force_writing=True)
        # KKK
        print ("Section added: " + sec_name )
        doctools.add_section(f,sec_name)
        continue
    elif file_path.strip().split()[0] == "ssec" or file_path.strip().split()[0] == "subsection":
        subsec_name = file_path.strip().split('"')[1]
        if len(file_pile) > 0:
            doctools.add_compact_slide (f,file_pile,figure_path="", force_writing=True)
        doctools.add_subsection(f,subsec_name)
        # KKK
        print ("subsection added: " + subsec_name)
        continue
    # Does nothing in the beamer. AFAIK
    elif file_path.strip().split()[0] == "sssec" or file_path.strip().split()[0] == "subsubsection" :
        subsubsec_name = file_path.strip().split('"')[1]
        doctools.add_subsubsection(f,subsubsec_name)
        # KKK
        print ("Subsubection added: " + sec_name )
        continue
    # print ("add slide: " + file_path )
    else:
        if doc_kind == 'general':
            doctools.add_slide (f,file_path)
        elif doc_kind == 'compact':
            # KKK
            # print ("--------------")
            # for i in file_pile:
            #     print (i)
            doctools.add_compact_slide (f,file_pile,file_path, force_writing)


doctools.end_document(f)

if compile_doc:
    doctools.compile_doc(output_file)
