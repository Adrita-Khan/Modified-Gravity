# 🌀 Modified Gravity with Cross-Correlation

Welcome to **Modified Gravity** — a project focused on testing and constraining modified gravity (MG) theories using cross-correlations between galaxy surveys and CMB lensing measurements. This repository includes everything you need to understand, run, and contribute to the project, along with key resources and development goals.

---

## ✨ Why Modified Gravity?

The current cosmological model — ΛCDM (Lambda Cold Dark Matter) — fits a wide range of data remarkably well, but it relies on dark energy and dark matter, which have not yet been directly detected. Modified gravity theories aim to explain cosmic acceleration and structure formation without invoking unknown dark components.

These theories often alter the Poisson equation and the relationship between the gravitational potentials, leading to distinctive signatures in the large-scale structure (LSS) of the Universe. As a result, MG theories can be tested through cosmological observables such as galaxy clustering and weak lensing.

---

## 🔀 Why Cross-Correlation?

Cross-correlation enhances our ability to test gravity models by:

- **Breaking degeneracies** between cosmological parameters (e.g., galaxy bias vs. growth rate).
- **Minimizing systematics** — uncorrelated noise and systematics tend to cancel in cross-correlations.
- **Enhancing signal** by combining information from multiple tracers of the gravitational potential:
  - **Galaxy-Galaxy Clustering**
  - **Galaxy–CMB Lensing Cross-Correlation**
  - **CMB Lensing Auto-Power Spectrum**

These observables are sensitive to the growth of structure and gravitational lensing, making them powerful tools for probing MG theories.

---

## 📝 Project Description

This project aims to test modified gravity theories by computing and interpreting cross-correlated power spectra:

- Galaxy-Galaxy power spectrum
- Galaxy–CMB lensing cross-power spectrum
- CMB Lensing–CMB Lensing auto-power spectrum

We use both theoretical modeling (CAMB, emulators) and observational specifications from LSST/DESC and Simons Observatory.

---

## 🎯 Goals

### 🔍 Literature Review

- [ ] Understand Power Spectrum / Two-Point Correlation Function (2PCF) under linear theory
- [ ] Familiarize with [HEALPix](https://healpix.sourceforge.io) / `healpy` for map handling
- [ ] Review key theories of Modified Gravity (e.g., f(R), Horndeski, DGP)
- [ ] Learn how to run [CAMB](https://camb.info)
- [ ] Explore [MGmu Emulator](https://github.com/ntessore/mg-mu-sigma) for fast matter power spectra

### 🧠 Project Sketch

- [ ] Write functions to calculate:
  - Galaxy–Galaxy power spectrum
  - Galaxy–CMB lensing cross-spectrum
  - CMB Lensing–Lensing auto-power spectrum
- [ ] Optimize pipeline with [JAX](https://github.com/google/jax) or NN interpolation
- [ ] Integrate realistic survey specs (e.g., LSST/DESC, Simons Obs: number density, redshift distributions)
- [ ] Estimate and plot theoretical and observational power spectra
- [ ] Interpret results in the context of MG theories

---

## 📁 Repository Structure

```bash
modified-gravity-crosscorr/
├── data/                # Simulated or observed data inputs
├── notebooks/           # Exploratory Jupyter notebooks
├── src/                 # Core functions for spectra calculation
│   └── cross_power.py   # Functions for GG, GCMB, CMBCMB spectra
├── plots/               # Output plots and figures
├── configs/             # Survey specs and theory parameters
├── README.md            # This file
├── requirements.txt     # Dependencies (CAMB, healpy, etc.)
└── environment.yml      # Conda environment

```

## 📚 Resources

- [CAMB Documentation](https://camb.readthedocs.io)
- [MGmu Emulator GitHub](https://github.com/ntessore/mg-mu-sigma)
- [LSST DESC](https://www.lsst.org/scientists/dark-energy-science-collaboration)
- [Simons Observatory](https://simonsobservatory.org)


