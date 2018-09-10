import os
import requests

import matplotlib.pyplot as plt
import pandas as pd


def get_velo_data(location, year=2015):
    BASE = "https://sandbox.zenodo.org/record/242457/"
    URLS = {2015: BASE + "files/bikes-2015.csv?download=1.csv"}

    if year not in URLS:
        raise ValueError("Year has to be one of 2014, 2015 "
                         "not %s." % year)

    fname = "bikes-%i.csv" % year
    if not os.path.exists(fname):
        with requests.get(URLS[year], stream=True) as r:
            r.raise_for_status()
            with open(fname, 'wb') as w:
                for chunk in r.iter_content(chunk_size=65535):
                    w.write(chunk)

    data = pd.read_csv(fname, parse_dates=True, dayfirst=True, index_col='Datum')

    # filter by location
    data = data[data.Standort == location]

    # subselect only the Velo data
    data = data[["Velo_in", "Velo_out"]]

    data['Total'] = data.Velo_in + data.Velo_out

    return data


mythenquai = get_velo_data('ECO09113499', year=2015)
# rename for easier plotting
mythenquai.columns = ["North", "South", "Total"]

# Compute weekly rides by summing over the 15m intervals
weekly = mythenquai.resample('W').sum()
weekly.plot()

plt.savefig("weekly-2015.png")
