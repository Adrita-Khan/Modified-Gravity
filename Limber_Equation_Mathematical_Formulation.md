# Limber's Equation - Complete Mathematical Formulation in LaTeX

## Basic Statistical Quantities

### Number density and fluctuations
```latex
\delta(\mathbf{x}) = \frac{n(\mathbf{x}) - \bar{n}}{\bar{n}}
```

### Probability and correlation functions
```latex
P[\delta_1, \delta_2] = \frac{N}{V} = \bar{n}
```

```latex
P[\delta_1, \delta_2] = \frac{N(N-1)}{V^2} = \bar{n}^2[1 + \xi(r_{12})]
```

```latex
P[\delta_1, \delta_2] = \frac{N(N-1)}{V_1 V_2} = \bar{n}^2[1 + \xi(r_{12})]
```

```latex
p(\mathbf{r}) = \frac{4\pi}{3} \int_0^\infty r^3 n(r) \xi(\mathbf{r}) \, dV
```

## Spatial and Angular Correlation Functions

### Spatial correlation function for two fields
```latex
\langle \delta_1(\mathbf{r}_1) \delta_2(\mathbf{r}_2) \rangle = \xi_{12}(|\mathbf{r}_2 - \mathbf{r}_1|)
```

### Angular correlation function
```latex
\omega_{12}(\theta) = \langle \delta_1(\hat{\mathbf{n}}) \delta_2(\hat{\mathbf{n}} + \boldsymbol{\theta}) \rangle
```

### Filter/weight functions
```latex
p_i(r) \quad \text{(filter or weight function)}
```

### Look-back time and scale factor
```latex
t(r) \quad \text{(look-back time)}
```
```latex
a(r) \quad \text{(scale factor)}
```

## Projected Density and Exact Relations

### Projected density contrast
```latex
\delta_i(\hat{\mathbf{n}}) = \frac{\int_0^{\infty} p_i(r) \delta_i(r\hat{\mathbf{n}}) \, dr}{\int_0^{\infty} p_i(r) \, dr}
```

### Exact relation between spatial and angular correlation
```latex
\omega_{12}(\theta) = \frac{\int_0^{\infty} dr_1 \int_0^{\infty} dr_2 \, p_1(r_1) p_2(r_2) \xi_{12}[\mathbf{r}(r_1, r_2, \theta), t(r_1), t(r_2)]}{\int_0^{\infty} p_1(r) \, dr \int_0^{\infty} p_2(r) \, dr}
```

where:
```latex
|\mathbf{r}(r_1, r_2, \theta)| = \sqrt{r_1^2 + r_2^2 - 2r_1 r_2 \cos \theta}
```

## Limber's Approximation

### New coordinates
```latex
\bar{r} = \frac{r_1 + r_2}{2} \quad \text{(mean radial distance)}
```
```latex
s = r_2 - r_1 \quad \text{(difference of radial distances)}
```

### Limber's equation (relativistic form)
```latex
\omega_{12}(\theta) = \int_0^{\infty} d\bar{r} \, \frac{p_1(\bar{r}) p_2(\bar{r})}{\bar{r}^2} \int_{-\infty}^{\infty} ds \, \xi_{12}(\sqrt{s^2 + \bar{r}^2 \theta^2}, \bar{r})
```

### Small angle approximation
For small angles $\theta \ll 1$:
```latex
\theta \rightarrow \sin \theta \quad \text{and} \quad \theta \rightarrow \tan \theta
```

### Final Limber approximation
```latex
\omega_{12}(\theta) = \int_0^{\infty} d\bar{r} \, \frac{p_1(\bar{r}) p_2(\bar{r})}{\bar{r}^2} \xi_{12}(\bar{r}\theta, \bar{r})
```

## Weak Lensing Applications

### Convergence field
```latex
\kappa(\boldsymbol{\theta}) = \frac{3\Omega_m H_0^2}{2c^2} \int_0^{\chi_H} d\chi \, g(\chi) a^{-1}(\chi) \delta[\chi \boldsymbol{\theta}, \chi]
```

### Lensing efficiency
```latex
g(\chi) = \int_\chi^{\chi_H} d\chi' \, n(\chi') \frac{D_A(\chi, \chi')}{D_A(\chi')}
```

### Power spectrum relation (Limber's equation for convergence)
```latex
C_\kappa(\ell) = \frac{9\Omega_m^2 H_0^4}{4c^4} \int_0^{\chi_H} d\chi \, \frac{g^2(\chi)}{a^2(\chi)} P_\delta\left(\frac{\ell}{\chi}, \chi\right)
```

### Geodesic deviation equation
```latex
\frac{d^2 \xi^i}{d\lambda^2} + 2\Gamma^\mu_{\nu 0} \frac{dx^\nu}{d\lambda} \frac{d\xi^i}{d\lambda} + \frac{\partial \Gamma^i_{\mu 0}}{\partial x^\nu} \frac{dx^\mu}{d\lambda} \xi^\nu = 0
```

### Born approximation
```latex
\boldsymbol{\alpha}(\boldsymbol{\theta}) = \frac{2}{c^2} \int_0^{\chi_s} d\chi \, \frac{D_A(\chi_s - \chi)}{D_A(\chi_s) D_A(\chi)} \nabla_\perp \Phi[\boldsymbol{\theta} D_A(\chi), \chi]
```

## Accuracy Estimates

### Filter width estimate
For weak lensing with source galaxies at $z_s = 1$:
```latex
\frac{\Delta \chi}{\bar{\chi}} \approx 0.5
```

### Center of filter
```latex
\bar{\chi}/\chi_H \approx 0.5
```

### Accuracy range
Limber's equation is accurate to about 10% for separations:
```latex
\theta < \text{several degrees}
```

## Power Spectrum Relation

### Fourier transform relationship
```latex
P(k) = \int d^3\mathbf{r} \, \xi(\mathbf{r}) e^{i\mathbf{k} \cdot \mathbf{r}}
```

### Limber's equation in Fourier space
```latex
C(\ell) = \int_0^{\infty} d\chi \, \frac{W^2(\chi)}{\chi^2} P\left(\frac{\ell}{\chi}, \chi\right)
```

where $W(\chi)$ is the weight function and $P(k,\chi)$ is the 3D power spectrum.
