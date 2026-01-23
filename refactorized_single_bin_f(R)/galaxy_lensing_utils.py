"""
Galaxy and CMB Lensing Utilities Module
========================================
Author: Adrita Khan
Date: 16 Jan 2026

This module provides:
- Galaxy redshift distributions
- CMB lensing kernels
- Window functions for observables
"""

import numpy as np
from scipy.integrate import simpson


def galaxy_number_density_raw(z, z0=0.3):
    """
    Raw galaxy number density (not normalized).
    
    Parameters:
        z: Redshift (scalar or array)
        z0: Characteristic redshift (default 0.3)
    
    Returns:
        n(z) ∝ exp(-z/z0)
    """
    return np.exp(-z / z0)


def normalized_galaxy_distribution(z_array, z0=0.3):
    """
    Normalized galaxy redshift distribution dN/dz.
    
    Formula: dN/dz = (1/N) × exp(-z/z0)
    where N = ∫ exp(-z/z0) dz
    
    Parameters:
        z_array: Array of redshift values
        z0: Characteristic redshift (default 0.3)
    
    Returns:
        Normalized dN/dz such that ∫ dN/dz dz = 1
    
    Raises:
        ValueError: If normalization is invalid
    """
    vals = galaxy_number_density_raw(z_array, z0=z0)
    norm = simpson(vals, z_array)
    
    # Sanity check: normalization must be positive and finite
    if norm <= 0 or not np.isfinite(norm):
        raise ValueError(f"Invalid dN/dz normalization: {norm}")
    
    return vals / norm


def cmb_lensing_kernel(z, cosmo, chi, Om_m, H0, c, z_star=1100.0):
    """
    CMB lensing convergence kernel W_κ(z).
    
    Formula: W_κ(z) = (3/2) Ω_m (H₀/c)² (1+z) χ(z) [χ_star - χ(z)] / χ_star
    
    Parameters:
        z: Redshift (array)
        cosmo: pyccl Cosmology object
        chi: Comoving distance χ(z) in Mpc
        Om_m: Matter density parameter Ω_m at z=0
        H0: Hubble constant in km/s/Mpc
        c: Speed of light in km/s
        z_star: CMB redshift (default 1100.0)
    
    Returns:
        W_κ(z) in units of Mpc⁻²
    """
    from cosmology_utils import comoving_distance
    
    chi_star = comoving_distance(z_star, cosmo)
    
    # Prefactor: (3/2) * Omega_m * (H0/c)^2 with units Mpc^-2
    prefactor = 1.5 * Om_m * (H0 / c)**2
    
    return prefactor * (1.0 + z) * chi * (chi_star - chi) / (chi_star + 1e-30)
