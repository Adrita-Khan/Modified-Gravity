# Modified Gravity with Cross-Correlation

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![CAMB](https://img.shields.io/badge/CAMB-Latest-green.svg)](https://camb.info)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/Adrita-Khan/Modified-Gravity)](https://github.com/Adrita-Khan/Modified-Gravity/issues)
[![GitHub stars](https://img.shields.io/github/stars/Adrita-Khan/Modified-Gravity)](https://github.com/Adrita-Khan/Modified-Gravity/stargazers)



Welcome to **Modified Gravity**. This repository contains all necessary components to understand, execute, and contribute to the project, alongside essential resources and outlined development goals.
*This project primarily focuses on forecasting signatures of modified gravity through cross-correlation analyses between the Simons Observatory and the Legacy Survey of Space and Time (LSST) at the Vera C. Rubin Observatory.*
---

## Why Modified Gravity?

The current cosmological framework — ΛCDM (Lambda Cold Dark Matter) — provides an excellent fit to a wide range of observations; however, it is built upon dark energy and dark matter, neither of which has been directly detected to date. As an alternative, modified gravity theories have been proposed to explain cosmic acceleration and the formation of large-scale structures without the invocation of unknown dark components.

These theories often involve modifications to the Poisson equation and alter the relationship between gravitational potentials. Such changes manifest as distinctive signatures within the large-scale structure (LSS) of the Universe. Consequently, MG theories can be constrained through observables such as galaxy clustering and weak lensing.

---

### Theories to be Tested

The project aims to test and constrain the following leading classes of modified gravity theories:

* **f(R) Gravity**: A class of scalar-tensor theories where the Ricci scalar $R$ in the Einstein-Hilbert action is replaced by a function $f(R)$. It predicts scale-dependent growth rates and modified lensing potentials.

* **Horndeski Theories**: The most general scalar-tensor theories with second-order field equations. They encompass many MG models and introduce modifications via kinetic and derivative couplings of a scalar field.
* and more!


---

## Why Cross-Correlation?

Cross-correlation techniques are employed to enhance the testing of gravity models for several key reasons:

- **Degeneracies** between cosmological parameters (e.g., galaxy bias vs. growth rate) can be broken.
- **Systematic errors** are mitigated, as uncorrelated noise and systematics tend to cancel out across different datasets.
- **Signal strength** is amplified by the joint analysis of multiple tracers of the gravitational potential:
  - **Galaxy–Galaxy Clustering**
  - **Galaxy–CMB Lensing Cross-Correlation**
  - **CMB Lensing Auto-Power Spectrum**

These combined observables are particularly sensitive to the growth of structure and the effects of gravitational lensing, rendering them effective tools for probing modified gravity.

---

## Project Description

The aim of this project is to test modified gravity theories by computing and analyzing cross-correlated power spectra:

- Galaxy–Galaxy power spectrum  
- Galaxy–CMB lensing cross-power spectrum  
- CMB Lensing–CMB Lensing auto-power spectrum  

Both theoretical modeling (e.g., using CAMB and emulators) and observational specifications from LSST/DESC and the Simons Observatory are utilized.

---

## Goals

### 🔮 Forecasting Capability

A key objective of this project is to **forecast the constraining power of upcoming cosmological surveys** on modified gravity (MG) theories. By simulating mock observations and comparing theoretical predictions against survey specifications, the framework enables prospective evaluation of how well future data can discriminate between General Relativity and alternative gravity models.

The forecasting pipeline includes the following components:

* **Synthetic Observables**: Theoretical power spectra — including Galaxy–Galaxy, Galaxy–CMB Lensing, and CMB Lensing auto-correlations — are generated under various MG models using tools such as **CAMB**, **MGmu Emulator**, and **parameterized post-Friedmann (PPF)** formalisms.

* **Survey Modeling**: Realistic survey characteristics (e.g., sky coverage, galaxy number density, redshift binning, shape noise) from projects such as **LSST/DESC** and the **Simons Observatory** are incorporated through configuration files. These specifications influence the expected noise levels and window functions in the simulated measurements.

* **Fisher Matrix Analysis**: A Fisher information matrix approach is used to quantify the precision with which cosmological and MG parameters can be constrained. This enables comparison of expected parameter errors across different models and survey strategies.

* **Bias and Degeneracy Evaluation**: By exploring the parameter space of modified gravity (e.g., $f_{R0}$ in f(R), $\alpha_M, \alpha_K, \alpha_B$ in Horndeski), the project can assess degeneracies with standard ΛCDM parameters and evaluate potential biases in inference if MG effects are neglected.

* **Emulator-Based Acceleration**: For faster exploration of the parameter space, the project supports neural-network-based interpolation using the **MGmu Emulator**, allowing rapid generation of spectra across MG parameter grids.

By combining these elements, the pipeline serves as a **forecasting tool for MG detectability**: it determines whether a given MG model would leave statistically significant imprints in the cross-correlation observables of next-generation surveys.


### Literature Review

- [ ] A review of the Power Spectrum and Two-Point Correlation Function (2PCF) under linear theory is to be conducted  
- [ ] Familiarization with [HEALPix](https://healpix.sourceforge.io) and the `healpy` Python package for spherical map handling  
- [ ] A review of key modified gravity theories (e.g., f(R), Horndeski, DGP) is planned  
- [ ] The operation of [CAMB](https://camb.info) is to be studied and implemented  
- [ ] The [MGmu Emulator](https://github.com/LSSTDESC/mgemu) will be explored for rapid computation of matter power spectra  

### Project Sketch

- [ ] Custom functions will be written to calculate:
  - Galaxy–Galaxy power spectrum  
  - Galaxy–CMB lensing cross-power spectrum  
  - CMB Lensing–CMB Lensing auto-power spectrum  
- [ ] The computational pipeline may be optimized using [JAX](https://github.com/google/jax) or neural network-based interpolation  
- [ ] Realistic survey specifications (e.g., number density and redshift distributions from LSST/DESC and Simons Observatory) will be integrated  
- [ ] Theoretical and observational power spectra will be estimated and visualized  
- [ ] Interpretations will be made in the context of selected MG models  

---
### Key Components

| Component | Description | Tools |
|-----------|-------------|-------|
| **Synthetic Observables** | Generate theoretical power spectra | CAMB, MGmu Emulator |
| **Survey Modeling** | Realistic survey specifications | LSST/DESC, Simons Observatory |
| **Fisher Analysis** | Parameter constraint forecasting | Custom Fisher matrix code |
| **Emulator Integration** | Fast parameter space exploration | Neural network interpolation |

---


## 📁 Repository Structure

```bash

├── data/                  # Simulated or observed data inputs
├── notebooks/             # Exploratory Jupyter notebooks
├── src/                   # Core functions for spectra calculation
│   └── cross_power.py     # Functions for GG, GCMB, CMBCMB spectra
├── plots/                 # Output plots and figures
├── configs/               # Survey specs and theory parameters
├── Dockerfile             # Docker environment file (GPU enabled)
├── README.md              # Project documentation
├── requirements.txt       # Dependencies (CAMB, healpy, etc.)

```

## 📚 Resources

- [CAMB Documentation](https://camb.readthedocs.io)
- [MGmu Emulator GitHub](https://github.com/LSSTDESC/mgemu)
- [LSST DESC](https://www.lsst.org/scientists/dark-energy-science-collaboration)
- [Simons Observatory](https://simonsobservatory.org)

---
*This repository serves as a comprehensive resource for understanding, testing, and contributing to the Modified Gravity (MG) project, providing the necessary components, documentation, and resources to execute simulations, analyze data, and forecast the impact of modified gravity theories on cosmological observations. It includes theoretical models, observational data, and tools for computing cross-correlated power spectra, with a focus on testing modified gravity theories like f(R) gravity and Horndeski theories through advanced computational methods and survey simulations.*

