```markdown
Cosmological Analysis Utility Functions
=======================================

This module provides a focused set of helper functions for cosmological
calculations relevant to galaxy–CMB lensing cross-correlation studies.

Functionality includes:
- Core Cosmological Functions: Hubble parameter, comoving distance, growth factor, and redshift-dependent densities.
- Lensing Kernel Functions: CMB and galaxy lensing kernels, magnification bias contributions.
- Utility Functions: Numerical integration support and simple bias modeling.

Note: This module does not yet include power spectrum calculations, statistical
analysis tools, or full cross-correlation pipelines. These may be implemented in
future modules.

Based on the standard ΛCDM cosmological model with reference to:
- Lahav et al. (2004)
- Karim et al. (2025)

Author: Adrita Khan  
Date: 01.08.2025
```
"""

import numpy as np
from scipy.integrate import quad
from astropy.cosmology import FlatLambdaCDM

# Physical Constants
c = 299792.458  # km/s (speed of light)
alpha = 2.225   # Magnification bias parameter

# =============================================================================
# FUNDAMENTAL COSMOLOGICAL FUNCTIONS
# =============================================================================

def hubble_function(z, H0, Om_m, Om_lambda):
    """
    Hubble function H(z) using the Friedmann equation.

    From Lahav et al. (2004), Eq. (68):
    H(z) = H₀ × sqrt[Ωₘ(1+z)³ + Ω_Λ]

    Parameters:
    -----------
    z : float or array
        Redshift
    H0 : float
        Present-day Hubble constant [km/s/Mpc]
    Om_m : float
        Matter density parameter
    Om_lambda : float
        Dark energy density parameter

    Returns:
    --------
    float or array
        Hubble parameter at redshift z [km/s/Mpc]
    """
    return H0 * np.sqrt(Om_m * (1 + z)**3 + Om_lambda)


def comoving_distance_proper(z, H0, Om_m, Om_lambda):
    """
    Proper comoving distance calculation using χ(z) = ∫₀ᶻ c/H(z') dz'

    Parameters:
    -----------
    z : float
        Redshift
    H0 : float
        Hubble constant [km/s/Mpc]
    Om_m : float
        Matter density parameter
    Om_lambda : float
        Dark energy density parameter

    Returns:
    --------
    float
        Comoving distance [Mpc]
    """
    def integrand(z_prime):
        return c / hubble_function(z_prime, H0, Om_m, Om_lambda)

    chi, _ = quad(integrand, 0, z)
    return chi


def growth_factor_D(z, H0, Om_m, Om_lambda):
    """
    Linear growth factor D(z) in ΛCDM cosmology.

    From Lahav et al. (2004), Eq. (66):
    D(z) = g(z)/(1+z)

    Parameters:
    -----------
    z : float
        Redshift
    H0, Om_m, Om_lambda : float
        Cosmological parameters

    Returns:
    --------
    float
        Growth factor at redshift z
    """
    g_z = growth_function_g(z, H0, Om_m, Om_lambda)
    return g_z / (1 + z)


def growth_function_g(z, H0, Om_m, Om_lambda):
    """
    Growth function g(z) from Lahav et al. (2004), Eq. (67).

    g(z) = (5Ω(z)/2) × 1/[Ω(z)^(4/7) - λ(z) + (1+Ω(z)/2)(1+λ(z)/70)]

    Parameters:
    -----------
    z : float
        Redshift
    H0, Om_m, Om_lambda : float
        Cosmological parameters

    Returns:
    --------
    float
        Growth function value
    """
    Omega_z = compute_Omega_z(z, H0, Om_m, Om_lambda)
    lambda_z = compute_lambda_z(z, H0, Om_m, Om_lambda)

    denominator = Omega_z**(4/7) - lambda_z + (1 + Omega_z/2) * (1 + lambda_z/70)
    g_z = (5 * Omega_z / 2) * (1 / denominator)

    return g_z


def compute_Omega_z(z, H0, Om_m, Om_lambda):
    """
    Matter density parameter Ω(z) from Lahav et al. (2004), Eq. (68).

    Parameters:
    -----------
    z : float
        Redshift
    H0, Om_m, Om_lambda : float
        Cosmological parameters

    Returns:
    --------
    float
        Matter density parameter at redshift z
    """
    numerator = Om_m * (1 + z)**3
    denominator = Om_m * (1 + z)**3 + (1 - Om_m - Om_lambda) * (1 + z)**2 + Om_lambda
    return numerator / denominator


def compute_lambda_z(z, H0, Om_m, Om_lambda):
    """
    Cosmological constant density parameter λ(z) from Lahav et al. (2004), Eq. (69).

    Parameters:
    -----------
    z : float
        Redshift
    H0, Om_m, Om_lambda : float
        Cosmological parameters

    Returns:
    --------
    float
        Dark energy density parameter at redshift z
    """
    numerator = Om_lambda
    denominator = Om_m * (1 + z)**3 + (1 - Om_m - Om_lambda) * (1 + z)**2 + Om_lambda
    return numerator / denominator


def comoving_distance(z, H0, Om0):
    """
    Comoving distance using astropy.cosmology.

    Parameters:
    -----------
    z : float
        Redshift
    H0 : float
        Hubble constant [km/s/Mpc]
    Om0 : float
        Present matter density parameter

    Returns:
    --------
    float
        Comoving distance [Mpc]
    """
    cosmo = FlatLambdaCDM(H0=H0, Om0=Om0)
    return cosmo.comoving_distance(z).value

# =============================================================================
# LENSING KERNEL FUNCTIONS
# =============================================================================

def cmb_lensing_kernel(z, z_star, H0, Om_m, Om_lambda):
    """
    CMB lensing kernel W_κ(z) from Karim et al. (2025), Eq. (4.2).

    W_κ(z) = (3Ωₘ H₀²)/(2c) × (1+z) × χ(z) × [χ_star - χ(z)]/χ_star

    Parameters:
    -----------
    z : float
        Redshift
    z_star : float
        CMB surface redshift (~1100)
    H0, Om_m, Om_lambda : float
        Cosmological parameters

    Returns:
    --------
    float
        CMB lensing kernel value
    """
    chi_z = comoving_distance_proper(z, H0, Om_m, Om_lambda)
    chi_star = comoving_distance_proper(z_star, H0, Om_m, Om_lambda)

    prefactor = (3 * Om_m * H0**2) / (2 * c)
    kernel = prefactor * (1 + z) * chi_z * (chi_star - chi_z) / chi_star

    return kernel


def galaxy_lensing_kernel(z, z_array, dN_dz_func, bias_func, H0, Om_m, Om_lambda):
    """
    Galaxy lensing kernel W_g(z) from Karim et al. (2025), Eq. (4.3) and (4.4).

    W_g(z) = b(z) × dN/dz + μ(z)

    Parameters:
    -----------
    z : float
        Redshift
    z_array : array
        Redshift array for integration
    dN_dz_func : function
        Galaxy number density function
    bias_func : function
        Galaxy bias function
    H0, Om_m, Om_lambda : float
        Cosmological parameters

    Returns:
    --------
    float
        Galaxy lensing kernel value
    """
    # Bias term
    bias_term = bias_func(z) * dN_dz_func(z)

    # Magnification term μ(z)
    chi_z = comoving_distance_proper(z, H0, Om_m, Om_lambda)

    def integrand(z_prime):
        chi_z_prime = comoving_distance_proper(z_prime, H0, Om_m, Om_lambda)
        return (1 - chi_z / chi_z_prime) * (alpha - 1) * dN_dz_func(z_prime)

    z_star = 10.0  # Approximate upper limit
    integral_term, _ = quad(integrand, z, z_star)

    mu_prefactor = (3 * Om_m * H0**2) / (2 * c) * (1 + z) * chi_z
    mu_z = mu_prefactor * integral_term

    return bias_term + mu_z


def bias_function(z):
    """
    Simple bias function b(z) = b0/D*(z) from Karim et al. (2025), Eq. (4.7).

    Parameters:
    -----------
    z : float
        Redshift

    Returns:
    --------
    float
        Galaxy bias at redshift z
    """
    b0 = 1.0  # Fiducial bias at z=0
    D_star_z = growth_factor_D(z, 70.0, 0.3, 0.7) / growth_factor_D(0, 70.0, 0.3, 0.7)
    return b0 / D_star_z


def galaxy_number_density(z):
    """
    Simple galaxy number density model dN/dz.

    Parameters:
    -----------
    z : float
        Redshift

    Returns:
    --------
    float
        Galaxy number density at redshift z
    """
    z0 = 0.3
    return np.exp(-z/z0)