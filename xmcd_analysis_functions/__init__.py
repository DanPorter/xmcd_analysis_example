"""
xmcd analysis functions Module

Various functions for use on XMCD and XAS data analysis
"""

__version__ = '0.1.0'

from .load_scan import load_from_dat, load_from_nxs
from .spectra_container import average_polarised_scans


__all__ = ['load_from_dat', 'load_from_nxs', 'average_polarised_scans', '__version__']