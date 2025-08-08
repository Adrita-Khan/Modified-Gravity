import os
import warnings
import logging
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# Suppress Warnings and Logs
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Set up Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import mgemu and emu
try:
    import mgemu
    from mgemu import emu
except ImportError as e:
    raise ImportError("Failed to import mgemu. Make sure it is installed.") from e

# Parameters
params = {
    "h": 0.67,
    "Omh2": 0.67**2 * 0.281,
    "ns": 0.971,
    "s8": 0.82,
    "n": 1,
    "z": 0.3
}

# Output Directory
output_dir = 'plot'
os.makedirs(output_dir, exist_ok=True)

# Plot
fig, ax1 = plt.subplots(figsize=(9, 6))
fR0_arr = np.logspace(-6, -4, 10)

for fR0 in fR0_arr:
    pkratio, k = emu(
        Omh2=params["Omh2"],
        ns=params["ns"],
        s8=params["s8"],
        fR0=fR0,
        n=params["n"],
        z=params["z"]
    )
    ax1.plot(k, pkratio, label=rf'$f_{{R0}} = {fR0:.0e}$')

ax1.set_xscale('log')
ax1.set_xlabel(r'$k \; [h \,\mathrm{Mpc}^{-1}]$', fontsize=23)
ax1.set_ylabel(r'$P_\mathrm{MG}(k)/P_{\Lambda\mathrm{CDM}}(k)$', fontsize=23)

# Secondary x-axis for physical scale λ = 2π/k
def k_to_lambda(k):
    return 2 * np.pi / k

def lambda_to_k(lmbda):
    return 2 * np.pi / lmbda

secax = ax1.secondary_xaxis('top', functions=(k_to_lambda, lambda_to_k))
secax.set_xscale('log')
secax.set_xlabel(r'$\lambda \; [h^{-1}\,\mathrm{Mpc}]$', fontsize=18)

# Legend and layout
ax1.legend(fontsize=10)
plt.tight_layout()

# Save plot only
output_path = os.path.join(output_dir, 'pkratio_vs_k_with_scale.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
logger.info(f"Plot saved to {output_path}")
