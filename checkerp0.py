import os
import re
import zipfile
from shutil import copyfile

# macros necesarios
PROJECT_DIR = './p0'
TMP_DIR = '/tmp/p0Check'
ZIP_REGEX = r'.*\.zip'
CHECK_REGEX = r'file\.txt'

print('Resultados de proyecto 1:')

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

    # obtiene los archivos para tests
    checkFiles = [
        f"{checkFile}" for checkFile in os.listdir(f'{TMP_DIR}/{fileName}') if bool(re.match(CHECK_REGEX, checkFile))]

    # chequeo
    if (len(checkFiles) != 1):
        print(f'{fileName}\t0')
    else:
        print(f'{fileName}\t100')

print("END")
