# Complete Cosmological MCMC Algorithm: Galaxy-CMB Cross-Correlation Analysis

## Overview
This algorithm performs Bayesian parameter estimation for cosmological parameters using the cross-correlation between galaxy positions and Cosmic Microwave Background (CMB) lensing. It uses Markov Chain Monte Carlo (MCMC) sampling to constrain fundamental cosmological parameters.

## Algorithm Structure

### Phase 1: Environment Setup and Dependencies

#### Step 1.1: Install Required Packages
```
Required packages:
- pocomc: MCMC sampler for cosmological inference
- cosmopower: Neural network emulator for cosmological power spectra
- astropy: Astronomical calculations and cosmological models
- getdist: Analysis of Monte Carlo samples
- corner: Corner plots for parameter visualization
- gdown: Google Drive file downloads
- Standard scientific libraries: numpy, scipy, matplotlib
```

#### Step 1.2: Import Libraries and Initialize
```python
import os, gdown, numpy as np, matplotlib.pyplot as plt
from scipy.stats import uniform, norm
from scipy.integrate import quad
import pocomc as pc, cosmopower as cp
from astropy.cosmology import FlatLambdaCDM, Planck18
import getdist, corner
```

#### Step 1.3: Create Directory Structure
```
Create directories:
- "home/": For storing downloaded models
- "plots/": For saving output plots and figures
```

### Phase 2: Parameter Initialization and Model Setup

#### Step 2.1: Define Fiducial Cosmological Parameters
```python
params = {
    'omega_b': [0.0225],      # Baryon density parameter
    'omega_cdm': [0.113],     # Cold dark matter density parameter  
    'h': [0.7],               # Hubble parameter (H₀/100)
    'tau_reio': [0.055],      # Reionization optical depth
    'n_s': [0.96],            # Scalar spectral index
    'ln10^{10}A_s': [3.07]   # Log of primordial amplitude
}
```

#### Step 2.2: Define Physical Constants
```python
c = 299792.458        # Speed of light (km/s)
alpha = 2.225         # Magnification bias parameter
```

#### Step 2.3: Download and Load CosmoPower Model
```
1. Download pre-trained neural network model from Google Drive
2. Load CosmoPower emulator for linear matter power spectrum P(k)
3. Model file: 'PKLIN_NN.pkl' → provides fast P(k) predictions
```

### Phase 3: Core Cosmological Functions

#### Step 3.1: Fundamental Cosmological Functions

**Hubble Function H(z)**
```
H(z) = H₀ × √[Ωₘ(1+z)³ + Ωₗ]
```
- Input: redshift z, cosmological parameters
- Output: Hubble parameter at redshift z
- Physics: Describes expansion rate of universe

**Comoving Distance χ(z)**
```
χ(z) = ∫₀ᶻ c/H(z') dz'
```
- Input: redshift z, cosmological parameters
- Output: comoving distance to redshift z
- Method: Numerical integration using scipy.integrate.quad

#### Step 3.2: Structure Growth Functions

**Growth Factor D(z)**
```
D(z) = g(z)/(1+z)
```
Where g(z) is the growth function:
```
g(z) = (5Ω(z)/2) × 1/[Ω(z)^(4/7) - λ(z) + (1+Ω(z)/2)(1+λ(z)/70)]
```

**Density Parameters Ω(z) and λ(z)**
```
Ω(z) = [Ωₘ(1+z)³] / [Ωₘ(1+z)³ + (1-Ωₘ-Ωₗ)(1+z)² + Ωₗ]
λ(z) = Ωₗ / [Ωₘ(1+z)³ + (1-Ωₘ-Ωₗ)(1+z)² + Ωₗ]
```

### Phase 4: Lensing Kernel Functions

#### Step 4.1: CMB Lensing Kernel
```
W_κ(z) = (3ΩₘH₀²)/(2c) × (1+z) × χ(z) × (χ* - χ(z))/χ*
```
- χ*: comoving distance to CMB (z ~ 1100)
- Describes how matter at redshift z contributes to CMB lensing

#### Step 4.2: Galaxy Lensing Kernel
```
W_g(z) = b(z) × dN/dz + μ(z)
```
Where:
- b(z): galaxy bias function = b₀/D*(z)
- dN/dz: galaxy number density distribution
- μ(z): magnification term from weak lensing

**Magnification Term μ(z)**
```
μ(z) = (3ΩₘH₀²)/(2c) × (1+z) × χ(z) × ∫ᶻᶻ* (1 - χ(z)/χ(z')) × (α-1) × dN/dz'(z') dz'
```

