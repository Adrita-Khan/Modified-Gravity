"""
Power Spectrum Utilities Module
================================
Author: Adrita Khan
Date: 16 Jan 2026

This module provides functions for:
- Initializing matter power spectrum emulators
- Computing boost factors for modified gravity
- Interpolating power spectra
"""

import numpy as np
import baccoemu
from emantis.matter_power_spectrum import NonLinearMGBoostEmulator
from scipy.interpolate import interp1d
import os
from contextlib import redirect_stdout, redirect_stderr


def initialize_bacco_emulator(params, k_min=-2, k_max=None, n_k=200, verbose=False):
    """
    Initialize Bacco emulator and compute nonlinear matter power spectrum.
    
    Parameters:
        params: Dict with cosmological parameters
        k_min: Log10 minimum wavenumber (default -2)
        k_max: Log10 maximum wavenumber (default None = emulator max)
        n_k: Number of k points (default 200)
        verbose: Print emulator output (default False)
    
    Returns:
        k: Wavenumber array in h/Mpc
        pk_nl: Nonlinear matter power spectrum in (Mpc/h)^3
        Q_boost: Boost factor (nonlinear/linear)
    """
    with open(os.devnull, 'w') as fnull:
        with redirect_stdout(fnull), redirect_stderr(fnull):
            emulator = baccoemu.Matter_powerspectrum(verbose=verbose)
            
            if k_max is None:
                k_max = np.log10(emulator.emulator['nonlinear']['k'].max())
            
            k = np.logspace(k_min, k_max, num=n_k)
            
            params_bacco = {
                "omega_cold": params["Omega_m"] - params["Omega_b"],
                "sigma8_cold": params["sigma8"],
                "omega_baryon": params["Omega_b"],
                "ns": params["n_s"],
                "hubble": params["h"],
                "neutrino_mass": params.get("M_nu", 0.0),
                "w0": params.get("w0", -1.0),
                "wa": params.get("wa", 0.0),
                "expfactor": params.get("aexp", 1.0)
            }
            
            k, Q_boost = emulator.get_nonlinear_boost(k=k, cold=False, **params_bacco)
            k, pk_nl = emulator.get_nonlinear_pk(k=k, cold=False, **params_bacco)
    
    return k, pk_nl, Q_boost


def initialize_emantis_emulator(verbose=False):
    """
    Initialize e-MANTIS emulator for f(R) gravity boost factors.
    
    Parameters:
        verbose: Print emulator output (default False)
    
    Returns:
        emu: NonLinearMGBoostEmulator object
    """
    return NonLinearMGBoostEmulator(verbose=verbose)


def compute_fR_boost(emantis_emu, params, logfR0, k, aexp=1.0):
    """
    Compute f(R) gravity boost factor using e-MANTIS.
    
    Parameters:
        emantis_emu: e-MANTIS emulator object
        params: Dict with cosmological parameters
        logfR0: Log10(-fR0), e.g., 5 means fR0 = -1e-5
        k: Wavenumber array
        aexp: Scale factor (default 1.0 for z=0)
    
    Returns:
        pk_boost: Boost factor B(k) where P_fR = P_GR × B(k)
    """
    params_emantis = {
        "Omega_m": params["Omega_m"],
        "Omega_b": params["Omega_b"],
        "h": params["h"],
        "n_s": params["n_s"],
        "sigma8_lcdm": params["sigma8"],
        "logfR0": logfR0
    }
    
    return emantis_emu.predict_boost(params_emantis, aexp=aexp, k=k)


def create_power_spectrum_interpolator(k, pk):
    """
    Create log-log interpolator for matter power spectrum.
    
    Parameters:
        k: Wavenumber array
        pk: Power spectrum array
    
    Returns:
        Interpolator function: log(k) -> log(P(k))
    """
    return interp1d(
        np.log(k), 
        np.log(pk + 1e-50),
        kind='cubic', 
        bounds_error=False, 
        fill_value='extrapolate'
    )


def check_k_bounds(k_vals, k_min, k_max, ell, spectrum_name, threshold=0.05):
    """
    Check if k values are within safe bounds and warn if clipping occurs.
    
    Parameters:
        k_vals: Array of k values to check
        k_min: Minimum safe k value
        k_max: Maximum safe k value
        ell: Current multipole value
        spectrum_name: Name of spectrum (for warning messages)
        threshold: Fraction of clipped values to trigger warning (default 0.05)
    
    Returns:
        k_safe: Clipped k values within bounds
    """
    k_safe = np.clip(k_vals, k_min, k_max)
    
    out_of_bounds = (k_vals < k_min) | (k_vals > k_max)
    if np.any(out_of_bounds):
        n_clipped = out_of_bounds.sum()
        if n_clipped > len(k_vals) * threshold:
            print(f"Warning [{spectrum_name}, ℓ={ell:.0f}]: "
                  f"{n_clipped}/{len(k_vals)} k-values clipped")
    
    return k_safe
