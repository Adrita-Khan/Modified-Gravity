
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
