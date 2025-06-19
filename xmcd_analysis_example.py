import numpy as np
import matplotlib.pyplot as plt

from xmcd_analysis_functions import load_from_dat, average_polarised_scans

files = [
    "data/236463.dat",
    "data/236464.dat",
    "data/236465.dat",
    "data/236466.dat",
    "data/236467.dat",
    "data/236468.dat",
    "data/236469.dat",
    "data/236470.dat",
]


print('Load data')
scans = [load_from_dat(f, sample_name='Mn') for f in files]

print('\nAnalysis Steps')
for scan in scans:
    print(scan)
    scan.divide_by_preedge()
    print(scan)
    scan.auto_edge_background()
    print(scan)
    scan.write_nexus(f"{scan.metadata.scan_no}_nxxas.nxs")

print('\nAverage')
pol1, pol2 = average_polarised_scans(*scans)
print(pol1)
print(pol2)

print('\nXMCD subtraction')
xmcd = pol1 - pol2
print(xmcd)
xmcd.write_nexus('xmcd.nxs')







