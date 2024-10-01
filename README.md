# About

This is a tool to test new code for interest model (IRM), basic Semilog with quadratic/cubic/quartic

```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install eth-ape'[recommended-plugins]'
ape plugins install arbitrum
pip install titanoboa
```

# Tools to plot curve for Curve Secondary Monetary Policy

https://github.com/curvefi/curve-stablecoin/blob/master/contracts/mpolicies/SecondaryMonetaryPolicy.vy

1. edit params in secondary-rate-params.py
2. run python secondary-rate-params.py
3. look at plot in data/
