"""
Cosmology Utilities Module
===========================
Author: Adrita Khan
Date: 16 Jan 2026

This module provides core cosmological functions for computing:
- Comoving distances
- Hubble parameter evolution
- Growth factors
- Density parameters
- Galaxy bias evolution

All functions use pyccl for robust cosmological calculations.
"""

import numpy as np
import pyccl as ccl
from scipy.integrate import simpson


# Constants
C_LIGHT = 299792.458  # Speed of light in km/s


def comoving_distance(z, cosmo):
    """
    Comoving distance in Mpc using pyccl.
    
    Parameters:
        z: Redshift (scalar or array)
        cosmo: pyccl Cosmology object
    
    Returns:
        Comoving distance in Mpc
    """
    if np.isscalar(z):
        a = 1.0 / (1.0 + z)
        return ccl.comoving_radial_distance(cosmo, a) * cosmo['h']
    else:
        a = 1.0 / (1.0 + np.asarray(z))
        return ccl.comoving_radial_distance(cosmo, a) * cosmo['h']


def hubble_parameter(z, cosmo, H0):
    """
    Hubble parameter H(z) in km/s/Mpc using pyccl.
    
    Parameters:
        z: Redshift (scalar or array)
        cosmo: pyccl Cosmology object
        H0: Hubble constant at z=0 in km/s/Mpc
    
    Returns:
        H(z) in km/s/Mpc
    """
    if np.isscalar(z):
        a = 1.0 / (1.0 + z)
        h_over_h0 = ccl.background.h_over_h0(cosmo, a)
        return H0 * h_over_h0
    else:
        a = 1.0 / (1.0 + np.asarray(z))
        h_over_h0 = ccl.background.h_over_h0(cosmo, a)
        return H0 * h_over_h0


def omega_matter(z, cosmo):
    """
    Matter density parameter Ω_m(z) at redshift z.
    
    Parameters:
        z: Redshift (scalar or array)
        cosmo: pyccl Cosmology object
    
    Returns:
        Ω_m(z)
    """
    if np.isscalar(z):
        a = 1.0 / (1.0 + z)
        return ccl.background.omega_x(cosmo, a, 'matter')
    else:
        a = 1.0 / (1.0 + np.asarray(z))
        return ccl.background.omega_x(cosmo, a, 'matter')


def omega_lambda(z, cosmo):
    """
    Dark energy density parameter Ω_Λ(z) at redshift z.
    
    Parameters:
        z: Redshift (scalar or array)
        cosmo: pyccl Cosmology object
    
    Returns:
        Ω_Λ(z)
    """
    if np.isscalar(z):
        a = 1.0 / (1.0 + z)
        return ccl.background.omega_x(cosmo, a, 'dark_energy')
    else:
        a = 1.0 / (1.0 + np.asarray(z))
        return ccl.background.omega_x(cosmo, a, 'dark_energy')


def growth_factor(z, cosmo):
    """
    Linear growth factor D(z), normalized to D(z=0) = 1.
    
    Physics: D(z) DECREASES with increasing z in expanding universe.
    - At z=0: D(0) = 1.0
    - At z→∞: D(∞) → 0
    
    Parameters:
        z: Redshift (scalar or array)
        cosmo: pyccl Cosmology object
    
    Returns:
        D(z) normalized to D(0) = 1
    """
    if np.isscalar(z):
        a = 1.0 / (1.0 + z)
        return ccl.background.growth_factor(cosmo, a)
    else:
        a = 1.0 / (1.0 + np.asarray(z))
        return ccl.background.growth_factor(cosmo, a)


def validate_growth_factor(z_grid, D_vals, D0):
    """
    Validate growth factor normalization and physical properties.
    
    Parameters:
        z_grid: Array of redshifts
        D_vals: Computed growth factors D(z)
        D0: Growth factor at z=0
    
    Raises:
        ValueError: If growth factors are unphysical
    
    Returns:
        Dict with validation results
    """
    print("="*70)
    print("GROWTH FACTOR VALIDATION")
    print("="*70)
    print(f"D(0) = {D0:.10f}")
    
    # Check 1: D(0) must be exactly 1.0
    if abs(D0 - 1.0) > 1e-6:
        raise ValueError(
            f"CRITICAL ERROR: Growth factor not properly normalized!\n"
            f"  Expected D(0) = 1.0\n"
            f"  Got D(0) = {D0:.10f}\n"
            f"  Difference: {abs(D0 - 1.0):.2e}"
        )
    print("✓ D(0) = 1.0 (correctly normalized)")
    
    # Check 2: Growth factors must be positive everywhere
    if np.any(D_vals <= 0):
        raise ValueError(
            f"CRITICAL ERROR: Non-positive growth factors detected!\n"
            f"  Min D(z) = {D_vals.min():.6f} (at z ≈ {z_grid[np.argmin(D_vals)]:.2f})"
        )
    print("✓ All D(z) > 0 (physically valid)")
    
    # Check 3: Growth should generally decrease with increasing z
    growth_diff = np.diff(D_vals)
    n_decreasing = np.sum(growth_diff < -1e-12)
    n_increasing = np.sum(growth_diff > 1e-12)
    n_neutral = len(growth_diff) - n_decreasing - n_increasing
    
    if n_decreasing < 0.90 * len(growth_diff):
        raise ValueError(
            f"CRITICAL ERROR: Growth factor not decreasing as expected!\n"
            f"  Decreasing: {n_decreasing}/{len(growth_diff)} ({100*n_decreasing/len(growth_diff):.1f}%)"
        )
    print(f"✓ D(z) decreases with z (physically correct)")
    print(f"  Decreasing: {n_decreasing}/{len(growth_diff)} points ({100*n_decreasing/len(growth_diff):.1f}%)")
    
    # Check 4: Growth factor values reasonable
    if D_vals[-1] < 0.1 or D_vals[-1] > D0:
        raise ValueError(
            f"CRITICAL ERROR: Growth factor values out of expected range!\n"
            f"  D(z_max) = {D_vals[-1]:.6f}, expected ~0.15-0.35"
        )
    print(f"✓ Growth factor values reasonable: D(z_max) = {D_vals[-1]:.6f}")
    print("="*70 + "\n")
    
    return {
        "D0": D0,
        "D_max": D_vals[-1],
        "n_decreasing": n_decreasing,
        "n_increasing": n_increasing,
        "validated": True
    }


def galaxy_bias(D_array, D0, b0=2.0, beta=0.5):
    """
    Galaxy bias evolution with tunable exponent.
    
    Formula: b(z) = b₀ × [D(0)/D(z)]^β
    
    Parameters:
        D_array: Growth factor D(z) at all redshifts
        D0: Growth factor at z=0 (should be 1.0)
        b0: Present-day bias (default 2.0)
        beta: Evolution exponent (default 0.5, matches BOSS/eBOSS)
    
    Physical interpretations:
        - beta = 0.0:  Constant bias (too weak)
        - beta = 0.5:  Moderate evolution (RECOMMENDED)
        - beta = 1.0:  Strong evolution (too extreme)
    
    Returns:
        Array of galaxy bias b(z)
    """
    return b0 * (D0 / (D_array + 1e-30))**beta
