# Modified Gravity with Cross-Correlation

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Issues](https://img.shields.io/badge/issues-0_open-green.svg)](https://github.com/Adrita-Khan/Modified-Gravity/issues)
[![Stars](https://img.shields.io/badge/stars-welcome-brightgreen.svg)](https://github.com/Adrita-Khan/Modified-Gravity/stargazers)

*Note: This project is ongoing and subject to continuous advancements and modifications.*

The project aims to **forecast the signatures of modified gravity theories** through cross-correlation analyses. It is a project of [Dunlap Institute](https://www.dunlap.utoronto.ca/) in collaboration with [CASSA](https://cassa.site/) and [CCDS](https://ccds.ai/).


---

## Why Modified Gravity?

While the ΛCDM framework fits many observations, it relies on undetected dark energy and dark matter. Modified gravity theories offer an alternative explanation for cosmic acceleration and large-scale structure formation, without invoking unknown components. These theories modify the Poisson equation and gravitational potentials, creating observable signatures in the large-scale structure of the Universe, which can be tested through galaxy clustering and weak lensing.

---

### Theories to be Tested

The project will test the following modified gravity theories:

* **f(R) Gravity**: Replaces the Ricci scalar $R$ in the Einstein-Hilbert action with a function $f(R)$, predicting scale-dependent growth rates and modified lensing potentials.
* **DGP Gravity**: A braneworld scenario where gravity leaks into an extra dimension at large scales, leading to cosmic acceleration without a cosmological constant.

---

## Why Cross-Correlation?

Cross-correlation techniques break degeneracies between cosmological parameters and reduce systematic errors by combining uncorrelated datasets. 

```mermaid
graph TD
    A[Single Probe] --> B[Parameter Degeneracies]
    A --> C[Systematic Uncertainties]
    
    D[Cross-Correlation] --> E[Break Degeneracies]
    D --> F[Reduce Systematics]
    D --> G[Amplify Signal]
    
    E --> H[Improved Constraints]
    F --> H
    G --> H
```

**Advantages:**

* **Break degeneracies** between cosmological parameters
* **Mitigate systematics** through uncorrelated noise cancellation
* **Amplify signals** via joint analysis of multiple tracers

This method also amplifies signal strength, particularly for:

* **Galaxy–Galaxy Clustering** ($C_\ell^{gg}$)
* **Galaxy–CMB Lensing Cross-Correlation** ($C_\ell^{\kappa g}$)

These observables provide insights into structure growth and gravitational lensing effects, crucial for probing modified gravity.

---

## Project Description

This project involves calculating and analyzing the following power spectra:

* **Galaxy–Galaxy power spectrum** ($C_\ell^{gg}$) — *auto-correlation*
* **Galaxy–CMB lensing cross-power spectrum** ($C_\ell^{\kappa g}$) — *cross-correlation*

Both theoretical models (e.g., CosmoPower, MGemu emulator) and observational data from LSST/DESC and the Simons Observatory are used.

---

## Goals

### Forecasting Capability

The project forecasts the ability of future cosmological surveys to constrain modified gravity theories. Using mock observations and theoretical predictions, the framework evaluates how well upcoming data can differentiate between General Relativity and alternative gravity models.

The forecasting pipeline includes:

* **Synthetic Observables**: Theoretical power spectra from various MG models, using tools like **CAMB**, **MGemu Emulator**, and **PPF** formalisms.
* **Survey Modeling**: Incorporation of survey characteristics (e.g., sky coverage, galaxy density) from LSST/DESC and Simons Observatory.
* **Fisher Matrix Analysis**: Quantifies the precision of cosmological and MG parameter constraints.
* **Bias and Degeneracy Evaluation**: Assesses degeneracies between MG and ΛCDM parameters.
* **Emulator-Based Acceleration**: Speeds up parameter space exploration using **MGemu Emulator**.

This pipeline provides a **forecasting tool for MG detectability** by assessing how specific MG models affect cross-correlation observables.

---

### Literature Review

* [ ] Review of Power Spectrum and 2PCF under linear theory
* [ ] Study of [HEALPix](https://healpix.sourceforge.io) and `healpy` for spherical map handling
* [ ] Exploration of key modified gravity theories (e.g., f(R), Horndeski, DGP)
* [ ] Understanding of [CosmoPower](https://alessiospuriomancini.github.io/cosmopower/)
* [ ] Exploration of [MGemu Emulator](https://github.com/LSSTDESC/mgemu) for rapid power spectrum computation

### Project Sketch

* [ ] Custom functions for Galaxy–Galaxy power spectrum and Galaxy–CMB lensing cross-power spectrum
* [ ] Integration of realistic survey specifications from LSST/DESC and Simons Observatory
* [ ] Visualization and interpretation of theoretical and observational power spectra

---

### Key Components

| Component                 | Description                                 | Tools                         |
| ------------------------- | ------------------------------------------- | ----------------------------- |
| **Synthetic Observables** | Generate theoretical power spectra          | CosmoPower, MGemu Emulator    |
| **Survey Modeling**       | Incorporate realistic survey specifications | LSST/DESC, Simons Observatory |
| **Fisher Analysis**       | Forecast parameter constraints              | Custom Fisher matrix code     |
| **Emulator Integration**  | Accelerate parameter space exploration      | Neural network interpolation  |

---

## Methodology for Cross-Correlation Forecasting of Modified Gravity Signatures

The approach for forecasting signatures of modified gravity involves cross-correlations between the **Simons Observatory (SO)** and **Legacy Survey of Space and Time (LSST)** at the Vera C. Rubin Observatory.

---

### 1. **Theoretical Framework**

Key models include:

* **f(R) Gravity**: Modifications to General Relativity (GR) by altering the Ricci scalar $R$.
* **DGP Gravity**: Extra dimensions affect gravitational interactions.

Key Parameters:

* **$f_R0$**: Amplitude of f(R) modifications.
* **$\gamma$**: Growth index in DGP models.

---

### 2. **Data Acquisition**

* **Simons Observatory (SO)**: CMB Lensing Maps and tSZ Effect for studying large-scale structure and galaxy clusters.
* **LSST at Rubin Observatory**: Galaxy Clustering and Weak Lensing for mapping matter density and cosmic shear.

---

### 3. **Cross-Correlation Techniques**

Power Spectra Analysis:

* **Galaxy–Galaxy (GG, $C_\ell^{gg}$)** — *auto-correlation*
* **Galaxy–CMB Lensing (GCMB, $C_\ell^{\kappa g}$)** — *cross-correlation*

Using a **multi-tracer approach**, data from different sources are combined to enhance signal-to-noise and reduce systematics.

---

### 4. **Forecasting and Statistical Analysis**

* **Fisher Matrix Forecasting**: Quantifies parameter constraints and breaks degeneracies between cosmological parameters.
* **Emulator-Based Acceleration**: Uses **MGemu Emulator** for rapid computation of power spectra across parameter grids.

---

### 5. **Implementation Tools**

* **CosmoPower**: Theoretical power spectra generation.
* **HEALPix and healpy**: Spherical data handling.
* **JAX**: Optimization of computational pipelines.
* **MGemu Emulator**: Fast computation of MG model spectra.

---

### 6. **Interpretation and Visualization**

* **Parameter Sensitivity**: Assess the impact of MG parameters on observables.
* **Survey Specifications**: Simulate realistic measurements with survey details.
* **Bias Evaluation**: Identify biases and systematics in parameter estimation due to MG effects.

---

## 📁 Repository Structure

```bash
├── data/                  # Simulated or observed data inputs
├── notebooks/             # Jupyter notebooks
├── src/                   # Core functions for spectra calculation
│   └── cross_power.py     # Functions for GG, GCMB, CMBCMB spectra
├── plots/                 # Output plots
├── configs/               # Survey specs and theory parameters
├── Dockerfile             # Docker environment file (GPU enabled)
├── README.md              # Project documentation
├── requirements.txt       # Dependencies (CosmoPower, healpy, etc.)
```

---

*This repository offers a comprehensive resource for understanding, testing, and contributing to the Modified Gravity project. It includes theoretical models, observational data, and tools for computing cross-correlated power spectra, focusing on testing theories like f(R) and DGP using advanced computational methods and survey simulations.*

---



## References

### Emulators
| Category | Emulator | Paper | Documentation |
|----------|----------|-------|---------------|
| **Modified Gravity** | **nDGP** | [Fiorini 2023](https://arxiv.org/pdf/2310.05786) | [Docs](https://github.com/BartolomeoF/nDGPemu) |
| | **e-mantis** | [Sáez-Casares 2023](https://arxiv.org/pdf/2303.08899) | [Docs](https://e-mantis.pages.obspm.fr/e-mantis/main/index.html) |
| **LambdaCDM** | **Bacco** | [Aricò 2020](https://arxiv.org/pdf/2011.15018) | [Docs](https://baccoemu.readthedocs.io/) |

### Statistical & Sampling Tools
| Tool | Documentation |
|------|---------------|
| **emcee** | [emcee.readthedocs.io](https://emcee.readthedocs.io/en/stable/) |
| **pocoMC** | [pocomc.readthedocs.io](https://pocomc.readthedocs.io/en/latest/) |
| **Corner** | [corner.readthedocs.io](https://corner.readthedocs.io/en/latest/) |
| **GetDist** | [getdist.readthedocs.io](https://getdist.readthedocs.io/en/latest/) |

### Astropy Cosmology
| Resource | Link |
|----------|------|
| [Overview](https://docs.astropy.org/en/stable/cosmology/index.html) • [Base API](https://docs.astropy.org/en/latest/api/astropy.cosmology.Cosmology.html) • [Units](https://docs.astropy.org/en/latest/cosmology/units.html) | General |
| [LambdaCDM](https://docs.astropy.org/en/stable/api/astropy.cosmology.LambdaCDM.html) • [FlatLambdaCDM](https://docs.astropy.org/en/stable/api/astropy.cosmology.FlatLambdaCDM.html) • [FlatwCDM](https://docs.astropy.org/en/stable/api/astropy.cosmology.FlatwCDM.html) • [FLRW](https://docs.astropy.org/en/stable/api/astropy.cosmology.FLRW.html) | Models |
| [Planck18](https://docs.astropy.org/en/latest/api/astropy.cosmology.realizations.Planck18.html) • [Redshift-Distance Units](https://docs.astropy.org/en/stable/api/astropy.cosmology.units.redshift_distance.html) | Utilities |

### Angular Power Spectra & Correlations
**NaMaster**: [GitHub](https://github.com/LSSTDESC/NaMaster) • [Docs](https://namaster.readthedocs.io/en/latest/) • [Covariances](https://namaster.readthedocs.io/en/latest/3Covariances.html)  
**CCL**: [Docs](https://ccl.readthedocs.io/en/latest/)

### LSSTDESC Tutorials
| Topic | Notebook |
|-------|----------|
| C_ℓ in pyccl | [CellsCorrelations.ipynb](https://github.com/LSSTDESC/CCLX/blob/master/CellsCorrelations.ipynb) |
| Emulators (Bacco) | [Cosmological_Emulator.ipynb](https://github.com/LSSTDESC/CCLX/blob/master/Cosmological_Emulator.ipynb) |
| Tomographic bins | [LSST_SRD_Redshift_Distributions_and_Binning.ipynb](https://github.com/LSSTDESC/CCLX/blob/master/LSST_SRD_Redshift_Distributions_and_Binning.ipynb) |
| emcee + pyccl | [MCMC Likelihood Analysis.ipynb](https://github.com/LSSTDESC/CCLX/blob/master/MCMC%20Likelihood%20Analysis.ipynb) |

### healpy
[healpy notebook](https://github.com/tanveerkarim/myTutorials/blob/main/notebooks/healpy-sims.ipynb)  
[healpy documentation](https://healpy.readthedocs.io/en/latest/)

## Contact

**Adrita Khan**  
[Email](mailto:adrita.khan.official@gmail.com) | [LinkedIn](https://www.linkedin.com/in/adrita-khan) | [Twitter](https://x.com/Adrita_)


