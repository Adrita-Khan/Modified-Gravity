Based on the implementation of the `mgemu` Modified Gravity emulator for the Hu–Sawicki $f(R)$ model, the **prior ranges** are implicitly constrained by the emulator’s **defined parameter validity bounds**.

The table below presents a structured summary of the **priors** applied to each model parameter:

| Parameter                | Symbol         | Description                       | Range                              | Value Used in This Study            |
| ------------------------ | -------------- | --------------------------------- | ---------------------------------- | ----------------------------------- |
| Matter density           | $\Omega_m h^2$ | Physical matter density           | $0.12 \leq \Omega_m h^2 \leq 0.15$ | $0.67^2 \times 0.281 \approx 0.126$ |
| Spectral index           | $n_s$          | Scalar spectral index             | $0.85 \leq n_s \leq 1.1$           | 0.971                               |
| Power spectrum amplitude | $\sigma_8$     | Linear fluctuation amplitude      | $0.7 \leq \sigma_8 \leq 0.9$       | 0.82                                |
| $f(R)$ strength          | $f_{R0}$       | Background field value at $z = 0$ | $10^{-8} \leq f_{R0} \leq 10^{-4}$ | $10^{-5}$                           |
| $f(R)$ power             | $n$            | Power index in Hu–Sawicki model   | $0 \leq n \leq 4$                  | 1                                   |
| Redshift                 | $z$            | Redshift of output                | $0 \leq z \leq 50$                 | 0.3                                 |

---

### Key Notes:

- These parameter limits serve as **hard-coded priors** within the emulator framework. Supplying input values outside these bounds may trigger extrapolation, which is discouraged by the original authors.
- The emulator provides the **enhancement ratio** $P_{\rm MG}(k)/P_{\Lambda \rm CDM}(k)$ across 213 $k$-bins spanning the range $k \in [0, 3.5]\,h/{\rm Mpc}$.
- It is recommended that results be considered **reliable only up to $k \sim 1.0\,h/{\rm Mpc}$**, beyond which the emulator's predictions may lack accuracy.

