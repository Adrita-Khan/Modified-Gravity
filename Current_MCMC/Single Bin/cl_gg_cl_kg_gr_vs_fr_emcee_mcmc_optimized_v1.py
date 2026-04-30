import numpy as np
import matplotlib.pyplot as plt
import warnings
import logging
import baccoemu
from emantis.matter_power_spectrum import NonLinearMGBoostEmulator
from scipy.interpolate import interp1d, RectBivariateSpline
from scipy.integrate import simpson, cumulative_trapezoid
import os
from contextlib import redirect_stdout, redirect_stderr
import emcee
import corner
import h5py

warnings.simplefilter("ignore")
logging.getLogger("py.warnings").setLevel(logging.CRITICAL)


class Config:
    COSMO_PARAMS = {
        "Omega_m": 0.315,
        "Omega_b": 0.05,
        "h": 0.67,
        "n_s": 0.96,
        "sigma8": 0.83,
        "M_nu": 0.0,
        "w0": -1.0,
        "wa": 0.0,
        "aexp": 1.0,
    }
    c = 299792.458
    Z_MIN = 0.01
    Z_MAX = 1.5
    N_Z = 500
    N_Z_CHI = 2000
    Z0_GALAXY = 0.3
    ELL_MIN = 10
    ELL_MAX = 2000
    N_ELL = 50
    BIAS_B0 = 2.0
    alpha = 2.225
    FR_VALUES = [4, 5, 6]
    BACCO_K_MIN = -2
    BACCO_K_MAX = None
    BACCO_N_K = 200
    EMANTIS_VERBOSE = False
    FIGURE_SIZE = (14, 10)
    K_MIN_SAFETY = 1.1
    K_MAX_SAFETY = 0.9


def hubble_function(z, H0, Om_m, Om_lambda):
    z = np.asarray(z)
    return H0 * np.sqrt(
        Om_m * (1 + z) ** 3
        + (1 - Om_m - Om_lambda) * (1 + z) ** 2
        + Om_lambda
    )


def build_chi_interpolator(H0, Om_m, Om_lambda, n=None):
    n = n or Config.N_Z_CHI
    z_dense = np.linspace(0.0, Config.Z_MAX * 1.05, n)
    Hz = hubble_function(z_dense, H0, Om_m, Om_lambda)
    chi_dense = np.concatenate(
        [[0.0], cumulative_trapezoid(Config.c / Hz, z_dense)]
    )
    return interp1d(z_dense, chi_dense, kind="cubic",
                    bounds_error=False, fill_value="extrapolate")


def compute_Omega_z(z, H0, Om_m, Om_lambda):
    num = Om_m * (1 + z) ** 3
    den = Om_m * (1 + z) ** 3 + (1 - Om_m - Om_lambda) * (1 + z) ** 2 + Om_lambda
    return num / den


def compute_lambda_z(z, H0, Om_m, Om_lambda):
    num = Om_lambda
    den = Om_m * (1 + z) ** 3 + (1 - Om_m - Om_lambda) * (1 + z) ** 2 + Om_lambda
    return num / den


def growth_function_g(z, H0, Om_m, Om_lambda):
    Omega_z = compute_Omega_z(z, H0, Om_m, Om_lambda)
    lambda_z = compute_lambda_z(z, H0, Om_m, Om_lambda)
    den = Omega_z ** (4 / 7) - lambda_z + (1 + Omega_z / 2) * (1 + lambda_z / 70)
    return (5 * Omega_z / 2) * (1 / den)


def growth_factor_D(z, H0, Om_m, Om_lambda):
    z = np.asarray(z)
    g_z = growth_function_g(z, H0, Om_m, Om_lambda)
    g_0 = growth_function_g(0.0, H0, Om_m, Om_lambda)
    return (g_z / (1.0 + z)) / g_0


def bias_function(z, H0, Omega_m, Omega_lambda, b0=1.0):
    D_z = growth_factor_D(z, H0, Omega_m, Omega_lambda)
    D_0 = growth_factor_D(0.0, H0, Omega_m, Omega_lambda)
    return b0 / (D_z / D_0 + 1e-30)


