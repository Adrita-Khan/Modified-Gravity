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

### LCDM parameters
h=0.67
Omh2=(h**2)*0.281
ns=0.971
s8=0.82
### Hu-Sawicki model parameters
fr0=1e-5
n=1
### Redshift
z=0.3


pkratio, k = emu(Omh2=Omh2, ns=ns, s8=s8, fR0=fr0, n=n, z=z)

plt.figure(1, figsize=(9, 6))
fR0_arr= np.logspace(-6, -4, 10)
for i in range(10):
    fR0 = fR0_arr[i]
    pkratio, k = emu(Omh2=Omh2, ns=ns, s8=s8, fR0=fR0, n=n, z=z)
    plt.plot(k, pkratio)
plt.xscale('log')
plt.ylabel(r'$P_{MG}(k)/P_{LCDM}(k)$', fontsize=23)
plt.xlabel(r'$k$', fontsize=23)

# Create the 'plot' directory if it doesn't exist
output_dir = 'plot'
os.makedirs(output_dir, exist_ok=True)

# Save the figure in the 'plot' directory
output_path = os.path.join(output_dir, 'pkratio_plot.png')
plt.savefig(output_path)

logger.info(f"Plot saved to {output_path}")
plt.close()
