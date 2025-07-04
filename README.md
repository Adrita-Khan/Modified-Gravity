# Modified Gravity with Cross-Correlation

Welcome to **Modified Gravity**. This repository contains all necessary components to understand, execute, and contribute to the project, alongside essential resources and outlined development goals.

---

## Why Modified Gravity?

The current cosmological framework — ΛCDM (Lambda Cold Dark Matter) — provides an excellent fit to a wide range of observations; however, it is built upon dark energy and dark matter, neither of which has been directly detected to date. As an alternative, modified gravity theories have been proposed to explain cosmic acceleration and the formation of large-scale structures without the invocation of unknown dark components.

These theories often involve modifications to the Poisson equation and alter the relationship between gravitational potentials. Such changes manifest as distinctive signatures within the large-scale structure (LSS) of the Universe. Consequently, MG theories can be constrained through observables such as galaxy clustering and weak lensing.

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


