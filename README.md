# MM1K_queueing_model
## Context
This project was made for the Performance Evaluation course of TÉLÉCOM Nancy (2nd Year).

## How to run
`queue_model.py` can be runned using python as long the libraries `numpy` and `matplotlib.pyplot` are installed.

You can then use```python3 queue_model.py```.

`compute_stats.py` needs the libraries `mpi4py` and `scipy.stats` to be installed and a working MPI implementation, preferably supporting MPI-3 and built with shared/dynamic libraries. (https://mpi4py.readthedocs.io/en/stable/install.html)

You can then use ```mpirun -np 10 python3 compute_stats.py``` to run with 10 processes.

## How to use
### Simulations
`queue_model.py` simulates a M/M/1/K queue.


The number of requests received per time unit, the number of requests treated per time unit, the observation time and the buffer size can be modified. The buffer size can be left unspecified to have an unlimited buffer.


You can run the simulation with the function `queue_model.run_simulation`.
You can print statistics on the simulation with the function `queue_model.print_statistics`.
You can plot the evolution of arrived and treated requests over time with the function `queue_model.plot_simulation`.

### Computing statistics using MPI
`compute_stats.py` can be used to get precise statistics on several simulations quickly using parallelization.

<img src="https://github.com/BigBaz54/MM1K_queueing_model/assets/96493391/bfe272ca-1006-4f32-9c57-d7840d0219bc.png" width="1000" height="550">

Confidence intervals are computed either using normal approximation or using the t-student distribution depending on the number of samples.
