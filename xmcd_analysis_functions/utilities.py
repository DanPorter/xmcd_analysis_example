
import os
import re
import numpy as np

regex_scan_number = re.compile(r'\d{3,}')

# Constants
class Const:
    pi = np.pi  # mmmm tasty Pi
    e = 1.6021733E-19  # C  electron charge
    h = 6.62606868E-34  # Js  Plank consant
    c = 299792458  # m/s   Speed of light
    u0 = 4 * pi * 1e-7  # H m-1 Magnetic permeability of free space
    me = 9.109e-31  # kg Electron rest mass
    mn = 1.6749e-27 # kg Neutron rest mass
    Na = 6.022e23  # Avagadro's No
    A = 1e-10  # m Angstrom
    r0 = 2.8179403227e-15  # m classical electron radius = e^2/(4pi*e0*me*c^2)
    Cu = 8.048  # Cu-Ka emission energy, keV
    Mo = 17.4808  # Mo-Ka emission energy, keV


def bytes2str(value: str | bytes | list | tuple) -> str:
    """Convert bytes or string to string"""
    if isinstance(value, (str, bytes)):
        return value.decode('utf-8', errors='ignore') if hasattr(value, 'decode') else value
    return bytes2str(next(iter(value), ''))


def get_scan_number(filename: str) -> int:
    """Return scan number from scan filename"""
    filename = os.path.basename(filename)
    match = regex_scan_number.search(filename)
    if match:
        return int(match[0])
    return 0


def photon_wavelength(energy_kev):
    """
    Converts energy in keV to wavelength in A
     wavelength_a = photon_wavelength(energy_kev)
     lambda [A] = h*c/E = 12.3984 / E [keV]
    """

    # Electron Volts:
    E = 1000 * energy_kev * Const.e

    # SI: E = hc/lambda
    lam = Const.h * Const.c / E
    wavelength = lam / Const.A
    return wavelength


def photon_energy(wavelength_a):
    """
    Converts wavelength in A to energy in keV
     energy_kev = photon_energy(wavelength_a)
     Energy [keV] = h*c/L = 12.3984 / lambda [A]
    """

    # SI: E = hc/lambda
    lam = wavelength_a * Const.A
    E = Const.h * Const.c / lam

    # Electron Volts:
    energy = E / Const.e
    return energy / 1000.0


# Polarisation field names inside NeXus groups
# See https://manual.nexusformat.org/classes/base_classes/NXbeam.html#nxbeam
NX_POLARISATION_FIELDS = [
    'incident_polarization_stokes',  # NXbeam
    'incident_polarization',  # NXbeam
    'polarisation',  # DLS specific in NXinsertion_device
]


class PolLabels:
    linear_horizontal = 'lh'
    linear_vertical = 'lv'
    circular_left = 'cl'
    circular_right = 'cr'
    circular_positive = 'pc'  # == circular_right
    circular_negative = 'nc'  # == circular_left
    linear_dichroism = 'xmld'
    circular_dichroism = 'xmcd'


def stokes_from_vector(*parameters: float) -> tuple[float, float, float, float]:
    """
    Return the Stokes parameters from an n-length vector
    """
    if len(parameters) == 4:
        p0, p1, p2, p3 = parameters
    elif len(parameters) == 3:
        p0 = 1
        p1, p2, p3 = parameters
    elif len(parameters) == 2:
        # polarisation vector [h, v]
        h, v = parameters
        p0, p3 = 1, 0
        phi = np.arctan2(v, h)
        p1, p2 = np.cos(2*phi), np.sin(2*phi)
    else:
        raise ValueError(f"Stokes parameters wrong length: {parameters}")
    return p0, p1, p2, p3


def polarisation_label_from_stokes(*stokes_parameters: float):
    """Convert Stokes vector to polarisation mode"""
    p0, p1, p2, p3 = stokes_from_vector(*stokes_parameters)
    circular = abs(p3) > 0.1
    if not circular and p1 > 0.9:
        return PolLabels.linear_horizontal
    if not circular and p1 < -0.9:
        return PolLabels.linear_vertical
    if circular and p3 > 0:
        return PolLabels.circular_right
    if circular and p3 < 0:
        return PolLabels.circular_left
    raise ValueError(f"Stokes parameters not recognized: {stokes_parameters}")


def polarisation_label_to_stokes(label: str) -> tuple[float, float, float, float]:
    """Convert polarisation mode to Stokes vector"""
    label = bytes2str(label).strip().lower()
    match label:
        case PolLabels.linear_horizontal:
            return 1, 1, 0, 0
        case PolLabels.linear_vertical:
            return 1, -1, 0, 0
        case PolLabels.circular_right:
            return 1, 0, 0, 1
        case PolLabels.circular_left:
            return 1, 0, 0, -1
        # assume positive-circular is right-handed
        case PolLabels.circular_positive:
            return 1, 0, 0, 1
        case PolLabels.circular_negative:
            return 1, 0, 0, -1
    return 1, 0, 0, 0


def check_polarisation(label: str) -> str:
    """Return regularised polarisation mode"""
    return polarisation_label_from_stokes(*polarisation_label_to_stokes(label))


def pol_subtraction_label(label: str):
    """Return xmcd or xmld"""
    label = check_polarisation(label)
    if label in [PolLabels.linear_horizontal, PolLabels.linear_vertical]:
        return PolLabels.linear_dichroism
    elif label in [PolLabels.circular_left, PolLabels.circular_right]:
        return PolLabels.circular_dichroism
    else:
        raise ValueError(f"Polarisation label not recognized: {label}")