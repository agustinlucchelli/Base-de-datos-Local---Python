import pandas as pd

def converti_excel(directorio_csv, directorio_excel):
    read_file = pd.read_csv (directorio_csv)
    read_file.to_excel (directorio_excel, index = None, header=True)