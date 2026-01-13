# Comprehensive Formula List for CMB-Galaxy Cross-Correlation in Modified Gravity

## 1. Modified Gravity Theory Formulas

### 1.1 f(R) Gravity

**Action:**
$$S = \frac{1}{16\pi G}\int d^4x\sqrt{-g}\,f(R) + S_m$$

**Parameterization (Hu-Sawicki model):**
$$f(R) = R - \frac{c_1(R/m^2)^n}{1 + c_2(R/m^2)^n}$$

**Present-day parameter:**
$$f_{R0} = \frac{df}{dR}\bigg|_{z=0}$$

**Modified Poisson equation:**
$$\nabla^2\Phi = \frac{16\pi G}{3}a^2\bar{\rho}\Delta - \frac{1}{3}\nabla^2\delta f_R$$

**Effective gravitational constant:**
$$G_{\text{eff}} = G\left(1 + \frac{4}{3}\frac{k^2}{k^2 + a^2m_{f_R}^2}\right)$$

where $m_{f_R}$ is the scalaron mass.

**Modified growth factor:**
$$\mu(a,k) = \frac{G_{\text{eff}}(a,k)}{G}$$

### 1.2 DGP Gravity

**Modified Friedmann equation:**
$$H^2 = \frac{8\pi G}{3}\rho + \frac{\epsilon}{r_c^2}\left(H - \epsilon\sqrt{H^2 + \frac{1}{r_c^2}}\right)$$

where $\epsilon = +1$ (normal branch) or $-1$ (self-accelerating branch), and $r_c$ is the crossover scale.

**Effective Newton's constant:**
$$G_{\text{eff}} = G\left(1 + \frac{1}{3\beta(a)}\right)$$

**DGP parameter:**
$$\beta(a) = 1 - 2H(a)r_c\left(1 + \frac{\dot{H}(a)}{3H(a)^2}\right)$$

**Growth index:**
$$f(a) = \Omega_m(a)^\gamma$$

where $\gamma \approx 0.68$ for ΛCDM and $\gamma \approx 0.55-0.58$ for DGP.

**Modified Poisson equation:**
$$k^2\Psi = -4\pi Ga^2\bar{\rho}\Delta\left(1 + \frac{1}{3\beta}\right)$$

## 2. Gravitational Potentials and Slip

**Metric perturbations (Newtonian gauge):**
$$ds^2 = -(1+2\Psi)dt^2 + a^2(1-2\Phi)d\mathbf{x}^2$$

**Gravitational slip parameter:**
$$\eta(a,k) = \frac{\Phi}{\Psi}$$

For GR: $\eta = 1$; for MG: $\eta \neq 1$

**Modified Poisson equations:**
$$k^2\Psi = -4\pi Ga^2\bar{\rho}\Delta\,\mu(a,k)$$
$$k^2\Phi = -4\pi Ga^2\bar{\rho}\Delta\,\mu(a,k)\,\eta(a,k)$$

## 3. Structure Growth

**Linear growth equation:**
$$\ddot{\delta} + 2H\dot{\delta} - 4\pi G\bar{\rho}\mu(a,k)\delta = 0$$

**Growth rate:**
$$f(a) = \frac{d\ln\delta}{d\ln a}$$

**Growth factor normalization:**
$$D(a) = \frac{\delta(a)}{\delta(a_i)}$$

**Velocity divergence:**
$$\theta = -\frac{k^2}{aH}f(a)\delta$$

## 4. Matter Power Spectrum

**Linear matter power spectrum:**
$$P_{\delta\delta}(k,z) = D^2(z)P_{\text{prim}}(k)T^2(k)$$

where $T(k)$ is the transfer function.

**Primordial power spectrum:**
$$P_{\text{prim}}(k) = A_s\left(\frac{k}{k_*}\right)^{n_s-1}$$

**Modified power spectrum:**
$$P^{\text{MG}}_{\delta\delta}(k,z) = \left[\frac{D^{\text{MG}}(z)}{D^{\text{GR}}(z)}\right]^2 P^{\text{GR}}_{\delta\delta}(k,z)$$

