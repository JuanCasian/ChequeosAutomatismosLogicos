import os
import re
import zipfile
from shutil import copyfile
import subprocess
import filecmp

# macros necesarios
PROJECT_DIR = './p6'
TMP_DIR = '/tmp/p6Check'
CHECK_FILES_DIR = './testsp6'
ZIP_REGEX = r'.*\.zip'
HACK_REGEX = r'.*\.hack'
NUM_REACTIVOS = 4

print('Resultados de proyecto 6:')

# regex de zip files
fileNames = [
    f"{zipFile.split('.')[0]}" for zipFile in os.listdir(PROJECT_DIR) if bool(re.match(ZIP_REGEX, zipFile))]

# limpiando tmp folder por si se corre más de una vez
os.system(f'rm -rf {TMP_DIR}')

# loop general para pruebas
for fileName in fileNames:
    # unzip de archivos a un directorio temporal
    with zipfile.ZipFile(f'{PROJECT_DIR}/{fileName}.zip', 'r') as zipRef:
        zipRef.extractall(f'{TMP_DIR}/{fileName}')

    # obtiene los archivos hack
    hackFiles = [
        f"{hackFile}" for hackFile in os.listdir(f'{CHECK_FILES_DIR}/') if bool(re.match(HACK_REGEX, hackFile))]

    # testing con hardware simulator
    testPasados = 0
    for hackFile in hackFiles:
        if (filecmp.cmp(f"{CHECK_FILES_DIR}/{hackFile}", f'{TMP_DIR}/{fileName}/{hackFile}')):
            testPasados += 1

    print(f'{fileName}\t{round(testPasados / NUM_REACTIVOS * 100)}')

print("END")