def cmb_lensing_kernel_vec(z_grid, z_star, H0, Om_m, Om_lambda, chi_of_z):
    Hz = hubble_function(z_grid, H0, Om_m, Om_lambda)
    prefactor = (3 * Om_m * H0 ** 2) / (2 * Config.c * Hz)
    chi_z = chi_of_z(z_grid)
    chi_star = float(chi_of_z(z_star))
    return prefactor * (1 + z_grid) * chi_z * (chi_star - chi_z) / chi_star


def galaxy_lensing_kernel_vec(z_grid, dNdz_arr, bias_arr, H0, Om_m, Om_lambda, chi_of_z):
    chi_z = chi_of_z(z_grid)
    Hz = hubble_function(z_grid, H0, Om_m, Om_lambda)
    alpha_minus1 = Config.alpha - 1.0
    f_A = alpha_minus1 * dNdz_arr
    f_B = alpha_minus1 * dNdz_arr / (chi_z + 1e-30)

    def suffix_trapz(f, z):
        ct = cumulative_trapezoid(f[::-1], z[::-1], initial=0.0)
        return ct[::-1]

    A_suffix = suffix_trapz(f_A, z_grid)
    B_suffix = suffix_trapz(f_B, z_grid)
    mag_integral = A_suffix - chi_z * B_suffix
    mu_prefactor = (3 * Om_m * H0 ** 2) / (2 * Config.c * Hz) * (1 + z_grid) * chi_z
    return bias_arr * dNdz_arr + mu_prefactor * mag_integral


def initialize_bacco_emulator(params, k_min=-2, k_max=None, n_k=200, verbose=False):
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull), redirect_stderr(fnull):
            emulator = baccoemu.Matter_powerspectrum(verbose=verbose)
            if k_max is None:
                k_max = np.log10(emulator.emulator["nonlinear"]["k"].max())
            k = np.logspace(k_min, k_max, num=n_k)
    return emulator, k


def initialize_emantis_emulator(verbose=False):
    return NonLinearMGBoostEmulator(verbose=verbose)


def _bacco_params(params):
    return {
        "omega_cold": params["Omega_m"] - params["Omega_b"],
        "sigma8_cold": params["sigma8"],
        "omega_baryon": params["Omega_b"],
        "ns": params["n_s"],
        "hubble": params["h"],
        "neutrino_mass": params.get("M_nu", 0.0),
        "w0": params.get("w0", -1.0),
        "wa": params.get("wa", 0.0),
    }


def build_pk_spline_gr(emulator, params, k, z_grid):
    bp = _bacco_params(params)
    log_k = np.log(k)
    pk_2d = np.empty((len(k), len(z_grid)))
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull), redirect_stderr(fnull):
            for j, z in enumerate(z_grid):
                _, pk_nl = emulator.get_nonlinear_pk(
                    k=k, cold=False, expfactor=1.0 / (1.0 + z), **bp
                )
                pk_2d[:, j] = pk_nl
    return RectBivariateSpline(log_k, z_grid, np.log(pk_2d + 1e-50), kx=3, ky=3)


def build_pk_spline_fr(emulator, emantis_emu, params, logfR0, k, z_grid):
    bp = _bacco_params(params)
    ep = {
        "Omega_m": params["Omega_m"],
        "Omega_b": params["Omega_b"],
        "h": params["h"],
        "n_s": params["n_s"],
        "sigma8_lcdm": params["sigma8"],
        "logfR0": logfR0,
    }
    log_k = np.log(k)
    pk_2d = np.empty((len(k), len(z_grid)))
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull), redirect_stderr(fnull):
            for j, z in enumerate(z_grid):
                aexp = 1.0 / (1.0 + z)
                _, pk_gr = emulator.get_nonlinear_pk(
                    k=k, cold=False, expfactor=aexp, **bp
                )
                boost = emantis_emu.predict_boost(ep, aexp=aexp, k=k)
                pk_2d[:, j] = pk_gr * boost
    return RectBivariateSpline(log_k, z_grid, np.log(pk_2d + 1e-50), kx=3, ky=3)


