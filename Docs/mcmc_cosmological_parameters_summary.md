# Cosmological Parameters in the MCMC Pipeline

The implementation defines **six cosmological parameters** in the `params` dictionary; however, only **five** of these parameters are actively incorporated in the MCMC sampling process.

## Parameters in the Dictionary

```python
params = {
    'omega_b': [0.0225],        # Baryon density parameter
    'omega_cdm': [0.113],       # Cold dark matter density parameter  
    'h': [0.7],                 # Reduced Hubble parameter (H₀/100)
    'tau_reio': [0.055],        # Reionization optical depth
    'n_s': [0.96],              # Scalar spectral index
    'ln10^{10}A_s': [3.07]     # Log of primordial scalar amplitude
}
```

## Parameters Actually Used in MCMC (5 parameters)

The MCMC sampling uses **5 parameters**:

1. **H₀** (Hubble constant)
   * Derived from: `h × 100`
   * Fiducial value: `70.0 km/s/Mpc`
   * Prior: Uniform distribution `[60, 80]`
   * **What it measures**: Current expansion rate of the universe

2. **Ωbh²** (Baryon density × h²)
   * Derived from: `omega_b × h²`
   * Fiducial value: `0.01575`
   * Prior: Normal distribution centered on fiducial
   * **What it measures**: Amount of ordinary matter in the universe

3. **Ωch²** (Cold dark matter density × h²)
   * Derived from: `omega_cdm × h²`
   * Fiducial value: `0.0567`
   * Prior: Normal distribution centered on fiducial
   * **What it measures**: Amount of dark matter in the universe

4. **n_s** (Scalar spectral index)
   * Direct from dictionary: `0.96`
   * Prior: Normal distribution centered on fiducial
   * **What it measures**: How primordial fluctuations vary with scale

5. **A_s** (Primordial scalar amplitude)
   * Derived from: `exp(ln10^{10}A_s) / 1e10`
   * Fiducial value: `≈ 2.14 × 10⁻⁹`
   * Prior: Normal distribution centered on fiducial
   * **What it measures**: Strength of primordial density fluctuations

## Parameter NOT Used in MCMC

* **τ_reio** (Reionization optical depth): `0.055`
   * This parameter is defined in the dictionary but **not included** in the MCMC sampling
   * It would typically measure when the first stars reionized the universe

## Missing? 

- **σ₈** (clustering amplitude) — sometimes derived from **A<sub>s</sub>** and **n<sub>s</sub>**

- **w** (dark energy equation of state) — if going beyond ΛCDM

- **Ω<sub>m</sub>** — often computed as: **Ω<sub>c</sub>h² + Ω<sub>b</sub>h² / h²**



## Parameter Conversions in the Code

The code converts between different parameterizations:

```python
# From dictionary format to analysis format
H0_fid = h_fid * 100.0                    # 0.7 → 70.0 km/s/Mpc
ombh2_fid = omega_b_fid * h_fid**2         # 0.0225 × 0.7² = 0.01575
omch2_fid = omega_cdm_fid * h_fid**2       # 0.113 × 0.7² = 0.0567  
As_fid = np.exp(ln10_10_As_fid) / 1e10     # exp(3.07)/1e10 ≈ 2.14×10⁻⁹
```

## Additional Derived Parameters

The code also computes derived parameters:

```python
Om0_fid = omega_b_fid + omega_cdm_fid      # Total matter density ≈ 0.1355
Om_lambda_fid = 1 - Om0_fid                # Dark energy density ≈ 0.8645
alpha = 2.225                              # Magnification bias (fixed)
```

## Summary

The analysis implements a **5-parameter ΛCDM cosmological model** where the fundamental parameters that describe:
* **Expansion rate** (H₀)
* **Matter content** (Ωbh², Ωch²)
* **Primordial fluctuations** (A_s, n_s)

This represents a standard approach in modern cosmology for measuring the basic properties of the universe using galaxy-CMB cross-correlations.
```
