import os
import warnings
import logging
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# =============================
# Suppress Warnings and Logs
# =============================

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# =============================
# Set up Logging
# =============================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================
# Import mgemu and emu
# =============================

try:
    import mgemu
    logger.info("mgemu imported successfully.")
    logger.info(f"Contents of mgemu: {dir(mgemu)}")
except ImportError as e:
    raise ImportError("Failed to import mgemu. Make sure it is installed.") from e

try:
    from mgemu import emu
    logger.info("emu function imported successfully.")
except ImportError as e:
    raise ImportError("Failed to import emu from mgemu.") from e

# =============================
# Define Parameters
# =============================

params = {
    "h": 0.67,
    "Omh2": 0.67**2 * 0.281,
    "ns": 0.971,
    "s8": 0.82,
    "n": 1,
    "z": 0.3
}

# =============================
# Create Output Directory
# =============================

output_dir = 'plot'
os.makedirs(output_dir, exist_ok=True)

# =============================
# Evaluate and Plot
# =============================

plt.figure(figsize=(9, 6))
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
    assert pkratio.shape == k.shape, "Shape mismatch between pkratio and k"
    plt.plot(k, pkratio, label=rf'$f_{{R0}} = {fR0:.0e}$')

plt.xscale('log')
plt.xlabel(r'$k$', fontsize=23)
plt.ylabel(r'$P_\mathrm{MG}(k)/P_{\Lambda\mathrm{CDM}}(k)$', fontsize=23)
plt.legend(fontsize=10)
plt.tight_layout()

# =============================
# Save the Plot
# =============================

output_path = os.path.join(output_dir, 'pkratio_vs_k.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
logger.info(f"Plot saved to {output_path}")

