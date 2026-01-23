"""
Galaxy & CMB Lensing Power Spectra: GR vs f(R) Gravity
=======================================================
Author: Adrita Khan
Date: 16 Jan 2026

Main analysis script for computing and comparing angular power spectra
in General Relativity and f(R) modified gravity theories.
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
import logging
import pyccl as ccl

# Import custom utilities
from cosmology_utils import (
    comoving_distance, hubble_parameter, growth_factor, validate_growth_factor
)
from galaxy_lensing_utils import (
    normalized_galaxy_distribution, cmb_lensing_kernel
)
from power_spectrum_utils import (
    initialize_bacco_emulator, initialize_emantis_emulator,
    compute_fR_boost, create_power_spectrum_interpolator
)
from angular_power_spectrum import (
    compute_Cl_galaxy_auto, compute_Cl_galaxy_cmb_cross
)
from plotting_utils import plot_power_spectra, print_diagnostics

# Suppress warnings
warnings.simplefilter("ignore")
logging.getLogger("py.warnings").setLevel(logging.CRITICAL)


# ========================================================
# Configuration
# ========================================================

# Import configuration
from config import (
    COSMO_PARAMS, C_LIGHT, Z_MIN, Z_MAX, N_Z, Z0_GALAXY,
    ELL_MIN, ELL_MAX, N_ELL, FR_VALUES, BIAS_B0, BIAS_BETA,
    K_MIN_SAFETY, K_MAX_SAFETY, TRANSFER_FUNCTION, print_config
)

# Display configuration
print_config()

# Derived quantities
H0 = COSMO_PARAMS["h"] * 100.0  # Hubble constant in km/s/Mpc
Om_m = COSMO_PARAMS["Omega_m"]


# ========================================================
# Initialize Cosmology
# ========================================================

print("Initializing pyccl cosmology...")
print(f"Using transfer function: {TRANSFER_FUNCTION}")
cosmo_ccl = ccl.Cosmology(
    Omega_c=COSMO_PARAMS["Omega_m"] - COSMO_PARAMS["Omega_b"],
    Omega_b=COSMO_PARAMS["Omega_b"],
    h=COSMO_PARAMS["h"],
    sigma8=COSMO_PARAMS["sigma8"],
    n_s=COSMO_PARAMS["n_s"],
    w0=COSMO_PARAMS["w0"],
    wa=COSMO_PARAMS["wa"],
    m_nu=COSMO_PARAMS["M_nu"],
    transfer_function=TRANSFER_FUNCTION
)


# ========================================================
# Compute Matter Power Spectra
# ========================================================

print("Initializing Bacco emulator for GR matter power spectrum...")
k, pk_nl_gr, Q_boost = initialize_bacco_emulator(COSMO_PARAMS)
pk_interp_gr = create_power_spectrum_interpolator(k, pk_nl_gr)

print("Initializing e-MANTIS emulator for f(R) boost factors...")
emantis_emu = initialize_emantis_emulator()


# ========================================================
# Pre-compute Redshift-Dependent Quantities
# ========================================================

print(f"Pre-computing redshift-dependent quantities (z ∈ [{Z_MIN}, {Z_MAX}])...")
z_grid = np.linspace(Z_MIN, Z_MAX, N_Z)

# Galaxy distribution
dNdz = normalized_galaxy_distribution(z_grid, z0=Z0_GALAXY)

# Cosmological evolution
chi_vals = comoving_distance(z_grid, cosmo_ccl)
H_vals = hubble_parameter(z_grid, cosmo_ccl, H0)

# Growth factors
D_vals = growth_factor(z_grid, cosmo_ccl)
D0 = growth_factor(0.0, cosmo_ccl)

# CMB lensing kernel
Wkappa_vals = cmb_lensing_kernel(
    z_grid, cosmo_ccl, chi_vals, Om_m, H0, C_LIGHT
)


# ========================================================
# Validate Growth Factors
# ========================================================

validation_results = validate_growth_factor(z_grid, D_vals, D0)


# ========================================================
# Compute Angular Power Spectra for GR
# ========================================================

print("\nComputing angular power spectra for GR...")
ell = np.logspace(np.log10(ELL_MIN), np.log10(ELL_MAX), N_ELL)

# Safe k bounds for interpolation
k_min_safe = k.min() * K_MIN_SAFETY
k_max_safe = k.max() * K_MAX_SAFETY

Cl_gg_gr = compute_Cl_galaxy_auto(
    ell, pk_interp_gr, cosmo_ccl, z_grid, dNdz,
    chi_vals, H_vals, D_vals, D0, C_LIGHT,
    b0=BIAS_B0, beta=BIAS_BETA,
    k_min=k_min_safe, k_max=k_max_safe
)

Cl_kg_gr = compute_Cl_galaxy_cmb_cross(
    ell, pk_interp_gr, cosmo_ccl, z_grid, dNdz,
    chi_vals, H_vals, D_vals, D0, Wkappa_vals, C_LIGHT,
    b0=BIAS_B0, beta=BIAS_BETA,
    k_min=k_min_safe, k_max=k_max_safe
)


# ========================================================
# Compute Angular Power Spectra for f(R) Gravity
# ========================================================

fr_results = {"gg": {}, "kg": {}}

for logfR0_val in FR_VALUES:
    print(f"\nComputing angular power spectra for f(R) with logfR0 = {logfR0_val}...")
    
    # Compute f(R) boost and power spectrum
    pk_boost = compute_fR_boost(
        emantis_emu, COSMO_PARAMS, logfR0_val, k, aexp=COSMO_PARAMS["aexp"]
    )
    pk_fR = pk_nl_gr * pk_boost
    pk_interp_fr = create_power_spectrum_interpolator(k, pk_fR)
    
    # Compute angular power spectra
    Cl_gg_fr = compute_Cl_galaxy_auto(
        ell, pk_interp_fr, cosmo_ccl, z_grid, dNdz,
        chi_vals, H_vals, D_vals, D0, C_LIGHT,
        b0=BIAS_B0, beta=BIAS_BETA,
        k_min=k_min_safe, k_max=k_max_safe
    )
    
    Cl_kg_fr = compute_Cl_galaxy_cmb_cross(
        ell, pk_interp_fr, cosmo_ccl, z_grid, dNdz,
        chi_vals, H_vals, D_vals, D0, Wkappa_vals, C_LIGHT,
        b0=BIAS_B0, beta=BIAS_BETA,
        k_min=k_min_safe, k_max=k_max_safe
    )
    
    # Store results
    fr_results["gg"][logfR0_val] = Cl_gg_fr
    fr_results["kg"][logfR0_val] = Cl_kg_fr


# ========================================================
# Plot Results
# ========================================================

print("\nPlotting results...")
fig = plot_power_spectra(
    ell, Cl_gg_gr, Cl_kg_gr, 
    fr_results=fr_results, 
    fR_values=FR_VALUES
)
plt.show()


# ========================================================
# Print Diagnostics
# ========================================================

print_diagnostics(
    z_grid, k, ell, COSMO_PARAMS, D0, D_vals, Cl_gg_gr, Cl_kg_gr
)

print("\nAnalysis complete!")
