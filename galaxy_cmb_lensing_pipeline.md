# Galaxy–CMB Lensing Cross-Correlation Pipeline for Cosmological Parameter Inference

## Overview

This pipeline implements a comprehensive framework for constraining cosmological parameters using the cross-correlation between galaxy clustering and Cosmic Microwave Background (CMB) lensing. The analysis combines theoretical predictions with observational data through Bayesian inference and Markov Chain Monte Carlo (MCMC) sampling.

## Table of Contents

1. [Theoretical Framework](#theoretical-framework)
2. [Implementation Structure](#implementation-structure)
3. [Mathematical Foundations](#mathematical-foundations)
4. [Code Components](#code-components)
5. [Usage Guide](#usage-guide)
6. [Parameter Estimation](#parameter-estimation)
7. [Results Visualization](#results-visualization)

---

## Theoretical Framework

### Fundamental Cosmological Model

The analysis assumes a flat ΛCDM (Lambda Cold Dark Matter) cosmological model with the following components:

- **Matter density**: Ωₘ = Ωb + Ωcdm (baryons + cold dark matter)
- **Dark energy density**: ΩΛ = 1 - Ωₘ (cosmological constant)
- **Spatial curvature**: Ωk = 0 (flat universe assumption)

### Key Physical Processes

1. **Galaxy Clustering**: Galaxies trace the underlying dark matter distribution with a bias factor
2. **CMB Lensing**: Gravitational deflection of CMB photons by intervening matter
3. **Cross-Correlation**: Statistical connection between galaxy positions and CMB lensing convergence

---

## Mathematical Foundations

### 1. Hubble Function

**Equation (68):**
```
H(z) = H₀ √[Ωₘ(1+z)³ + ΩΛ]
```

**Physical meaning**: Expansion rate of the universe at redshift z
- **Components**: Matter density Ωₘ dominates at high z, dark energy ΩΛ at low z

### 2. Comoving Distance

```
χ(z) = ∫₀ᶻ c/H(z') dz'
```

**Physical meaning**: Line-of-sight distance to object at redshift z in comoving coordinates
- **Integration**: Numerical integration over cosmic time

### 3. Growth Factor

**Equation (66):**
```
D(z) = g(z)/(1+z)
```

**Growth Function (Equation 67):**
```
g(z) = (5Ω(z)/2) × 1/[Ω(z)^(4/7) - λ(z) + (1 + Ω(z)/2)(1 + λ(z)/70)]
```

**Where:**
```
Ω(z) = Ωₘ(1+z)³ / [Ωₘ(1+z)³ + (1-Ωₘ-ΩΛ)(1+z)² + ΩΛ]    (Eq. 68)

λ(z) = ΩΛ / [Ωₘ(1+z)³ + (1-Ωₘ-ΩΛ)(1+z)² + ΩΛ]              (Eq. 69)
```

**Physical meaning**: How density perturbations grow with cosmic time

### 4. Lensing Kernel Functions

#### CMB Lensing Kernel
**Equation (4.2):**
```
W_κ(z) = (3ΩₘH₀²)/(2c) × (1+z) × χ(z) × [χ* - χ(z)]/χ*
```
- **χ***: Comoving distance to CMB surface (z* ≈ 1100)
- **Physical meaning**: Lensing efficiency of matter at redshift z on CMB photons

#### Galaxy Lensing Kernel
**Equations (4.3) and (4.4):**
```
W_g(z) = b(z) × dN/dz + μ(z)
```

**Magnification term (4.4):**
```
μ(z) = (3ΩₘH₀²)/(2c) × (1+z) × χ(z) × ∫_z^∞ [1 - χ(z)/χ(z')] × (α-1) × dN/dz'(z') dz'
```

**Galaxy bias (4.7):**
```
b(z) = b₀/D*(z)
```
- **α = 2.225**: Magnification bias parameter
- **Physical meaning**: How galaxy observations are affected by lensing magnification

### 5. Power Spectrum Calculations

#### CosmoPower Neural Network
**Input parameters:**
```
θ = {Ωbh², Ωch², h, ns, ln(10¹⁰As), z}
```
**Output:**
```
P(k,z) = NN_CosmoPower(θ)
```
**Physical meaning**: Matter power spectrum at wavenumber k and redshift z

#### Limber Approximation
**3D → 2D projection:**
```
C_ℓ = ∫₀^∞ dz × H(z)/χ²(z) × W_X(z) × W_Y(z) × P(k = ℓ/χ(z), z)
```
**Simplified form:**
```
C_ℓ ≈ P(k = ℓ/χ, z)/χ²
```
**Physical meaning**: Projects 3D matter correlations to 2D angular correlations

### 6. Cross-Correlation Analysis

#### Galaxy-CMB Cross-Correlation
**Full Limber integral:**
```
C_ℓ^(gκ) = (1/c) ∫₀^∞ dz × H(z)/χ²(z) × W_g(z) × W_κ(z) × P_mm(ℓ/χ(z), z)
```

**Practical approximation:**
```
C_ℓ^(gκ) = b_g × η_lens × √[P_g(ℓ/χ_eff, z_g) × P_κ(ℓ/χ_eff, z_κ)] / χ_eff²
```

**Where:**
- **χ_eff = √(χ_g × χ_κ)**: Effective distance
- **η_lens**: Lensing efficiency factor
- **b_g**: Galaxy bias

#### Lensing Efficiency
```
η_lens = W_κ(z_g, z*) / W_κ(z_κ, z*)
```

**CMB Lensing Weight:**
```
W_κ(z, z*) = (3ΩₘH₀²)/(2c) × (1+z) × χ(z) × [χ* - χ(z)]/χ*
```

### 7. Statistical Framework

#### Covariance Matrix
**Cosmic variance formula:**
```
Cov(C_ℓ^XY) = δ_ℓℓ' × 1/((2ℓ+1)f_sky) × [C_ℓ^XX × C_ℓ^YY + (C_ℓ^XY)²]
```

**For galaxy-CMB cross-correlation:**
```
Cov(C_ℓ^gκ) = 2 × C_ℓ^gg × C_ℓ^gκ / [(2ℓ+1) × f_sky]
```
- **f_sky**: Fraction of sky observed
- **Physical meaning**: Statistical uncertainty from finite survey volume

#### Log-Likelihood Function
**Chi-squared statistic:**
```
χ² = (C_ℓ^model - C_ℓ^data)ᵀ × Cov⁻¹ × (C_ℓ^model - C_ℓ^data)
```

**Log-likelihood:**
```
ln ℒ = -½χ²
```

**Posterior probability (Bayes' theorem):**
```
P(θ|D) ∝ ℒ(D|θ) × π(θ)
```
- **θ**: Cosmological parameters {H₀, Ωbh², Ωch², ns, As}
- **π(θ)**: Prior probability distributions

---

## Implementation Structure

### Core Components

1. **`utils.py`**: Fundamental cosmological functions
2. **Main Pipeline**: Data processing and MCMC sampling
3. **Visualization**: Results analysis and plotting

### Dependencies

```python
# Core scientific libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform, norm
from scipy.integrate import quad

# Specialized packages
import pocomc as pc           # Population Monte Carlo sampling
import cosmopower as cp       # Power spectrum emulation
from astropy.cosmology import FlatLambdaCDM
import getdist               # MCMC analysis
import corner                # Posterior visualization
```

---

## Code Components

### `utils.py` Functions

#### Basic Cosmological Functions

```python
def hubble_function(z, H0, Om_m, Om_lambda):
    """Hubble parameter H(z) at redshift z"""
    return H0 * np.sqrt(Om_m * (1 + z)**3 + Om_lambda)

def comoving_distance_proper(z, H0, Om_m, Om_lambda):
    """Comoving distance via numerical integration"""
    def integrand(z_prime):
        return c / hubble_function(z_prime, H0, Om_m, Om_lambda)
    chi, _ = quad(integrand, 0, z)
    return chi
```

#### Growth Factor Calculations

```python
def growth_factor_D(z, H0, Om_m, Om_lambda):
    """Linear growth factor D(z) = g(z)/(1+z)"""
    return growth_function_g(z, H0, Om_m, Om_lambda) / (1 + z)

def growth_function_g(z, H0, Om_m, Om_lambda):
    """Growth function g(z) from Lahav et al. (2004)"""
    Omega_z = compute_Omega_z(z, H0, Om_m, Om_lambda)
    lambda_z = compute_lambda_z(z, H0, Om_m, Om_lambda)
    denom = Omega_z**(4/7) - lambda_z + (1 + Omega_z/2) * (1 + lambda_z/70)
    return (5 * Omega_z / 2) / denom
```

#### Lensing Kernels

```python
def cmb_lensing_kernel(z, z_star, H0, Om_m, Om_lambda):
    """CMB lensing kernel W_κ(z)"""
    chi_z = comoving_distance_proper(z, H0, Om_m, Om_lambda)
    chi_star = comoving_distance_proper(z_star, H0, Om_m, Om_lambda)
    prefactor = (3 * Om_m * H0**2) / (2 * c)
    return prefactor * (1 + z) * chi_z * (chi_star - chi_z) / chi_star

def galaxy_lensing_kernel(z, z_array, dN_dz_func, bias_func, H0, Om_m, Om_lambda):
    """Galaxy lensing kernel W_g(z) including bias and magnification"""
    bias_term = bias_func(z) * dN_dz_func(z)
    # ... magnification calculation ...
    return bias_term + mu_z
```

### Main Pipeline Functions

#### Power Spectrum Interface

```python
def run_cosmopower(H0, ombh2, omch2, ns, As, z):
    """Interface to CosmoPower neural network emulator"""
    h = H0 / 100.0
    cosmology_params = {
        'omega_b': [ombh2 / h**2],
        'omega_cdm': [omch2 / h**2],
        'h': [h],
        'n_s': [ns],
        'ln10^{10}A_s': [np.log(As * 1e10)],
        'z': [z]
    }
    result = cp_nn.ten_to_predictions_np(cosmology_params)
    return result[0]
```

#### Cross-Correlation Analysis

```python
def galaxy_cmb_cross_spectrum(P_k_z_g, P_k_z_k, z_g, z_k, H0, Om0, b_g=1.0, lmax=1000):
    """Compute galaxy-CMB lensing cross-correlation"""
    ell = np.arange(2, lmax + 1)
    chi_g = comoving_distance(z_g, H0, Om0)
    chi_k = comoving_distance(z_k, H0, Om0)
    chi_eff = np.sqrt(chi_g * chi_k)
    
    # Cross-correlation calculation with proper lensing efficiency
    lensing_efficiency = compute_lensing_efficiency_proper(z_g, z_k, H0, Om0, Om_lambda)
    C_ell = b_g * lensing_efficiency * P_k_cross / chi_eff**2
    
    return ell, C_ell
```

#### Likelihood Function

```python
def log_likelihood(params):
    """Compute log-likelihood for parameter estimation"""
    H0, ombh2, omch2, ns, As = params
    
    # Generate theoretical predictions
    P_k_g = run_cosmopower(H0, ombh2, omch2, ns, As, z_g)
    P_k_k = run_cosmopower(H0, ombh2, omch2, ns, As, z_k)
    
    # Compute cross-correlation
    ell, C_gk_model = galaxy_cmb_cross_spectrum(P_k_g, P_k_k, z_g, z_k, H0, Om0)
    
    # Chi-squared calculation
    diff = C_gk_model - C_true_use
    chi2 = np.dot(diff, np.dot(inv_cov_use, diff))
    
    return -0.5 * chi2
```

---

## Parameter Conversions

### Standard Cosmological Parameters
```
h = H₀/100                    [dimensionless Hubble parameter]
Ωb = Ωbh²/h²                 [baryon density parameter]  
Ωc = Ωch²/h²                 [cold dark matter density]
Ωm = Ωb + Ωc                 [total matter density]
ΩΛ = 1 - Ωm                  [dark energy density, flat universe]
As = exp(ln(10¹⁰As))/10¹⁰   [primordial scalar amplitude]
```

### Physical Constants
```
c = 299,792.458 km/s         [speed of light]
α = 2.225                    [magnification bias parameter]
z* ≈ 1100                    [CMB surface redshift]
```

---

## Usage Guide

### 1. Initial Setup

```python
# Define fiducial cosmological parameters
params = {
    'omega_b': [0.0225],         # Baryon density parameter
    'omega_cdm': [0.113],        # Cold dark matter density parameter
    'h': [0.7],                  # Dimensionless Hubble parameter
    'tau_reio': [0.055],         # Reionization optical depth
    'n_s': [0.96],               # Scalar spectral index
    'ln10^{10}A_s': [3.07],      # Log amplitude of primordial scalar perturbations
}

# Set observational parameters
z_g = 0.5                        # Galaxy survey redshift
z_k = 1.0                        # Effective lensing redshift  
f_sky = 0.1                      # Sky fraction = 10%
lmax = 1000                      # Maximum angular scale
```

### 2. Generate Fiducial Spectra

```python
# Convert parameters
H0_fid = h_fid * 100.0
ombh2_fid = omega_b_fid * h_fid**2
omch2_fid = omega_cdm_fid * h_fid**2
As_fid = np.exp(ln10_10_As_fid) / 1e10

# Generate power spectra
P_k_g_fid = run_cosmopower(H0_fid, ombh2_fid, omch2_fid, ns_fid, As_fid, z_g)
P_k_k_fid = run_cosmopower(H0_fid, ombh2_fid, omch2_fid, ns_fid, As_fid, z_k)

# Compute angular power spectra
ell, C_gg_fid = limber_projection(P_k_g_fid, z_g, H0_fid, Om0_fid, lmax)
_, C_kk_fid = limber_projection(P_k_k_fid, z_k, H0_fid, Om0_fid, lmax)
_, C_gk_fid = galaxy_cmb_cross_spectrum(P_k_g_fid, P_k_k_fid, z_g, z_k, H0_fid, Om0_fid, lmax=lmax)
```

### 3. Set Up MCMC Sampling

```python
# Define priors
prior = pc.Prior([
    uniform(loc=H0_fid-10, scale=20),              # H0 ∈ [H0_fid-10, H0_fid+10]
    norm(loc=ombh2_fid, scale=0.003),              # ombh2
    norm(loc=omch2_fid, scale=0.015),              # omch2
    norm(loc=ns_fid, scale=0.015),                 # ns
    norm(loc=As_fid, scale=3e-10)                  # As
])

# Initialize sampler
sampler = pc.Sampler(
    prior=prior,
    likelihood=log_likelihood,
    vectorize=False,
    random_state=42
)

# Run MCMC
sampler.run()
samples, weights, logl, logp = sampler.posterior()
```

---

## Parameter Estimation

### Prior Distributions

| Parameter               | Symbol        | Distribution Type | Center (Mean)       | Width / Range                     |
|-------------------------|---------------|-------------------|----------------------|------------------------------------|
| Hubble constant         | H₀            | Uniform            | H₀_fid ± 10          | Range = [H₀_fid - 10, H₀_fid + 10] |
| Baryon density          | Ωbh²          | Normal             | ombh2_fid            | σ = 0.003                          |
| Cold dark matter density| Ωch²          | Normal             | omch2_fid            | σ = 0.015                          |
| Scalar spectral index   | ns            | Normal             | ns_fid               | σ = 0.015                          |
| Scalar amplitude        | As            | Normal             | As_fid               | σ = 3 × 10⁻¹⁰                     |

### Observational Setup

```
z_g = 0.5                    [galaxy survey redshift]
z_k = 1.0                    [effective lensing redshift]  
f_sky = 0.1                  [sky fraction = 10%]
ℓ_max = 1000                 [maximum angular scale]
ℓ_min = 2                    [minimum angular scale]
```

### Key Physical Scales

#### Angular Scales
```
θ ≈ 1/ℓ                     [angular scale in radians]
θ_deg ≈ 180°/(π×ℓ)          [angular scale in degrees]
```

#### Physical Scales
```
k = ℓ/χ(z)                  [comoving wavenumber]
λ = 2π/k                    [comoving wavelength]  
λ_phys = λ/(1+z)            [physical wavelength]
```

---

## Results Visualization

### 1. Posterior Analysis

```python
# Compute posterior statistics
means = np.average(samples, axis=0, weights=weights)
stds = np.sqrt(np.average((samples - means)**2, axis=0, weights=weights))

# Print results
params_names = ["H₀", "Ωbh²", "Ωch²", "ns", "As"]
fiducial_values = [H0_fid, ombh2_fid, omch2_fid, ns_fid, As_fid]

print("Parameter     | Fiducial | Posterior Mean ± Std")
for i, name in enumerate(params_names):
    print(f"{name:12s} | {fiducial_values[i]:8.5f} | {means[i]:8.5f} ± {stds[i]:8.5f}")
```

### 2. Trace Plots

```python
# Check MCMC convergence
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, name in enumerate(params_names):
    axes[i].plot(samples[:, i], alpha=0.7, linewidth=0.5)
    axes[i].axhline(y=fiducial_values[i], color='red', linestyle='--')
    axes[i].set_title(f'{name} Trace')
    axes[i].set_xlabel('Sample Number')
    axes[i].set_ylabel(name)
```

### 3. Corner Plots

```python
# Using corner.py
fig = corner.corner(
    samples,
    labels=params_names,
    truths=fiducial_values,
    weights=weights,
    show_titles=True,
    quantiles=[0.16, 0.5, 0.84]
)

# Using GetDist
from getdist import MCSamples, plots
samples_gd = MCSamples(samples=samples, weights=weights, names=params_names)
g = plots.get_subplot_plotter()
g.triangle_plot([samples_gd], filled=True, markers=dict(zip(params_names, fiducial_values)))
```

---

## Mathematical Framework Summary

This analysis implements the full theoretical framework for multi-probe cosmology, combining:

- **Galaxy clustering**: Tracing the matter distribution
- **Weak lensing**: Gravitational effects on light propagation  
- **CMB observations**: Cosmic microwave background anisotropies

The pipeline uses **Bayesian inference** to constrain fundamental cosmological parameters through the statistical comparison of theoretical predictions with observational data, providing robust estimates of the universe's composition and evolution.

### Key Innovations

1. **Neural Network Emulation**: Fast power spectrum computation using CosmoPower
2. **Cross-Correlation Analysis**: Joint constraints from multiple observables
3. **Proper Error Propagation**: Realistic covariance matrices accounting for cosmic variance
4. **Robust Sampling**: Population Monte Carlo for efficient posterior exploration

This comprehensive approach enables precise determination of cosmological parameters while properly accounting for theoretical and observational uncertainties.
