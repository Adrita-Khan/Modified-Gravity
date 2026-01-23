"""
Angular Power Spectrum Computation Module
==========================================
Author: Adrita Khan
Date: 16 Jan 2026

This module provides functions for computing angular power spectra using
the Limber approximation:
- Galaxy auto-power spectrum C_ℓ^gg
- Galaxy-CMB lensing cross-power spectrum C_ℓ^κg
"""

import numpy as np
from scipy.integrate import simpson
from cosmology_utils import galaxy_bias
from power_spectrum_utils import check_k_bounds


def compute_Cl_galaxy_auto(ell_array, pk_interp_log, cosmo, z_grid, dNdz, 
                            chi_vals, H_vals, D_vals, D0, c,
                            b0=2.0, beta=0.5, k_min=None, k_max=None):
    """
    Calculate galaxy auto-power spectrum C_ℓ^gg using Limber approximation.
    
    Formula: C_ℓ^gg = ∫ dz (H(z)/c) × [b(z) × n(z)]² × P(k,z) / χ(z)²
    where k = (ℓ + 0.5) / χ(z) (Limber's formula)
    
    Parameters:
        ell_array: Array of multipole moments ℓ
        pk_interp_log: Interpolated log(P(k)) function
        cosmo: pyccl Cosmology object
        z_grid: Redshift grid for integration
        dNdz: Normalized galaxy distribution dN/dz
        chi_vals: Comoving distances χ(z) in Mpc
        H_vals: Hubble parameter H(z) in km/s/Mpc
        D_vals: Growth factors D(z) at all redshifts
        D0: Growth factor at z=0 (must be 1.0)
        c: Speed of light in km/s
        b0: Present-day galaxy bias (default 2.0)
        beta: Bias evolution exponent (default 0.5)
        k_min: Minimum safe k value (default auto)
        k_max: Maximum safe k value (default auto)
    
    Returns:
        C_ℓ^gg for all multipoles
    """
    # Compute galaxy bias and window function
    b_vals = galaxy_bias(D_vals, D0, b0=b0, beta=beta)
    Wg = b_vals * dNdz
    
    Cl = np.zeros_like(ell_array, dtype=float)
    
    for i, ell in enumerate(ell_array):
        # Limber approximation: k = (ℓ + 0.5) / χ(z)
        k_vals = (ell + 0.5) / chi_vals
        
        # Clip k values to safe range if bounds provided
        if k_min is not None and k_max is not None:
            k_safe = check_k_bounds(k_vals, k_min, k_max, ell, "C_ℓ^gg")
        else:
            k_safe = k_vals
        
        # Evaluate power spectrum at z=0
        try:
            logP0 = pk_interp_log(np.log(k_safe))
            P0 = np.exp(logP0)
        except ValueError:
            P0 = np.ones_like(k_vals) * 1e-10
        
        # Scale power spectrum to arbitrary z using growth factor
        # P(k,z) = P(k,z=0) × [D(z) / D(0)]²
        P_kz = P0 * (D_vals / D0)**2
        
        # Limber integral
        integrand = (H_vals / c) * (Wg**2) * P_kz / (chi_vals**2)
        Cl[i] = simpson(integrand, z_grid)
    
    return Cl


def compute_Cl_galaxy_cmb_cross(ell_array, pk_interp_log, cosmo, z_grid, dNdz,
                                 chi_vals, H_vals, D_vals, D0, Wkappa_vals, c,
                                 b0=2.0, beta=0.5, k_min=None, k_max=None):
    """
    Calculate galaxy-CMB lensing cross-power spectrum C_ℓ^κg using Limber approximation.
    
    Formula: C_ℓ^κg = ∫ dz (H(z)/c) × W_κ(z) × b(z) × n(z) × P(k,z) / χ(z)²
    where k = (ℓ + 0.5) / χ(z) (Limber's formula)
    
    Parameters:
        ell_array: Array of multipole moments ℓ
        pk_interp_log: Interpolated log(P(k)) function
        cosmo: pyccl Cosmology object
        z_grid: Redshift grid for integration
        dNdz: Normalized galaxy distribution dN/dz
        chi_vals: Comoving distances χ(z) in Mpc
        H_vals: Hubble parameter H(z) in km/s/Mpc
        D_vals: Growth factors D(z) at all redshifts
        D0: Growth factor at z=0 (must be 1.0)
        Wkappa_vals: CMB lensing kernel W_κ(z)
        c: Speed of light in km/s
        b0: Present-day galaxy bias (default 2.0)
        beta: Bias evolution exponent (default 0.5)
        k_min: Minimum safe k value (default auto)
        k_max: Maximum safe k value (default auto)
    
    Returns:
        C_ℓ^κg for all multipoles
    """
    # Compute galaxy bias and window function
    b_vals = galaxy_bias(D_vals, D0, b0=b0, beta=beta)
    Wg = b_vals * dNdz
    
    Cl = np.zeros_like(ell_array, dtype=float)
    
    for i, ell in enumerate(ell_array):
        # Limber approximation: k = (ℓ + 0.5) / χ(z)
        k_vals = (ell + 0.5) / chi_vals
        
        # Clip k values to safe range if bounds provided
        if k_min is not None and k_max is not None:
            k_safe = check_k_bounds(k_vals, k_min, k_max, ell, "C_ℓ^κg")
        else:
            k_safe = k_vals
        
        # Evaluate power spectrum at z=0
        try:
            logP0 = pk_interp_log(np.log(k_safe))
            P0 = np.exp(logP0)
        except ValueError:
            P0 = np.ones_like(k_vals) * 1e-10
        
        # Scale power spectrum to arbitrary z using growth factor
        # P(k,z) = P(k,z=0) × [D(z) / D(0)]²
        P_kz = P0 * (D_vals / D0)**2
        
        # Limber integral
        integrand = (H_vals / c) * (Wkappa_vals * Wg) * P_kz / (chi_vals**2)
        Cl[i] = simpson(integrand, z_grid)
    
    return Cl
