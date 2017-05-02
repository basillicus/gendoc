import os
import sys
import subprocess

def add_header (f,title      = "NC-AFM Tips exploration",
                title_short  = "AFM-Tips",
                author       = "David Abbasi-Pérez",
                author_short = "D. Abbasi-Pérez",
                institute    = "KCL",
                institute_short = "Department of Physics",
                date         = "",
                date_short   = ""):

    f.write(
        '''% Type of document
%\\documentclass[serif,9pt]{beamer}
%\\documentclass{beamer}
% \\documentclass[sans-serif,notes=show]{beamer}
\\documentclass[handout,compress]{beamer}
%\\documentclass[serif,notes=show]{beamer}
\\usepackage[utf8]{inputenc} % necesario para los acentos de Pérez
\\usepackage[T1]{fontenc}    % necesario para conservar los _ en los paths
\\usepackage[skip=2pt,font=scriptsize]{caption} % Algo para el caption de las figuras
%\\usepackage[latin1]{inputenc}
%\\usepackage[spanish]{babel}
\\usepackage{multimedia}
%\\usepackage{animate}

\\usepackage{listings} % To include pieces of text or code directly on the report
\\lstset{%
basicstyle=\\small\\ttfamily,
breaklines=true,
columns=fullflexible
}
% NOTE: If the lstlisting block is included as an \\input-ed file, will not generate new pages if the 
% block of text needs to. 
% Use: \\lstinputlisting{fileNameToBeIncluded.txt} inside the main file instead.


% To show the number of frames in the footer
%   \\expandafter\\def\\expandafter\\insertshorttitle\\expandafter{%
                                                              %     \\insertshorttitle\\hfill%
                                                              %     \\insertframenumber\\,/\\,\\inserttotalframenumber}

\\usetheme{Madrid}
\\useoutertheme{miniframes}
%\\setbeamertemplate{mini frames}[default]
\\useinnertheme{circles}
\\usecolortheme{dolphin}
\\title[''' + title_short + " ]{" + title + ''' }
\\author[''' +  author_short +']{' + author + '''}
\\institute[''' + institute_short + ''']{%
                           % Universidad de Oviedo,\n '''
                         + institute + '''}

  %Spain}
\\date[''' + date_short + ''']{% July the 1$^{st}$, 2014
                               }

%\\logo{\\includegraphics[scale=0.03]{figs/uniovi-escudo-plata.pdf}}
%  {Copyleft \\copyright{} 2014. Reproducción permitida bajo los \\\\
%        términos de la licencia de documentación libre GNU.}


\\usepackage{color}
\\definecolor{White}{rgb}{1,1,1}
\\definecolor{Black}{rgb}{0,0,0}
\\definecolor{Red}{rgb}{1,0,0}
\\definecolor{Green}{rgb}{0,1,0}
\\definecolor{TitleBackground}{rgb}{0.35,0.35,0.702}
\\definecolor{Blue}{rgb}{0,0,1}
\\definecolor{Gold}{rgb}{1,0.84,0}
\\definecolor{MintCream}{rgb}{0.96,1,0.98}
\\definecolor{NavyBlue}{rgb}{0,0,0.5}
\\definecolor{highlight}{rgb}{0.9,0.5,0.1}   % Higlighted color

% Remove Navitagion Bar
% \\beamertemplatenavigationsymbolsempty
%\\setbeamertemplate{navigation symbols}{}


% Extra personalization options for the beamer presentation
\\setbeamercolor{title}{fg=white,bg=TitleBackground}
\\begin{document}
\\renewcommand{\\figurename}{}
''')

def add_slide (f,figure_path="",title="", caption=""):
    figure_path=figure_path.strip()
    dirs=figure_path.split("/")[:-1]
    path=""
    for dir in dirs:
        path+=dir + "/"
    # TODO:  parse_outcar() and find_notes()
    incar = parse_incar(path)
    outcar = parse_outcar(path)
    # outcar =""
    notes = find_notes(path)
    # notes = ""

    f.write('''% -------------------------------------------------------------------------
\\begin{frame}
\\frametitle{}
\\begin{columns}
    \\begin{column}{0.5\\textwidth}
        \\begin{figure}[h]
            \\begin{center}
                \\includegraphics[width=0.7\\textwidth]{''' + figure_path + '''}
                 \\caption{}
                \\label{}
            \\end{center}
        \\end{figure}
    \\end{column}
    \\begin{column}{0.5\\textwidth}
        \\begin{block}{INCAR}
           % Include INCAR options
            \\tiny{''' + incar + '''}
        \\end{block}
        \\begin{block}{OUTCAR}
            % Include Parse OUTCAR
            \\tiny{''' + outcar + '''}
        \\end{block}
    \\end{column}
\\end{columns}
\\scalebox{.25}{\\protect\\detokenize{''' + path + '''}}
    \\begin{block}{NOTES}
        % Include NOTES
        \\scalebox{.35}{''' + notes + '''}
    \\end{block}
\\end{frame}

''')

#
# 
# # def add_itemize(items_list=[]):
# # \begin{frame}
# #     \begin{itemize}
# #         for item in item_list:
# #         f.write("\item " + item)
# #     \end{itemize}
# # \end{frame}
# 
# # def add_equation ():
# #      \begin{equation}
# #         equation
# #      \end{equation}
# # 
# 