### Phase 5: Power Spectrum Calculations

#### Step 5.1: CosmoPower Interface
```python
def run_cosmopower(H0, ombh2, omch2, ns, As, z):
    # Convert parameters to CosmoPower format
    h = H0 / 100.0
    cosmology_params = {
        'omega_b': [ombh2 / h**2],
        'omega_cdm': [omch2 / h**2], 
        'h': [h],
        'n_s': [ns],
        'ln10^{10}A_s': [np.log(As * 1e10)],
        'z': [z]
    }
    # Get P(k,z) prediction from neural network
    return cp_nn.ten_to_predictions_np(cosmology_params)[0]
```

#### Step 5.2: Limber Projection
Converts 3D matter power spectrum P(k,z) to 2D angular power spectrum C_ℓ:
```
C_ℓ = P(k = ℓ/χ, z) / χ²
```
- Input: P(k,z), redshift z, cosmological parameters
- Output: Angular power spectrum C_ℓ for ℓ = 2 to ℓ_max

### Phase 6: Cross-Correlation Analysis

#### Step 6.1: Galaxy-CMB Cross-Correlation Spectrum
```
C_ℓ^(gκ) = b_g × η_lens × √[P_g(k) × P_κ(k)] / χ_eff²
```
Where:
- b_g: galaxy bias parameter
- η_lens: lensing efficiency factor
- χ_eff: effective distance (geometric mean)
- P_g, P_κ: galaxy and CMB lensing power spectra

#### Step 6.2: Lensing Efficiency Calculation
```
η_lens = W_κ(z_g, z_CMB) / W_κ(z_κ, z_CMB)
```
- Accounts for geometric lensing efficiency
- z_CMB ≈ 1100 (CMB last scattering surface)

### Phase 7: Statistical Analysis Framework

#### Step 7.1: Covariance Matrix Computation
```
Cov(C_ℓ^gκ) = 2 × C_ℓ^gκ × C_ℓ^gg / [(2ℓ+1) × f_sky]
```
- Accounts for cosmic variance and finite survey area
- f_sky: fraction of sky observed
- Diagonal approximation (assumes uncorrelated ℓ modes)

#### Step 7.2: Likelihood Function
```
log L(θ) = -½ × (C_model - C_obs)ᵀ × Cov⁻¹ × (C_model - C_obs)
```
Where:
- θ = [H₀, Ωbh², Ωch², n_s, A_s]: parameter vector
- C_model: theoretical prediction for parameters θ
- C_obs: observed cross-correlation spectrum
- Gaussian likelihood assumption

### Phase 8: Data Preparation Pipeline

#### Step 8.1: Generate Fiducial Spectra
```
For fiducial parameters θ_fid:
1. Compute P_g(k,z_g) using CosmoPower
2. Compute P_κ(k,z_κ) using CosmoPower  
3. Calculate C_ℓ^gg, C_ℓ^κκ, C_ℓ^gκ using Limber projection
4. These serve as "observed" data for testing
```

#### Step 8.2: Data Validation and Masking
```
1. Apply quality cuts: remove invalid/infinite values
2. Create mask for usable ℓ-modes
3. Ensure positive definite covariance matrix
4. Apply regularization if needed (pseudo-inverse)
```

### Phase 9: MCMC Sampling Setup

#### Step 9.1: Prior Distributions
```python
# Define parameter priors
prior = pc.Prior([
    uniform(loc=H0_fid-10, scale=20),    # H₀ ~ Uniform[60,80]
    norm(loc=ombh2_fid, scale=0.003),    # Ωbh² ~ Normal
    norm(loc=omch2_fid, scale=0.015),    # Ωch² ~ Normal  
    norm(loc=ns_fid, scale=0.015),       # n_s ~ Normal
    norm(loc=As_fid, scale=3e-10)        # A_s ~ Normal
])
```

#### Step 9.2: Sampler Configuration
```python
sampler = pc.Sampler(
    prior=prior,                    # Prior distributions
    likelihood=log_likelihood,      # Likelihood function
    vectorize=False,               # Process samples individually
    random_state=42                # Reproducible results
)
```

### Phase 10: MCMC Execution

#### Step 10.1: Sampling Process
```
1. Initialize chains at random positions from prior
2. Propose new parameter values
3. Evaluate likelihood at proposed point
4. Accept/reject based on Metropolis-Hastings criterion
5. Repeat until convergence achieved
6. Extract posterior samples with weights
```

