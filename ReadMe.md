# Markowitz-Modell
## Markowitz-Problem
Das Porgramm löst folgendene Minimierungsprobleme
```math
\text{minimize}_{x\in\mathbb{R}^J}\;\text{var}\;x^\top\xi\;\\
\text{subject to}\;\mathbb{E}\,x^\top\xi\geq\mu,\;x^\top\mathbf{1}=1
```
```math
\text{maximize}_{x\in\mathbb{R}^J}\;\text{E}\,x^\top\xi-\frac{\kappa}{2}\text{var}\;x^\top\xi\; \\
\text{subject to}\;x^\top\mathbf{1}=1
```
```math
\text{minimize}_{x\in\mathbb{R}^J}\mathbb{E}\,x^\top\xi+\mathcal{R}(-x^\top\xi)\; \\
\text{subject to}\;\mathbb{E}\,x^\top\xi\geq\mu,\;x^\top\mathbf{1}=1\; \\
\text{with}\;\mathcal{R}(X) = (1-\gamma)\mathbb{E}X+\gamma\text{AVaR}_\alpha(X)
```
## Notwendige Bibliotheken
```bash
py -m pip install numpy
```
```bash
py -m pip install pandas
```
```bash
py -m pip install pandas_datareader
```
```bash
py -m pip install matplotlib
```

## Verwendung