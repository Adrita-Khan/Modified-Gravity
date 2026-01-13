# Maximum Multipole Moment Selection in Cosmology

The choice of maximum multipole moment ($\ell_{\max}$) in cosmological analyses represents a crucial decision that balances scientific goals with practical constraints. This selection involves multiple interconnected factors related to experimental capabilities, theoretical understanding, and computational limitations.

## Angular Resolution and Beam Size Relationship

The primary constraint on $\ell_{\max}$ stems from the **angular resolution** of the observational instrument. The fundamental relationship follows from the beam characteristics of the telescope or detector system.[1][2][3]

For a Gaussian beam with full-width-at-half-maximum (FWHM) denoted as $\theta_{\text{FWHM}}$, there is an approximate correspondence between angular scale and multipole moment:

$$\ell \sim \frac{180°}{\theta_{\text{FWHM}}}$$

More precisely, the beam suppresses power at high multipoles according to a **beam window function** $B_\ell$, which for a Gaussian beam takes the form:[2]

$$B_\ell = \exp\left(-\frac{\ell(\ell+1)\sigma_{\text{beam}}^2}{2}\right)$$

where $\sigma_{\text{beam}} = \theta_{\text{FWHM}}/(2\sqrt{2\ln 2})$ is related to the beam size. The practical limit for reliable multipole analysis occurs when $B_\ell$ becomes significantly small, typically around $\ell_{\max} \sim 2-3 \times 180°/\theta_{\text{FWHM}}$.[4][2]

## Pixelization and Sampling Constraints

The choice of $\ell_{\max}$ is fundamentally limited by the **pixelization scheme** used for sky maps. For the widely-used HEALPix pixelization scheme, there are specific relationships that must be respected.[5][6][7][8]

### HEALPix Resolution Parameters

For a HEALPix map with resolution parameter $N_{\text{side}}$:
- Total number of pixels: $N_{\text{pix}} = 12N_{\text{side}}^2$
- Default maximum multipole: $\ell_{\max}^{\text{default}} = 3N_{\text{side}} - 1$
- Theoretical upper limit: $\ell_{\max}^{\text{theory}} = 2N_{\text{side}}$

The theoretical limit $\ell_{\max} = 2N_{\text{side}}$ arises from **Nyquist sampling** considerations. Beyond this limit, spherical harmonic transforms become unreliable due to insufficient spatial sampling.[6][8]

### Pixel Window Function

The pixelization process introduces a **pixel window function** $P_\ell$ that modulates the power spectrum. This function approximately follows:[8][4]

$$P_\ell^{\text{sinc}} = \text{sinc}\left(\frac{\ell\theta_r}{2\pi}\right)$$

where $\theta_r$ is the pixel resolution scale. For HEALPix, the window function becomes significant when $\ell \gtrsim 2N_{\text{side}}$, providing another constraint on reliable $\ell_{\max}$ values.[8]

## Experimental and Survey-Specific Considerations

### Planck Mission Example

The **Planck satellite** provides an excellent case study for $\ell_{\max}$ selection. Different analysis contexts within Planck use varying maximum multipoles:[9]

- **Low-$\ell$ analysis**: $\ell < 30$ (commander-based likelihood)
- **High-$\ell$ temperature**: $\ell_{\max} = 2508$ (temperature power spectrum)
- **High-$\ell$ polarization**: $\ell_{\max} = 1996$ (polarization analysis)
- **Lensing reconstruction**: $\ell_{\max} \sim 3000$ (gravitational lensing potential)

The specific choice depends on signal-to-noise ratio, systematic error control, and the physics being probed.[9]

### Ground-Based Experiments

Modern ground-based CMB experiments typically choose $\ell_{\max}$ based on several factors:[10][1]

- **Angular resolution**: Higher resolution allows higher $\ell_{\max}$
- **Sky coverage**: Smaller sky patches may require different multipole ranges
- **Systematic control**: Non-Gaussian covariances become important at high-$\ell$

For example, weak lensing studies often use $\ell_{\max} = 1000, 3000,$ or even $20000$ depending on the required precision and systematic error tolerance.[1]

## Physical Scale Considerations

The choice of $\ell_{\max}$ also relates to the **physical scales** being probed. Each multipole moment corresponds roughly to an angular scale:[11]

$$\theta \sim \frac{180°}{\ell + 1/2}$$

Higher multipole moments probe smaller angular scales, which correspond to smaller physical scales at the last scattering surface. The practical considerations include:

- **Linear vs. nonlinear regimes**: Very high $\ell$ probes nonlinear structure formation
- **Baryonic physics**: Small-scale effects become important at $\ell \gtrsim 3000$
- **Instrumental systematics**: Higher $\ell$ modes are more susceptible to systematic errors

## Computational and Statistical Factors

### Matrix Operations and Computational Cost

The computational cost of likelihood evaluation scales approximately as $\mathcal{O}(\ell_{\max}^3)$ for full covariance matrix operations. This strongly motivates careful selection of $\ell_{\max}$ to balance scientific return with computational feasibility.[12][13]

### Covariance Matrix Rank

The **rank** of covariance matrices provides mathematical constraints on viable $\ell_{\max}$ values. For $N$ pixels and spherical harmonics up to $\ell_{\max}$, the matrix rank is constrained by:[12]

$$\text{rank}(C) \leq \min\left(N, \ell_{\max}^2 - \ell_{\min}^2 + 2\ell_{\max} + 1\right)$$

This constraint becomes particularly relevant for masked or partial sky analyses.[12]

