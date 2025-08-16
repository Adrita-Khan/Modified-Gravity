

* **cosmo\_mcmc\_test\_v5.ipynb**

  * Does not include \$f\_{\rm sky}\$ in the denominator
  * Uses uniform prior
  * Does not sample \$b\_{0}\$
  * Samples \$\Omega\_b\$ (baryon density)

* **cosmo\_mcmc\_test\_v6.ipynb**

  * Includes \$f\_{\rm sky}\$ in the denominator
  * Uses uniform prior
  * Does not sample \$b\_{0}\$
  * Samples \$\Omega\_b\$ (baryon density)



| Notebook                   | \$f\_{\rm sky}\$ in variance/denominator | Prior on \$\boldsymbol{\theta}\$                            | \$b\_{0}\$ (linear bias) sampled? | \$\Omega\_b\$ (baryon density) sampled? |
| -------------------------- | ---------------------------------------- | ----------------------------------------------------------- | --------------------------------- | --------------------------------------- |
| `cosmo_mcmc_test_v5.ipynb` | ❌ No                                     | Uniform \$\big(p(\boldsymbol{\theta})=\mathrm{const}\big)\$ | ❌ No                              | ✅ Yes                                   |
| `cosmo_mcmc_test_v6.ipynb` | ✅ Yes                                    | Uniform \$\big(p(\boldsymbol{\theta})=\mathrm{const}\big)\$ | ❌ No                              | ✅ Yes                                   |

### Why the \$f\_{\rm sky}\$ switch matters

For power-spectrum–based likelihoods, the (Gaussian) variance of \$\hat C\_\ell\$ scales like

$$
\mathrm{Var}\!\left(\hat C_\ell\right)\;\simeq\;\frac{2}{(2\ell+1)\,f_{\rm sky}}\left(C_\ell+N_\ell\right)^{2}.
$$

* Including \$f\_{\rm sky}\$ (as in **v6**) inflates the covariance appropriately for partial-sky analyses.
* Omitting it (as in **v5**) is equivalent to assuming \$f\_{\rm sky}=1\$, which underestimates errors when \$f\_{\rm sky}<1\$.

### Parameters and priors

* \$\Omega\_b\$ (baryon density) is sampled in both notebooks.
* \$b\_{0}\$ (linear galaxy bias) is **not** sampled in either case. Recall:

$$
P_{gg}(k) = b_{0}^{2}\,P_{mm}(k).
$$

### Practical takeaway

* Use **v6** for partial-sky analyses (has the \$1/f\_{\rm sky}\$ factor).
* Fixing \$b\_{0}\$ can tighten posteriors but may bias cosmological parameters (e.g., \$\Omega\_b\$) through degeneracies.
