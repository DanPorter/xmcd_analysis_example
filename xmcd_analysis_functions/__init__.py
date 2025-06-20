"""
xmcd analysis functions Module

Various functions for use on XMCD and XAS data analysis

Most of the code here is taken from mmg_toolbox:
https://github.com/DanPorter/mmg_toolbox

File Explanation:
utilities.py - various useful functions from type conversions to x-ray polarisation labels
dat_file_reader.py - reads .dat files into a DataHolder structure
nexus_functions.py - various useful functions for extracting data from NeXus files
nexus_writer.py - functions for adding NeXus groups and datasets to HDF5 files
spectra_analysis.py - general functions for analysis of x-ray absorption spectra
spectra.py - defines the Spectra object class
spectra_container.py - defines the SpectraContainer object class
load_scan.py - extracts scan data and metadata from .dat and .nxs files, returning SpectraContainer
"""

__version__ = '0.1.0'

from .load_scan import load_from_dat, load_from_nxs
from .spectra_container import average_polarised_scans


__all__ = ['load_from_dat', 'load_from_nxs', 'average_polarised_scans', '__version__']