import subprocess
from shutil import copyfile
import zipfile
import re
import os

# macros necesarios
PROJECT_DIR = './p4'
TMP_DIR = '/tmp/p4Check'
CHECK_FILES_DIR = './testsp4'
ZIP_REGEX = r'.*\.zip'
CHECK_REGEX = r'.*\.tst'
CMP_REGEX = r'.*\.cmp'
ASM_REGEX = r'.*\.asm'
NUM_REACTIVOS = 2

print('Resultados de proyecto 4:')

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
        f"{checkFile}" for checkFile in os.listdir(f'{CHECK_FILES_DIR}/') if bool(re.match(CHECK_REGEX, checkFile))]

    # obtiene los archivos cmp
    cmpFiles = [
        f"{cmpFile}" for cmpFile in os.listdir(f'{CHECK_FILES_DIR}/') if bool(re.match(CMP_REGEX, cmpFile))]

    # copia test files a dir tmp
    for checkFile in checkFiles:
        copyfile(f'{CHECK_FILES_DIR}/{checkFile}',
                 f'{TMP_DIR}/{fileName}/{checkFile}')

    # copia los cmp files a dir tmp
    for cmpFile in cmpFiles:
        copyfile(f'{CHECK_FILES_DIR}/{cmpFile}',
                 f'{TMP_DIR}/{fileName}/{cmpFile}')

    # obtiene los archivos asm
    asmFiles = [
        f"{asmFile}" for asmFile in os.listdir(f'{TMP_DIR}/{fileName}') if bool(re.match(ASM_REGEX, asmFile))]

    # compila machine language a binary file
    for asmFile in asmFiles:
        infoDeAsm = subprocess.run(
            ['./tools/Assembler.sh', f'{TMP_DIR}/{fileName}/{asmFile}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = infoDeAsm.stdout.decode('utf-8').split('\n')[0]

    # testing con CPU Emulator
    testPasados = 0
    for checkFile in checkFiles:
        infoDeTest = subprocess.run(
            ['./tools/CPUEmulator.sh', f'{TMP_DIR}/{fileName}/{checkFile}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = infoDeTest.stdout.decode('utf-8').split('\n')[0]
        if result == 'End of script - Comparison ended successfully':
            testPasados += 1

    print(f'{fileName}\t{round(testPasados / NUM_REACTIVOS * 100)}')

print("END")