**Non-linear correction (phenomenological):**
$$P_{\text{nl}}(k,z) = P_{\text{lin}}(k,z)\exp\left[-k^2\sigma^2_v(z)\right]$$

## 5. Galaxy Clustering

**Galaxy overdensity:**
$$\delta_g(\mathbf{x},z) = b(z)\delta_m(\mathbf{x},z)$$

where $b(z)$ is the linear bias parameter.

**Galaxy power spectrum:**
$$P_{gg}(k,z) = b^2(z)P_{\delta\delta}(k,z)$$

**Redshift-space distortions:**
$$P_{gg}^s(k,\mu,z) = \left[b + f\mu^2\right]^2P_{\delta\delta}(k,z)$$

where $\mu = \cos\theta$ and $\theta$ is the angle to the line of sight.

## 6. Angular Power Spectra

### 6.1 Galaxy-Galaxy Angular Power Spectrum

**2D angular power spectrum:**
$$C_\ell^{gg}(z_i,z_j) = \int_0^\infty \frac{dk}{k}P_{gg}(k,\bar{z})\,W_\ell^g(k,z_i)W_\ell^g(k,z_j)$$

**Window function (Limber approximation):**
$$W_\ell^g(k,z) = b(z)q_i(z)\frac{H(z)}{c}\frac{1}{\chi^2(z)}$$

where $q_i(z)$ is the normalized redshift distribution:
$$q_i(z) = \frac{dN/dz_i}{\int dN/dz_i\,dz_i}$$

**Full Limber formula:**
$$C_\ell^{gg}(i,j) = \int_0^{\chi_H} d\chi\frac{W_i^g(\chi)W_j^g(\chi)}{\chi^2}P_{\delta\delta}\left(k=\frac{\ell+1/2}{\chi},z(\chi)\right)$$

### 6.2 CMB Lensing Convergence Power Spectrum

**CMB lensing convergence:**
$$\kappa(\hat{n}) = \int_0^{\chi_{CMB}}d\chi\,W^\kappa(\chi)\delta(\chi\hat{n},\chi)$$

**Lensing kernel:**
$$W^\kappa(\chi) = \frac{3H_0^2\Omega_m}{2c^2}\frac{\chi}{a(\chi)}\frac{\chi_{CMB}-\chi}{\chi_{CMB}}$$

**Auto power spectrum:**
$$C_\ell^{\kappa\kappa} = \int_0^{\chi_{CMB}}\frac{d\chi}{\chi^2}[W^\kappa(\chi)]^2P_{\delta\delta}\left(\frac{\ell+1/2}{\chi},z(\chi)\right)$$

### 6.3 Galaxy-CMB Lensing Cross-Power Spectrum

**Cross-correlation:**
$$C_\ell^{\kappa g}(i) = \int_0^{\chi_{CMB}}d\chi\frac{W^\kappa(\chi)W_i^g(\chi)}{\chi^2}P_{\delta\delta}\left(\frac{\ell+1/2}{\chi},z(\chi)\right)$$

**Alternative form:**
$$C_\ell^{\kappa g} = \int_0^\infty \frac{dk}{k}P_{\delta\delta}(k,z)W_\ell^\kappa(k)W_\ell^g(k)$$

## 7. Redshift Distribution Functions

**Galaxy redshift distribution (photo-z):**
$$n(z) = \frac{z^2}{\Gamma(3/\alpha)}\left(\frac{z}{z_0}\right)^{\alpha}\exp\left[-\left(\frac{z}{z_0}\right)^\alpha\right]\frac{1}{z_0}$$

**Smail distribution:**
$$n(z) \propto z^\alpha\exp\left[-\left(\frac{z}{z_0}\right)^\beta\right]$$

**Tomographic binning:**
$$n_i(z) = \int_{z_i^{\min}}^{z_i^{\max}}dz\,p(z|z_p)n(z_p)$$

## 8. Survey Specifications

**Galaxy number density:**
$$\bar{n}_i = \int_{z_i^{\min}}^{z_i^{\max}}dz\,n(z)$$

**Shot noise:**
$$N_\ell^{gg} = \frac{1}{\bar{n}_i}$$

