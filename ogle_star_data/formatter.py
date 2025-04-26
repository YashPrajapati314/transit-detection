import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

dat_files = []

for root, dir, files in os.walk('./light_curves_dat/'):
    dat_files = files

os.makedirs("light_curves_csv", exist_ok=True)

for file in dat_files:
    with open(os.path.join("light_curves_dat", file), 'r') as f:
        dat_file = f.read()
    dat_file = dat_file.strip()
    dat_file_rows = dat_file.split('\n')
    data = []
    for row in dat_file_rows:
        row_ls = row.split(' ')
        data.append(row_ls)
    filename_without_extension = file.split('.')[0]
    df = pd.DataFrame(columns=['T', 'Flux', 'E'], data=data)
    df.to_csv(os.path.join("light_curves_csv", f'{filename_without_extension}.csv'), index=False)