def compute_Cl_vec(ell_array, pk_spline, z_grid, Wg_vals, Wkappa_vals,
                   chi_vals, H_vals, h, c_light, k_min=None, k_max=None, cross=False):
    chi_h = chi_vals * h
    k_vals = (ell_array[:, None] + 0.5) / chi_h[None, :]
    if k_min is not None:
        k_vals = np.clip(k_vals, k_min, k_max)
    log_P_flat = pk_spline(
        np.log(k_vals).ravel(), np.tile(z_grid, len(ell_array)), grid=False
    )
    P_kz = np.exp(log_P_flat).reshape(len(ell_array), len(z_grid)) / h ** 3
    W_product = (Wkappa_vals * Wg_vals)[None, :] if cross else Wg_vals[None, :] ** 2
    integrand = (H_vals[None, :] / c_light) * W_product * P_kz / chi_vals[None, :] ** 2
    return simpson(integrand, z_grid, axis=1)


def plot_power_spectra(ell, Cl_gg_gr, Cl_kg_gr, fr_results=None,
                       fR_values=None, figsize=(14, 10)):
    fig = plt.figure(figsize=figsize)

    plt.subplot(2, 2, 1)
    plt.loglog(ell, Cl_gg_gr, "b-", linewidth=2.5, label=r"$C_\ell^{gg}\;[\mathrm{GR}]$")
    if fr_results and fR_values:
        for v in fR_values:
            if v in fr_results["gg"]:
                plt.loglog(ell, fr_results["gg"][v], "--", linewidth=2,
                           label=rf"$f(R):\,\log_{{10}}|f_{{R0}}|-{v}$")
    plt.xlabel(r"$\ell$"); plt.ylabel(r"$C_\ell^{gg}$")
    plt.title(r"Galaxy Auto Spectrum"); plt.legend(fontsize=9); plt.grid(ls="--", alpha=0.7)

    plt.subplot(2, 2, 2)
    plt.loglog(ell, np.abs(Cl_kg_gr), "b-", linewidth=2.5, label=r"$C_\ell^{\kappa g}\;[\mathrm{GR}]$")
    if fr_results and fR_values:
        for v in fR_values:
            if v in fr_results["kg"]:
                plt.loglog(ell, np.abs(fr_results["kg"][v]), "--", linewidth=2,
                           label=rf"$f(R):\,\log_{{10}}|f_{{R0}}|-{v}$")
    plt.xlabel(r"$\ell$"); plt.ylabel(r"$|C_\ell^{\kappa g}|$")
    plt.title(r"CMB Lensing × Galaxy"); plt.legend(fontsize=9); plt.grid(ls="--", alpha=0.7)

    plt.subplot(2, 2, 3)
    if fr_results and fR_values:
        for v in fR_values:
            if v in fr_results["gg"]:
                plt.semilogx(ell, fr_results["gg"][v] / Cl_gg_gr, "--", linewidth=2,
                             label=rf"$\log|f_{{R0}}|-{v}$")
        plt.axhline(1.0, color="k", lw=1.5, alpha=0.5)
    plt.xlabel(r"$\ell$"); plt.ylabel(r"Ratio"); plt.title(r"Galaxy Auto Ratio")
    plt.legend(fontsize=9); plt.grid(ls="--", alpha=0.7); plt.ylim([0.95, 1.45])

    plt.subplot(2, 2, 4)
    if fr_results and fR_values:
        for v in fR_values:
            if v in fr_results["kg"]:
                plt.semilogx(ell, fr_results["kg"][v] / Cl_kg_gr, "--", linewidth=2,
                             label=rf"$\log|f_{{R0}}|-{v}$")
        plt.axhline(1.0, color="k", lw=1.5, alpha=0.5)
    plt.xlabel(r"$\ell$"); plt.ylabel(r"Ratio"); plt.title(r"CMB Cross Ratio")
    plt.legend(fontsize=9); plt.grid(ls="--", alpha=0.7); plt.ylim([0.95, 1.45])

    plt.tight_layout()
    return fig


_ROUND = 5
_geo_cache = {}
_pk_cache = {}
_GEO_MAXSIZE = 128
_PK_MAXSIZE = 128


def _evict(cache, maxsize):
    if len(cache) >= maxsize:
        del cache[next(iter(cache))]


