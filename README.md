# xmcd_analysis_example
Example data analysis of xas spectra from Diamond Light Source.

Includes generation of NeXus files for XAS spectra from beamline i06-1 
and the processing of these spectra to calculate the XMCD spectra.

 - Author: Dan Porter
 - Diamond Light Source Ltd
 - 2025

### Methodology
Scan files from a Synchrotron X-Ray beamline (I06-1 @ Diamond Light Source) are given in the data folder.
Each file is a fast, sweeping energy scan across the Fe L3,2 edge. The different files are for repeated
circular-right (CR) and circular-left (CL) polarisations (note the absolute direction is not known). 

Each scan file contains both electron-yield (TEY) and and fluorescence-yield (TFY) channels.

The code uses pythonic scan and spectra object models to make the analysis clearer (I hope!).

#### Channel Processing steps

For each channel, the following steps are performed:
 - normalise signal by monitor
 - normalise signal by flat pre-edge signal
 - fit a generic background (see below) including a step-edge for each absorption edge
 - subtract the background and normalise by the step height.

#### Averaging and Subtraction
Combining the background-subtracted channels from each scan:
 - interpolate the energy steps to provide consistent spectra
 - average the signals of the scans for each polarisation and channel
 - subtract the averaged signal CR - CL to calculate the XMCD
 - Integrate the XMCD spectra to determine the sum rules.

#### Background subtraction
Various background options are possible and several options are included in the code. 
The examples use an automatic fitted background composed of step models and a polynomial:

##### background = 
 - Step_1[cen=L3, wid=1-3eV, height=2/3 step height] + 
 - Step_2[cen=L2, wid=Step_1, height=1/3 step height] + 
 - Poly[order 3]

The step edges are initially chosen by looking for typical L-edges in the energy window.

More information about the background subtraction options is available in [xmcd_analysis_functions/spectra_analysis.py](xmcd_analysis_functions/spectra_analysis.py)

### Examples
The [xmcd_analysis_example.py](xmcd_analysis_example.py) script uses a suite of functions to generate the NXxas-like NeXus files and the final XMCD file.

The [xmcd_analysis_example.ipynb](xmcd_analysis_example.ipynb) jupyter notebook provides 
further explanation of the analysis steps and the Spectra object model used.


### NeXus Files
XAS energy scans converted into NeXus file with ~NXxas application definition.
Every scan measures both TEY and TFY channels, however the default mode is chosen as TFY.
Each scan has several processing steps. Each processing step is provided as an NXnote in the NXprocessing group, 
and has an associated NXdata containing the signal and background for both channels.

| Polarisation | Original Scan   | Converted Scan                                                                                                                                                                             |
|--------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CR           | data/236463.dat | [236463_nxxas.nxs](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2FDanPorter%2Fxmcd_analysis_example%2Fblob%2F69a249b1bd51acb50412176e0512806be91b15f0%2F236463_nxxas.nxs) |
| CL           | data/236464.dat | [236464_nxxas.nxs](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2FDanPorter%2Fxmcd_analysis_example%2Fblob%2F69a249b1bd51acb50412176e0512806be91b15f0%2F236464_nxxas.nxs) |
| CL           | data/236465.dat | [236465_nxxas.nxs](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2FDanPorter%2Fxmcd_analysis_example%2Fblob%2F69a249b1bd51acb50412176e0512806be91b15f0%2F236465_nxxas.nxs) |
| CR           | data/236466.dat | [236466_nxxas.nxs](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2FDanPorter%2Fxmcd_analysis_example%2Fblob%2F69a249b1bd51acb50412176e0512806be91b15f0%2F236466_nxxas.nxs) |
| CR           | data/236467.dat | [236467_nxxas.nxs](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2FDanPorter%2Fxmcd_analysis_example%2Fblob%2F69a249b1bd51acb50412176e0512806be91b15f0%2F236467_nxxas.nxs) |
| CL           | data/236468.dat | [236468_nxxas.nxs](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2FDanPorter%2Fxmcd_analysis_example%2Fblob%2F69a249b1bd51acb50412176e0512806be91b15f0%2F236468_nxxas.nxs) |
| CL           | data/236469.dat | [236469_nxxas.nxs](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2FDanPorter%2Fxmcd_analysis_example%2Fblob%2F69a249b1bd51acb50412176e0512806be91b15f0%2F236469_nxxas.nxs) |
| CR           | data/236470.dat | [236470_nxxas.nxs](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2FDanPorter%2Fxmcd_analysis_example%2Fblob%2F69a249b1bd51acb50412176e0512806be91b15f0%2F236470_nxxas.nxs) |

Each polarisation is measured 4 times. The background-subtracted spectra are averaged for each polarisation
and subtracted to provide the XMCD spectra, stored in a separate file. 
This NeXus file follows a similar structure to the NXxas files above, but also contains an NXnote in NXprocessing 
giving the integrated XMCD sum rules. 
Please note the methodology used for the sum rules here is not very accurate and needs refining.

 - [236464_nxxas.nxs](https://myhdf5.hdfgroup.org/view?url=https%3A%2F%2Fgithub.com%2FDanPorter%2Fxmcd_analysis_example%2Fblob%2F69a249b1bd51acb50412176e0512806be91b15f0%2Fxmcd.nxs)
