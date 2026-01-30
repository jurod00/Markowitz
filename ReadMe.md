# Markowitz-Modell
## Markowitz-Problem
Das Porgramm löst folgendene Minimierungsprobleme
```math
\operatorname{minimize}_{x\in\R^J}\operatorname{var}x^T\xi \\
\text{subject to}\;\mathbb{E}\,x^T\xi\geq\mu\;
```
```math
\operatorname{minimize}_{x\in\R^J}\mathbb{E}\,x^T\xi+\mathcal{R}(-x^T\xi) \\
\text{subject to}\;\mathbb{E}\,x^T\xi\geq\mu\text{ with}\hspace*{26pt} \\
\mathcal{R}(X) = (1-\gamma)\mathbb{E}X+\gamma\operatorname{AVaR}_\alpha(X)
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