def get_geometry(Omega_m, b0, z_grid_local, z_star):
    key = (round(float(Omega_m), _ROUND), round(float(b0), _ROUND))
    if key in _geo_cache:
        return _geo_cache[key]
    H0_loc = Config.COSMO_PARAMS["h"] * 100.0
    Om_m_loc = float(Omega_m)
    Om_lam_loc = 1.0 - Om_m_loc
    chi_of_z_loc = build_chi_interpolator(H0_loc, Om_m_loc, Om_lam_loc)
    chi_loc = chi_of_z_loc(z_grid_local)
    H_loc = hubble_function(z_grid_local, H0_loc, Om_m_loc, Om_lam_loc)
    raw_nz = (2.0 * Config.Z0_GALAXY) * (z_grid_local / Config.Z0_GALAXY) ** 2 \
             * np.exp(-z_grid_local / Config.Z0_GALAXY)
    dNdz_loc = raw_nz / simpson(raw_nz, z_grid_local)
    Wkap_loc = cmb_lensing_kernel_vec(z_grid_local, z_star, H0_loc, Om_m_loc, Om_lam_loc, chi_of_z_loc)
    bias_loc = bias_function(z_grid_local, H0_loc, Om_m_loc, Om_lam_loc, b0=float(b0))
    Wg_loc = galaxy_lensing_kernel_vec(z_grid_local, dNdz_loc, bias_loc, H0_loc, Om_m_loc, Om_lam_loc, chi_of_z_loc)
    result = dict(H0=H0_loc, Om_m=Om_m_loc, Om_lam=Om_lam_loc,
                  chi=chi_loc, H=H_loc, Wkappa=Wkap_loc, Wg=Wg_loc)
    _evict(_geo_cache, _GEO_MAXSIZE)
    _geo_cache[key] = result
    return result


def get_pk_spline(Omega_m, sigma8, logfR0, z_grid_local, bacco_emu, emantis_emu, k):
    key = (round(float(Omega_m), _ROUND), round(float(sigma8), _ROUND), round(float(logfR0), _ROUND))
    if key in _pk_cache:
        return _pk_cache[key]
    params = Config.COSMO_PARAMS.copy()
    params["Omega_m"] = float(Omega_m)
    params["sigma8"] = float(sigma8)
    spline = build_pk_spline_fr(bacco_emu, emantis_emu, params, abs(float(logfR0)), k, z_grid_local)
    _evict(_pk_cache, _PK_MAXSIZE)
    _pk_cache[key] = spline
    return spline


def model_cls_fast(theta, ell_local, z_grid_local, z_star, bacco_emu, emantis_emu, k, k_min_safe, k_max_safe):
    Omega_m, sigma8, b0, logfR0 = theta
    geo = get_geometry(Omega_m, b0, z_grid_local, z_star)
    spline = get_pk_spline(Omega_m, sigma8, logfR0, z_grid_local, bacco_emu, emantis_emu, k)
    shared_kw = dict(
        z_grid=z_grid_local,
        Wg_vals=geo["Wg"], Wkappa_vals=geo["Wkappa"],
        chi_vals=geo["chi"], H_vals=geo["H"],
        h=Config.COSMO_PARAMS["h"], c_light=Config.c,
        k_min=k_min_safe, k_max=k_max_safe,
    )
    Cl_gg = compute_Cl_vec(ell_local, spline, cross=False, **shared_kw)
    Cl_kg = compute_Cl_vec(ell_local, spline, cross=True, **shared_kw)
    return Cl_gg, Cl_kg


def flatten_cls(Cl_gg, Cl_kg):
    return np.concatenate([Cl_gg, Cl_kg])


