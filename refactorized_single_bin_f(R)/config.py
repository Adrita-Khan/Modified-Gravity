"""
Configuration Module
====================
Author: Adrita Khan
Date: 16 Jan 2026

Centralized configuration for cosmological parameters and analysis settings.
Edit this file to change parameters without modifying the main code.
"""

# ========================================================
# Cosmological Parameters
# ========================================================

COSMO_PARAMS = {
    "Omega_m": 0.315,      # Total matter density parameter
    "Omega_b": 0.05,       # Baryon density parameter
    "h": 0.67,             # Reduced Hubble constant (H0 = 100h km/s/Mpc)
    "n_s": 0.96,           # Scalar spectral index
    "sigma8": 0.83,        # Amplitude of matter fluctuations at 8 Mpc/h
    "M_nu": 0.0,           # Total neutrino mass [eV]
    "w0": -1.0,            # Dark energy equation of state at z=0
    "wa": 0.0,             # Time evolution of dark energy EOS
    "aexp": 1.0            # Scale factor (a=1 at z=0)
}

# Transfer function for pyccl
# Options: "eisenstein_hu", "bbks", "boltzmann_class", "boltzmann_camb"
# "boltzmann_camb" - Most accurate, requires CAMB (slower)
# "eisenstein_hu" - Fast analytical approximation (default)
TRANSFER_FUNCTION = "boltzmann_camb"


# ========================================================
# Physical Constants
# ========================================================

C_LIGHT = 299792.458  # Speed of light [km/s]


# ========================================================
# Integration Parameters
# ========================================================

# Redshift integration
Z_MIN = 0.01           # Minimum redshift
Z_MAX = 3.0            # Maximum redshift
N_Z = 500              # Number of redshift points

# Galaxy distribution
Z0_GALAXY = 0.3        # Characteristic redshift for dN/dz


# ========================================================
# Angular Power Spectrum Settings
# ========================================================

# Multipole range
ELL_MIN = 10           # Minimum multipole
ELL_MAX = 2000         # Maximum multipole
N_ELL = 50             # Number of multipole points (log-spaced)


# ========================================================
# Galaxy Bias Parameters
# ========================================================

BIAS_B0 = 2.0          # Present-day galaxy bias b(z=0)
BIAS_BETA = 0.5        # Bias evolution exponent
                       # b(z) = b0 × [D(0)/D(z)]^beta
                       # Recommended values:
                       #   0.0 = constant bias (unrealistic)
                       #   0.5 = moderate evolution (matches observations)
                       #   1.0 = strong evolution (too extreme)


# ========================================================
# Modified Gravity Models
# ========================================================

# f(R) gravity models to test
# logfR0 = n means fR0 = -10^(-n)
FR_VALUES = [4, 5, 6]  # Test fR0 = -1e-4, -1e-5, -1e-6

# For single f(R) model analysis, set:
# SINGLE_FR_MODEL = 5  # Use only fR0 = -1e-5
SINGLE_FR_MODEL = None  # Set to None to compare multiple models


# ========================================================
# Emulator Settings
# ========================================================

# Bacco emulator (matter power spectrum)
BACCO_K_MIN = -2       # Log10 minimum k [h/Mpc]
BACCO_K_MAX = None     # Log10 maximum k (None = use emulator max)
BACCO_N_K = 200        # Number of k points

# e-MANTIS emulator (f(R) boost)
EMANTIS_VERBOSE = False


# ========================================================
# Plotting Settings
# ========================================================

FIGURE_SIZE = (14, 6)          # Figure size [inches]
FIGURE_DPI = 100               # Resolution for saved figures
SAVE_FIGURES = False           # Save figures to disk
OUTPUT_DIR = "./output"        # Directory for saved figures


# ========================================================
# Numerical Settings
# ========================================================

# Safety factors for k-bounds
K_MIN_SAFETY = 1.1    # Multiply emulator k_min by this factor
K_MAX_SAFETY = 0.9    # Multiply emulator k_max by this factor

# Clipping warning threshold
K_CLIP_THRESHOLD = 0.05  # Warn if >5% of k values are clipped


# ========================================================
# Validation Settings
# ========================================================

# Growth factor validation tolerances
D0_TOLERANCE = 1e-6           # Tolerance for D(0) = 1.0
D_DECREASE_FRACTION = 0.90    # Minimum fraction of decreasing D(z) points


# ========================================================
# Preset Configurations
# ========================================================

def load_planck2018_cosmology():
    """Load Planck 2018 best-fit cosmology"""
    return {
        "Omega_m": 0.3153,
        "Omega_b": 0.0493,
        "h": 0.6736,
        "n_s": 0.9649,
        "sigma8": 0.8111,
        "M_nu": 0.06,
        "w0": -1.0,
        "wa": 0.0,
        "aexp": 1.0
    }


def load_desi2024_cosmology():
    """Load DESI 2024 cosmology (example)"""
    return {
        "Omega_m": 0.295,
        "Omega_b": 0.048,
        "h": 0.68,
        "n_s": 0.97,
        "sigma8": 0.82,
        "M_nu": 0.0,
        "w0": -1.0,
        "wa": 0.0,
        "aexp": 1.0
    }


# ========================================================
# Helper Functions
# ========================================================

def get_H0():
    """Get Hubble constant in km/s/Mpc"""
    return COSMO_PARAMS["h"] * 100.0


def get_Omega_Lambda():
    """Get dark energy density (flat universe)"""
    return 1.0 - COSMO_PARAMS["Omega_m"]


def print_config():
    """Print current configuration"""
    print("="*60)
    print("CURRENT CONFIGURATION")
    print("="*60)
    print("\nCosmology:")
    for key, val in COSMO_PARAMS.items():
        print(f"  {key:12s} = {val}")
    
    print(f"\nTransfer Function: {TRANSFER_FUNCTION}")
    print(f"Redshift range: [{Z_MIN}, {Z_MAX}] with {N_Z} points")
    print(f"Multipole range: [{ELL_MIN}, {ELL_MAX}] with {N_ELL} points")
    print(f"\nGalaxy bias: b0={BIAS_B0}, β={BIAS_BETA}")
    print(f"f(R) models: logfR0 = {FR_VALUES}")
    print("="*60)


# Usage example:
# from config import COSMO_PARAMS, load_planck2018_cosmology
# COSMO_PARAMS = load_planck2018_cosmology()
