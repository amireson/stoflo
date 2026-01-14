# stoflo

**stoflo** (stocks and flows) is a Python-based system dynamics model. It is designed for
modelling systems of ordinary differential equations (ODEs), or equivalently, changes in
the state of a set of stocks as a function of flows between them.

The model comprises five basic elements:

1. Time grid information;
2. Definition of stocks and their initial states;
3. Definition of flows and their connections into or out of each stock, using custom-built functions;
4. Definition of drivers — exogenous time series data that flow into or out of stocks;
5. Definition of model parameters in a dictionary.

From these basic building blocks, anything from a simple reservoir to a complex, interacting
system can be modelled. The current implementation uses explicit Euler integration with
sub-stepping controlled by the parameter `niter` (the number of calculation timesteps between
reporting timesteps).

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/amireson/stoflo.git