def main():
    PLOT_OUTPUT_DIR = "mcmc_plots"
    os.makedirs(PLOT_OUTPUT_DIR, exist_ok=True)

    H0 = Config.COSMO_PARAMS["h"] * 100.0
    Om_m = Config.COSMO_PARAMS["Omega_m"]
    Om_lambda = 1.0 - Om_m
    z_star = 1100.0

    bacco_emu, k = initialize_bacco_emulator(
        Config.COSMO_PARAMS,
        k_min=Config.BACCO_K_MIN,
        k_max=Config.BACCO_K_MAX,
        n_k=Config.BACCO_N_K,
        verbose=Config.EMANTIS_VERBOSE,
    )
    emantis_emu = initialize_emantis_emulator(verbose=Config.EMANTIS_VERBOSE)
    k_min_safe = k.min() * Config.K_MIN_SAFETY
    k_max_safe = k.max() * Config.K_MAX_SAFETY

    z_grid = np.linspace(Config.Z_MIN, Config.Z_MAX, Config.N_Z)
    chi_of_z = build_chi_interpolator(H0, Om_m, Om_lambda)
    chi_vals = chi_of_z(z_grid)
    H_vals = hubble_function(z_grid, H0, Om_m, Om_lambda)

    _raw_nz = (2.0 * Config.Z0_GALAXY) * (z_grid / Config.Z0_GALAXY) ** 2 \
              * np.exp(-z_grid / Config.Z0_GALAXY)
    dNdz = _raw_nz / simpson(_raw_nz, z_grid)

    Wkappa_vals = cmb_lensing_kernel_vec(z_grid, z_star, H0, Om_m, Om_lambda, chi_of_z)
    bias_arr = bias_function(z_grid, H0, Om_m, Om_lambda, b0=Config.BIAS_B0)
    Wg_vals = galaxy_lensing_kernel_vec(z_grid, dNdz, bias_arr, H0, Om_m, Om_lambda, chi_of_z)

    pk_spline_gr = build_pk_spline_gr(bacco_emu, Config.COSMO_PARAMS, k, z_grid)

    ell = np.logspace(np.log10(Config.ELL_MIN), np.log10(Config.ELL_MAX), Config.N_ELL)
    shared = dict(
        z_grid=z_grid, Wg_vals=Wg_vals, Wkappa_vals=Wkappa_vals,
        chi_vals=chi_vals, H_vals=H_vals, h=Config.COSMO_PARAMS["h"],
        c_light=Config.c, k_min=k_min_safe, k_max=k_max_safe,
    )
    Cl_gg_gr = compute_Cl_vec(ell, pk_spline_gr, cross=False, **shared)
    Cl_kg_gr = compute_Cl_vec(ell, pk_spline_gr, cross=True, **shared)

    fr_results = {"gg": {}, "kg": {}}
    for logfR0_val in Config.FR_VALUES:
        pk_spline_fr = build_pk_spline_fr(bacco_emu, emantis_emu, Config.COSMO_PARAMS, logfR0_val, k, z_grid)
        fr_results["gg"][logfR0_val] = compute_Cl_vec(ell, pk_spline_fr, cross=False, **shared)
        fr_results["kg"][logfR0_val] = compute_Cl_vec(ell, pk_spline_fr, cross=True, **shared)

    fig = plot_power_spectra(ell, Cl_gg_gr, Cl_kg_gr,
                             fr_results=fr_results, fR_values=Config.FR_VALUES,
                             figsize=Config.FIGURE_SIZE)
    fig.savefig(os.path.join(PLOT_OUTPUT_DIR, "power_spectra_gr_vs_fr.png"), dpi=300, bbox_inches="tight")
    plt.show()

    PARAM_NAMES = [r"$\Omega_m$", r"$\sigma_8$", r"$b_0$", r"$\log_{10}|f_{R0}|$"]
    FIDUCIAL_THETA = np.array([Config.COSMO_PARAMS["Omega_m"], Config.COSMO_PARAMS["sigma8"], Config.BIAS_B0, -5.0])
    PRIORS = {"Omega_m": (0.20, 0.45), "sigma8": (0.60, 1.00), "b0": (0.50, 4.00), "logfR0": (-6.00, -4.00)}

    N_Z_MCMC = 80
    N_ELL_MCMC = 20
    ELL_MIN_MCMC = Config.ELL_MIN
    ELL_MAX_MCMC = 1200
    STAT_FRAC_ERR_GG = 0.05
    STAT_FRAC_ERR_KG = 0.08
    N_WALKERS = 32
    N_STEPS = 800
    BURN_IN = 200
    THIN = 5
    HDF5_CHAIN_FILE = "emcee_clgg_clkg_chain.h5"
    HDF5_BACKEND_NAME = "mcmc"
    RESET_HDF5_BACKEND = True
    CHECK_AUTOCORR_EVERY = 100

    np.random.seed(42)

    ell_mcmc = np.logspace(np.log10(ELL_MIN_MCMC), np.log10(ELL_MAX_MCMC), N_ELL_MCMC)
    z_grid_mcmc = np.linspace(Config.Z_MIN, Config.Z_MAX, N_Z_MCMC)

    Cl_gg_fid, Cl_kg_fid = model_cls_fast(
        FIDUCIAL_THETA, ell_mcmc, z_grid_mcmc, z_star, bacco_emu, emantis_emu, k, k_min_safe, k_max_safe
    )
    data_vector = flatten_cls(Cl_gg_fid, Cl_kg_fid)
    sigma_gg = STAT_FRAC_ERR_GG * np.abs(Cl_gg_fid)
    sigma_kg = STAT_FRAC_ERR_KG * np.maximum(np.abs(Cl_kg_fid), 1e-30)
    sigma_vector = flatten_cls(sigma_gg, sigma_kg)

    fig = plt.figure(figsize=(8, 5))
    plt.errorbar(ell_mcmc, Cl_gg_fid, yerr=sigma_gg, fmt="o", label=r"Mock $C_\ell^{gg}$")
    plt.errorbar(ell_mcmc, np.abs(Cl_kg_fid), yerr=sigma_kg, fmt="s", label=r"Mock $|C_\ell^{\kappa g}|$")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel(r"Multipole $\ell$"); plt.ylabel(r"Angular power spectrum")
    plt.legend(); plt.tight_layout()
    fig.savefig(os.path.join(PLOT_OUTPUT_DIR, "mock_data_vector.png"), dpi=300, bbox_inches="tight")
    plt.show()

    def log_prior(theta):
        Omega_m, sigma8, b0, logfR0 = theta
        if not (PRIORS["Omega_m"][0] < Omega_m < PRIORS["Omega_m"][1]): return -np.inf
        if not (PRIORS["sigma8"][0] < sigma8 < PRIORS["sigma8"][1]): return -np.inf
        if not (PRIORS["b0"][0] < b0 < PRIORS["b0"][1]): return -np.inf
        if not (PRIORS["logfR0"][0] < logfR0 < PRIORS["logfR0"][1]): return -np.inf
        return 0.0

    def log_likelihood(theta):
        try:
            Cl_gg, Cl_kg = model_cls_fast(
                theta, ell_mcmc, z_grid_mcmc, z_star, bacco_emu, emantis_emu, k, k_min_safe, k_max_safe
            )
            model_vector = flatten_cls(Cl_gg, Cl_kg)
            if not np.all(np.isfinite(model_vector)):
                return -np.inf
            residual = (data_vector - model_vector) / sigma_vector
            return -0.5 * np.sum(residual ** 2)
        except Exception:
            return -np.inf

    def log_probability(theta):
        lp = log_prior(theta)
        if not np.isfinite(lp):
            return -np.inf
        ll = log_likelihood(theta)
        return lp + ll if np.isfinite(ll) else -np.inf

    ndim = len(FIDUCIAL_THETA)
    initial_spread = np.array([0.01, 0.02, 0.05, 0.08])
    initial_positions = FIDUCIAL_THETA + initial_spread * np.random.randn(N_WALKERS, ndim)
    prior_bounds = [PRIORS["Omega_m"], PRIORS["sigma8"], PRIORS["b0"], PRIORS["logfR0"]]
    for i in range(N_WALKERS):
        for d, (lo, hi) in enumerate(prior_bounds):
            initial_positions[i, d] = np.clip(initial_positions[i, d], lo + 1e-3, hi - 1e-3)

    backend = emcee.backends.HDFBackend(HDF5_CHAIN_FILE, name=HDF5_BACKEND_NAME)
    if RESET_HDF5_BACKEND:
        backend.reset(N_WALKERS, ndim)
        start_state = initial_positions
        print(f"Starting new chain → {HDF5_CHAIN_FILE}")
    else:
        start_state = None
        print(f"Resuming chain from {HDF5_CHAIN_FILE} ({backend.iteration} steps)")

    sampler = emcee.EnsembleSampler(N_WALKERS, ndim, log_probability, backend=backend)
    autocorr_history = []
    old_tau = np.inf

    for sample in sampler.sample(start_state, iterations=N_STEPS, progress=True):
        if sampler.iteration % CHECK_AUTOCORR_EVERY != 0:
            continue
        try:
            tau = sampler.get_autocorr_time(tol=0)
            autocorr_history.append([sampler.iteration, *tau])
            print(f"Step {sampler.iteration}: mean τ = {np.mean(tau):.2f}")
            converged = np.all(tau * 100 < sampler.iteration)
            converged &= np.all(np.abs(old_tau - tau) / tau < 0.01)
            if converged:
                print("Converged — stopping early.")
                break
            old_tau = tau
        except Exception as err:
            print(f"Step {sampler.iteration}: τ not reliable yet ({err})")

    print(f"Mean acceptance fraction: {np.mean(sampler.acceptance_fraction):.3f}")
    print(f"Saved chain: {os.path.abspath(HDF5_CHAIN_FILE)}")

    reader = emcee.backends.HDFBackend(HDF5_CHAIN_FILE, name=HDF5_BACKEND_NAME, read_only=True)
    chain = reader.get_chain()
    log_prob_chain = reader.get_log_prob()

    fig, axes = plt.subplots(ndim + 1, 1, figsize=(10, 2.2 * (ndim + 1)), sharex=True)
    for i in range(ndim):
        axes[i].plot(chain[:, :, i], alpha=0.35)
        axes[i].axhline(FIDUCIAL_THETA[i], linestyle="--", linewidth=1)
        axes[i].set_ylabel(PARAM_NAMES[i])
    axes[-1].plot(log_prob_chain, alpha=0.35)
    axes[-1].set_ylabel(r"$\log p$"); axes[-1].set_xlabel("Step")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOT_OUTPUT_DIR, "chain_diagnostics.png"), dpi=300, bbox_inches="tight")
    plt.show()

    try:
        tau = reader.get_autocorr_time(tol=0)
        for name, tau_i in zip(PARAM_NAMES, tau):
            print(f"{name}: τ = {tau_i:.2f} steps")
    except Exception as err:
        print("τ not reliable yet:", err)

    if autocorr_history:
        ac = np.array(autocorr_history)
        fig = plt.figure(figsize=(7, 4))
        plt.plot(ac[:, 0], np.mean(ac[:, 1:], axis=1), label=r"Mean $\hat{\tau}$")
        plt.plot(ac[:, 0], ac[:, 0] / 100.0, "--", label="N/100")
        plt.xlabel("Steps"); plt.ylabel(r"Mean $\hat{\tau}$")
        plt.legend(); plt.tight_layout()
        fig.savefig(os.path.join(PLOT_OUTPUT_DIR, "autocorrelation_time_monitor.png"), dpi=300, bbox_inches="tight")
        plt.show()

    reader = emcee.backends.HDFBackend(HDF5_CHAIN_FILE, name=HDF5_BACKEND_NAME, read_only=True)
    try:
        tau = reader.get_autocorr_time()
        burn_in = int(2 * np.max(tau))
        thin = max(1, int(0.5 * np.min(tau)))
    except Exception:
        burn_in, thin = BURN_IN, THIN

    flat_samples = reader.get_chain(discard=burn_in, thin=thin, flat=True)
    flat_log_prob = reader.get_log_prob(discard=burn_in, thin=thin, flat=True)

    print(f"burn-in={burn_in}, thin={thin}, N_samples={len(flat_samples)}")
    for i, name in enumerate(PARAM_NAMES):
        q16, q50, q84 = np.percentile(flat_samples[:, i], [16, 50, 84])
        print(f"{name} = {q50:.5f} -{q50 - q16:.5f} +{q84 - q50:.5f}")

    fig = corner.corner(
        flat_samples,
        labels=PARAM_NAMES,
        truths=FIDUCIAL_THETA,
        show_titles=True,
        title_fmt=".4f",
        quantiles=[0.16, 0.50, 0.84],
        title_kwargs={"fontsize": 11},
        label_kwargs={"fontsize": 12},
    )
    fig.savefig(os.path.join(PLOT_OUTPUT_DIR, "corner_plot.png"), dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