#### Step 10.2: Convergence Monitoring
```
Monitor:
- Effective sample size
- Potential scale reduction factor (R̂)
- Autocorrelation times
- Chain mixing via trace plots
```

### Phase 11: Results Analysis Pipeline

#### Step 11.1: Posterior Statistics
```python
# Compute weighted statistics
means = np.average(samples, axis=0, weights=weights)
stds = np.sqrt(np.average((samples - means)**2, axis=0, weights=weights))

# Generate parameter constraints
for each parameter:
    print(f"{name}: {mean:.5f} ± {std:.5f}")
```

#### Step 11.2: Comparison with Fiducial Values
```
For each parameter θᵢ:
1. Compare posterior mean with input fiducial value
2. Check if fiducial value within 68% confidence interval
3. Assess parameter recovery accuracy
4. Identify potential systematic biases
```

### Phase 12: Visualization Pipeline

#### Step 12.1: Posterior Distribution Plots
```
For each parameter:
1. Create histogram of posterior samples
2. Overlay fiducial (true) value as vertical line
3. Show posterior mean and confidence intervals
4. Save high-resolution figures
```

#### Step 12.2: Trace Plots for Convergence Assessment
```
For each parameter:
1. Plot sample values vs. iteration number
2. Check for proper mixing and stationarity
3. Identify burn-in period
4. Assess chain convergence visually
```

#### Step 12.3: Corner Plots for Parameter Correlations
```
Create multi-dimensional visualization:
1. 1D posteriors on diagonal
2. 2D joint posteriors in off-diagonal panels  
3. Contour levels at 68% and 95% confidence
4. Overlay fiducial values as reference points
```

#### Step 12.4: Two Plotting Libraries Integration
```
Library 1 - corner.py:
- Simple, fast corner plots
- Good for quick visualization
- Customizable aesthetics

Library 2 - GetDist:
- Professional publication-quality plots
- Advanced statistical analysis
- Better handling of sample weights
```

### Phase 13: Quality Control and Validation

#### Step 13.1: Numerical Stability Checks
```
1. Verify covariance matrix invertibility
2. Check for numerical overflow/underflow
3. Validate parameter bounds enforcement
4. Test likelihood function robustness
```

#### Step 13.2: Physical Consistency Tests
```
1. Ensure Ωₘ + Ωₗ ≈ 1 (flat universe)
2. Check derived parameters (age, distance scales)
3. Validate against known cosmological constraints
4. Test limiting cases and approximations
```

### Phase 14: Error Handling and Robustness

#### Step 14.1: Exception Management
```python
try:
    # Core computation
except Exception as e:
    print(f"Error: {e}")
    return -np.inf  # Return invalid likelihood
```

#### Step 14.2: Graceful Degradation
```
1. Use regularized matrix inversion if singular
2. Apply data masks for invalid points
3. Provide fallback approximations
4. Continue analysis with reduced dataset if needed
```

### Phase 15: Output and Results Summary

#### Step 15.1: Numerical Results Export
```
Generate summary files:
1. Parameter constraints table
2. Covariance matrix of parameters
3. Best-fit parameter values
4. Goodness-of-fit statistics
```

#### Step 15.2: Publication-Quality Figures
```
Save plots in multiple formats:
1. PNG for presentations (300 DPI)
2. PDF for publications (vector format)
3. Include proper axis labels and legends
4. Professional color schemes and fonts
```

## Algorithm Complexity and Performance

### Computational Complexity
- **CosmoPower calls**: O(N_samples × N_redshifts) 
- **Limber integrals**: O(N_ℓ × N_k)
- **MCMC sampling**: O(N_samples × likelihood_cost)
- **Total runtime**: ~minutes to hours depending on N_samples

### Memory Requirements
- **Sample storage**: ~MB for typical runs
- **Covariance matrices**: O(N_ℓ²) storage
- **Power spectra**: O(N_k × N_z) per model

### Scalability Considerations
- Can parallelize likelihood evaluations
- CosmoPower enables rapid P(k) computations
- Limber approximation reduces dimensionality

## Scientific Applications

### Primary Use Cases
1. **Cosmological parameter estimation** from large-scale structure
2. **Dark energy constraints** via geometric measurements  
3. **Modified gravity tests** through growth rate measurements
4. **Systematic bias characterization** in galaxy surveys

This algorithm represents a complete, production-ready pipeline for cosmological parameter inference using modern Bayesian methods and fast theoretical predictions.