**CMB lensing noise:**
$$N_\ell^{\kappa\kappa} = \frac{L^2C_\ell^{TT}}{(\ell-L)^2C_{\ell-L}^{TT} + L^2C_L^{TT}}$$

(Simplified form; exact form depends on reconstruction method)

**Total power spectrum (with noise):**
$$\tilde{C}_\ell^{gg} = C_\ell^{gg} + N_\ell^{gg}$$
$$\tilde{C}_\ell^{\kappa\kappa} = C_\ell^{\kappa\kappa} + N_\ell^{\kappa\kappa}$$

## 9. Fisher Matrix Formalism

**Fisher matrix:**
$$F_{ij} = \sum_{\ell=\ell_{\min}}^{\ell_{\max}}f_{\text{sky}}\frac{2\ell+1}{2}\text{Tr}\left[\mathbf{C}_\ell^{-1}\frac{\partial\mathbf{C}_\ell}{\partial\theta_i}\mathbf{C}_\ell^{-1}\frac{\partial\mathbf{C}_\ell}{\partial\theta_j}\right]$$

**Covariance matrix (for GG, κG, κκ):**
$$\mathbf{C}_\ell = \begin{pmatrix}
\tilde{C}_\ell^{gg} & C_\ell^{\kappa g} \\
C_\ell^{\kappa g} & \tilde{C}_\ell^{\kappa\kappa}
\end{pmatrix}$$

**For multi-bin analysis:**
$$\mathbf{C}_\ell = \begin{pmatrix}
\tilde{C}_\ell^{g_ig_j} & C_\ell^{\kappa g_i} \\
C_\ell^{\kappa g_j} & \tilde{C}_\ell^{\kappa\kappa}
\end{pmatrix}$$

**Parameter uncertainties:**
$$\sigma(\theta_i) = \sqrt{[\mathbf{F}^{-1}]_{ii}}$$

**Marginalized constraints:**
$$\sigma(\theta_i|\text{marg}) = \sqrt{[\mathbf{F}^{-1}]_{ii}}$$

**Figure of Merit:**
$$\text{FoM} = \frac{1}{\sqrt{\det(\mathbf{C}_{sub})}}$$

where $\mathbf{C}_{sub}$ is the covariance of parameters of interest.

## 10. PPF (Parametrized Post-Friedmann) Formalism

**Modified growth:**
$$\mu(a,k) = \frac{\Psi}{(\Psi_{\text{GR}})}$$
$$\gamma(a,k) = \frac{\Phi}{\Psi}$$

**Phenomenological parameterization:**
$$\mu(a,k) = 1 + \mu_0\frac{\Omega_{\text{DE}}(a)}{1+k^2/k^2_*}$$
$$\eta(a,k) = 1 + \eta_0\frac{\Omega_{\text{DE}}(a)}{1+k^2/k^2_*}$$

## 11. Cosmological Distance Relations

**Comoving distance:**
$$\chi(z) = \int_0^z \frac{c\,dz'}{H(z')}$$

**Hubble parameter:**
$$H(z) = H_0\sqrt{\Omega_m(1+z)^3 + \Omega_k(1+z)^2 + \Omega_\Lambda}$$

**Modified Hubble (DGP):**
$$H(z) = H_0\sqrt{\Omega_m(1+z)^3 + \Omega_{rc}[1+\sqrt{1+(1+z)^3\Omega_m/\Omega_{rc}^2}]}$$

**Angular diameter distance:**
$$d_A(z) = \frac{\chi(z)}{1+z}$$

## 12. Numerical Implementation

**Discrete Limber sum:**
$$C_\ell^{XY} = \sum_i \Delta\chi_i\frac{W^X(\chi_i)W^Y(\chi_i)}{\chi_i^2}P_{\delta\delta}\left(\frac{\ell+1/2}{\chi_i},z_i\right)$$

**Logarithmic k-integration:**
$$C_\ell = \int d\ln k\,P(k,z)W_\ell(k)$$

**Band power estimation:**
$$C_b = \frac{1}{\Delta\ell}\sum_{\ell\in b}C_\ell$$
