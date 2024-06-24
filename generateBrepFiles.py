#!/usr/bin/env python3

# Export BREP files for the runtime given source FCStd files
# The FCStd files must have a 'Sketch' object which will be exported
# as a BREP file in the same directory as the FCStd file
# Does not depend on the freecad libs, just unzips the file,
# extracts Sketch.Shape.brp to the same location, naming it after the FCStd file

import os
import zipfile
import sys

def extractFromFCStdFile(root:str, fileName:str, sketchName:str='Sketch'):
    """
    Extracts the Sketch.Shape.brp file from the given FCStd file
    """
    baseName = os.path.splitext(fileName)[0]
    sketchFile = f'{sketchName}.Shape.brp'

    with zipfile.ZipFile(os.path.join(root, fileName), 'r') as zip_ref:
        zip_ref.extract(sketchFile, path=root)
        os.rename(os.path.join(root, sketchFile), os.path.join(root, baseName + '.brp'))

def generateBrepFiles(baseDir:str):
    """
    Generate BREP files for all the FCStd files in the given directory
    """
    for root, dirs, files in os.walk(baseDir):
        for file in files:
            if file.endswith('.FCStd'):
                extractFromFCStdFile(root, file)

if __name__ == '__main__':
    generateBrepFiles('resources/profiles')