def add_cover (f):
   f.write('''
\\begin{frame}[plain, label=title]
\\titlepage
\\begin{columns}
    \\begin{column}{0.34\\linewidth}
        \\begin{figure}[h]
            \\begin{center}
                \\includegraphics[scale=0.08]{logo.png}
                \\label{}
            \\end{center}
        \\end{figure}
    \\end{column}
\\end{columns}
\\end{frame}
''')

def add_section (f,section_title=""):
   f.write("\n\\section{%s}\n" % (section_title))

def add_subsection (f,subsection_title=""):
   f.write("\n\\subsection{%s}\n" % (subsection_title))

def add_subsubsection (f,subsubsection_title=""):
   f.write("\n\\subsubsection{%s}\n" % (subsubsection_title))

def end_document(f):
    f.write("\n \\end{document}")

def parse_incar (path):
    ''' extracts INCAR information from the OUTCAR (actual run calculation) in the folder <path> '''

    CWD = os.getcwd()
    os.chdir(path)
    try:
        ifile = open ('OUTCAR','r')
    except:
        print ("No OUTCAR file in: " + path)
        return

    keywords = []
    for line in ifile:
        if line == "\n" : continue
        #if line.strip()[0] == "#" : continue
        if 'EDIFF  ' in line:
            keyword = line.strip().split()[0:3]
            keywords.append(keyword)
        if 'PREC ' in line:
            keyword = line.strip().split()[0:3]
            keywords.append(keyword)
        if 'GGA  ' in line:
            keyword = line.strip().split()[0:3]
            keywords.append(keyword)
        if 'IVDW' in line:
            keyword = line.strip().split()[0:3]
            keywords.append(keyword)
        if 'EDIFFG' in line:
            keyword = line.strip().split()[0:3]
            keywords.append(keyword)
        if 'IBRION' in line:
            keyword = line.strip().split()[0:3]
            keywords.append(keyword)
        if 'ISMEAR' in line:
            keyword = line.strip().split()[0:6]
            keywords.append(keyword)
        if 'POTIM' in line:
            keyword = line.strip().split()[0:3]
            keywords.append(keyword)
        if 'ADDGRID' in line:
            keyword = line.strip().split()[0:3]
            keywords.append(keyword)

    incar = ""
    # Formating the incar
    next_line=False
    for i, keyword in enumerate (keywords):
        if next_line:
            tmp = ''.join(keywords[i])  +  " ; \n"
            next_line=False
        else:
            # Note that keywords[i] es lo mismo que keyword
            tmp = ''.join(keyword) +  " ; "
            next_line=True
    #        print (incar)
        incar += tmp

    # Back to the CWD
    os.chdir(CWD)
    return incar

def parse_outcar (path):
    ''' extracts information from the OUTCAR in the folder <path> '''

    CWD = os.getcwd()
    os.chdir(path)
    try:
        ifile = open ('OUTCAR','r')
    except:
        print ("No INCAR file in: " + path)
        return

    """Reaads OUTCAR type file.
    Reads unitcell, atom positions, energies, and forces from the OUTCAR file.
    CAREFUL: does not explicitly read constraints (yet?)
    Based on "No recuerdo el nombre del Author"'s script
    """
    data    = ifile.readlines()

    natoms  = 0
    images  = []
    # atoms   = Atoms(pbc = True)
    energy  = 0
    atoms   = []
    forces  = []
    species = []
    symbols = []
    species_num = []
    converged = False

    for n,line in enumerate(data):
        if 'VRHFIN' in line:
            temp = line.split('=')
            species.append(temp[1][0:2].strip(':'))
        if 'ions per type' in line:
            temp = line.split()
            for ispecies in range(len(species)):
                species_num += [int(temp[ispecies+4])]
                natoms += species_num[-1]
                for iatom in range(species_num[-1]): symbols += [species[ispecies]]
        if 'direct lattice vectors' in line:
            cell = []
            for i in range(3):
                temp = data[n+1+i].split()
                cell += [[float(temp[0]), float(temp[1]), float(temp[2])]]
        if 'FREE ENERGIE OF THE ION-ELECTRON SYSTEM' in line:
            energy = float(data[n+2].split()[4])
        if 'reached required accuracy' in line: 
            converged = True

    # Formatting the output
    outcar=""
    outcar += "n. atoms = " + str(natoms) + "\n"
    for i in range(len(species)):
        outcar += species[i] + ": " + str(species_num[i]) + "; "
    outcar +="\n\n"
    outcar += "Energy = " + str(energy) + "\n\n"
    if not converged:
        outcar += "WARNING: Calculation not converged!\n"

    os.chdir(CWD)
    return outcar

def find_notes(path):
    ''' extracts information from the OUTCAR in the folder <path> '''

    CWD = os.getcwd()
    os.chdir(path)

    file_found = False
    notes = ""
    list_files = os.listdir("./")
    notes_files=[]
#     print (path + "/n")
#     print (list_files)
    for f in list_files:
        if "note" in f.lower():
            file_found = True
            print ("file NOTES found in " + path )
            notes_files.append(f)
            # temp = open (f,'r')
            # temp_lines = temp.readlines()

    # # Format the thingy
    # if file_found:
    #     for line in temp_lines:
    #         if line == "\n": continue
    #         notes += line + "\n\n"

    # Format the thingy
    if file_found:
        for f in notes_files:
            notes += "\\lstinputlisting{" + path + f + "}\n"

    os.chdir(CWD)
    return notes

def compile_doc (f):
    cmd = "pdflatex " + f + " > /dev/null  2&>1"
    print ("compile_doc: compiling " + f + " as: " + cmd )
    os.system(cmd)
