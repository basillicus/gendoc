#!/bin/bash

# En cada directorio de la lista de directorios 'list_dir' genera la imagen de la ultima geometria optimizada usando Jmol
# - El fichero que lee es el 'OUTCAR'. Si hay mas OUTCARS.*  NO los lee.
# - Genera un fichero <IMAGE_NAME> 
CWD=$(pwd)
list_dir=$(cat dirs)
IMAGE_NAME="TIP.jpg"

for i in $list_dir; do 
    # Will ask before overwrittin a file, just in case
    # we are passing files by mistake, instead of dir paths
    cd $i
    cat > temp.jmol << EOF
load OUTCAR
color background white
set perspectiveDepth true
animation last
moveto /* time, axisAngle */ 1.0 { -483 -617 -621 126.63}
write image 1600 1200 jpg 95 "$IMAGE_NAME"
EOF
    # If the image does not exist, generate it
    if ! [ -f $IMAGE_NAME ]; then
        jmol -ns temp.jmol
    fi
    rm temp.jmol
    cd $CWD
done
