
- **cosmo_mcmc_test_v5.ipynb**  
  - Does not include *fsky* in the denominator  
  - Uses uniform prior  
  - Does not sample *bnot*  
  - Samples *omegab* (baryon density)  

- **cosmo_mcmc_test_v6.ipynb**  
  - Includes *fsky* in the denominator  
  - Uses uniform prior  
  - Does not sample *bnot*  
  - Samples *omegab* (baryon density)  






| Notebook                | fsky in denominator | Prior   | bnot sampled | omegab sampled |
|--------------------------|---------------------|---------|--------------|----------------|
| cosmo_mcmc_test_v5.ipynb | ❌ No               | Uniform | ❌ No        | ✅ Yes         |
| cosmo_mcmc_test_v6.ipynb | ✅ Yes              | Uniform | ❌ No        | ✅ Yes         |



| Notebook | $\(f_{\rm sky}\)$ in variance/denominator | Prior on \(\boldsymbol{\theta}\) | \(b_0\) (linear bias) sampled? | \(\Omega_b\) (baryon density) sampled? |
|---|---|---|---|---|
| `cosmo_mcmc_test_v5.ipynb` | ❌ No | Uniform (\(p(\boldsymbol{\theta})=\mathrm{const}\)) | ❌ No | ✅ Yes |
| `cosmo_mcmc_test_v6.ipynb` | ✅ Yes | Uniform (\(p(\boldsymbol{\theta})=\mathrm{const}\)) | ❌ No | ✅ Yes |

### Why the \(f_{\rm sky}\) switch matters
For power-spectrum–based likelihoods, the (Gaussian) variance of \(\hat C_\ell\) scales like  
\[
\mathrm{Var}(\hat C_\ell)\;\simeq\;\frac{2}{(2\ell+1)\,f_{\rm sky}}\left(C_\ell+N_\ell\right)^2.
\]
- Including \(f_{\rm sky}\) (as in **v6**) correctly inflates the covariance for partial-sky analyses.  
- Omitting it (as in **v5**) is equivalent to assuming \(f_{\rm sky}=1\), which underestimates parameter errors when \(f_{\rm sky}<1\).

### Parameters and priors
- **\(\Omega_b\)** (baryon density) is sampled in both notebooks.  
- **\(b_0\)** (linear galaxy bias) is **not** sampled in either case. Recall:  
  \[
  P_{gg}(k) = b_0^2 \, P_{mm}(k)
  \]
  so fixing \(b_0\) can artificially tighten posteriors but risks bias if the chosen value is off.

### Practical takeaway
- Use **v6** for partial-sky analyses: it includes the \(1/f_{\rm sky}\) factor and yields realistic uncertainties.  
- Be mindful that fixing \(b_0\) can propagate into cosmological parameters like \(\Omega_b\) due to degeneracies in \(P(k)\) or \(C_\ell\).