## Standard Formulas and Relationships

### Beam-Limited $\ell_{\max}$

For a Gaussian beam with FWHM $\theta_b$ (in arcminutes), a commonly used formula is:

$$\ell_{\max} \approx \frac{10800}{\theta_b}$$

where the factor accounts for the point where beam suppression becomes severe.[2][4]

### HEALPix Sampling Formula

For HEALPix maps, the safe multipole range is:

$$\ell_{\max}^{\text{safe}} = 2N_{\text{side}}$$

with the default choice being $\ell_{\max}^{\text{default}} = 3N_{\text{side}} - 1$, though this requires careful numerical handling of spherical harmonic transforms.[6][8]

### Signal-to-Noise Considerations

The effective $\ell_{\max}$ for scientific analysis is often determined by where the signal-to-noise ratio becomes unity:

$$\left(\frac{S}{N}\right)_\ell = 1$$

This depends on the specific power spectrum being measured, instrumental noise characteristics, and beam suppression.[14][15]

## Practical Implementation Guidelines

### Multi-Scale Analysis Strategy

Modern CMB analyses often employ **multiple $\ell_{\max}$ values** for different purposes:[10][1]

1. **Conservative choice** ($\ell_{\max} \sim 1000$): Well-understood linear regime
2. **Intermediate choice** ($\ell_{\max} \sim 3000$): Balance of signal and systematic control  
3. **Aggressive choice** ($\ell_{\max} \sim 5000-20000$): Maximum information extraction

### Validation and Testing

The chosen $\ell_{\max}$ should be validated through:
- **Simulation studies**: Testing reconstruction fidelity at the chosen limit
- **Systematic error analysis**: Ensuring biases remain below statistical uncertainties
- **Convergence tests**: Verifying that results are stable against modest changes in $\ell_{\max}$

The selection of maximum multipole moment in cosmological analyses represents a sophisticated optimization problem that must balance theoretical understanding, experimental capabilities, and computational resources. The specific choice depends critically on the scientific objectives, instrumental characteristics, and acceptable systematic error levels for each analysis.

[1] https://arxiv.org/pdf/1204.2229.pdf  
[2] https://academic.oup.com/mnras/article-pdf/394/3/1419/18484910/mnras0394-1419.pdf  
[3] https://www.aanda.org/articles/aa/full_html/2010/02/aa13117-09/aa13117-09.html  
[4] https://arxiv.org/html/2410.12951v2  
[5] https://ziotom78.github.io/Healpix.jl/stable/resolutions/  
[6] https://www.zubairkhalid.org/papers/C33.pdf  
[7] https://stackoverflow.com/questions/30812976/healpy-healpix-what-is-the-relationship-between-the-total-pixels-and-total-sphe  
[8] https://arxiv.org/pdf/2410.12951.pdf  
[9] https://www.aanda.org/articles/aa/pdf/2020/09/aa36386-19.pdf  
[10] https://arxiv.org/pdf/1509.05374.pdf  
[11] https://en.wikipedia.org/wiki/Cosmic_microwave_background  
[12] https://arxiv.org/pdf/1701.06617.pdf  
[13] https://academic.oup.com/mnras/article-pdf/375/2/625/4247543/mnras0375-0625.pdf  
[14] https://link.aps.org/doi/10.1103/PhysRevD.99.023502  
[15] https://link.aps.org/doi/10.1103/PhysRevD.109.043527  
[16] https://www.numberanalytics.com/blog/power-of-multipole-moments-cmb  
[17] https://www.aanda.org/articles/aa/pdf/2011/02/aa15906-10.pdf  
[18] https://arxiv.org/html/2506.22795v1  
[19] https://stackoverflow.com/questions/65844496/healpy-getting-spherical-harmonics-from-as-function-of-pixel-l-and-m  
[20] https://link.aps.org/doi/10.1103/PhysRevD.107.083515  
[21] https://scholarworks.boisestate.edu/cgi/viewcontent.cgi?article=1254&context=math_facpubs  
[22] https://lambda.gsfc.nasa.gov/product/wmap/dr4/pub_papers/sevenyear/cosmology/wmap_7yr_cosmology.pdf  
[23] https://arxiv.org/abs/astro-ph/0006392  
[24] https://phys.libretexts.org/Courses/University_of_California_Davis/Physics_156:_A_Cosmology_Workbook/01:_Workbook/1.27:_Cosmic_Microwave_Background_Anisotropies  
[25] https://arxiv.org/html/2502.20282v1  
[26] https://pmc.ncbi.nlm.nih.gov/articles/PMC10905750/  
[27] https://www.reddit.com/r/GraphicsProgramming/comments/m19ith/explain_to_me_like_i_am_5_using_spherical/  
[28] https://www.aanda.org/articles/aa/pdf/2023/07/aa44619-22.pdf  
[29] https://arxiv.org/pdf/2506.22795.pdf  
[30] https://digital.csic.es/bitstream/10261/349456/1/cmbanisotro.pdf  
[31] https://www.aanda.org/articles/aa/full_html/2025/02/aa52588-24/aa52588-24.html  
[32] https://arxiv.org/pdf/astro-ph/0410394.pdf  
[33] https://academic.oup.com/mnras/article/539/1/542/8088428  
[34] https://irsa.ipac.caltech.edu/data/Planck/release_1/docs/DR1_Explanatory_Supplement.pdf  
[35] https://healpix.jpl.nasa.gov/pdf/facilities.pdf  
