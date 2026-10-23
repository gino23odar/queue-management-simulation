# Evaluation of Scheduling Algorithms for Queue Management

This project investigates the effects of different scheduling
algorithms on waiting times and service efficiency using a
Python-based discrete-event simulation.

## Scheduling Algorithms

Three non-preemptive scheduling strategies are evaluated:

- First Come, First Served (FCFS)
- Shortest Processing Time (SPT)
- Priority-based scheduling

## Requirements

- Python 3.12 or newer
- pip

## Installation

Create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Run the Demo

```powershell
.\.venv\Scripts\python.exe -m queue_sim.demo
```

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Run Experiments

Quick experimental run:

```powershell
.\.venv\Scripts\python.exe -m queue_sim.experiments --repetitions 5
```

Full experimental run:

```powershell
.\.venv\Scripts\python.exe -m queue_sim.experiments --repetitions 30
```

## Statistical Comparison

```powershell
.\.venv\Scripts\python.exe -m queue_sim.comparison
```

## Generate Plots

```powershell
.\.venv\Scripts\python.exe -m queue_sim.plots --servers 2
```

## Experimental Parameters

Customer loads:
- 100
- 300
- 500

Number of servers:
- 1
- 2
- 4

Repetitions:
- 30 per configuration

Scheduling strategies:
- FCFS
- SPT
- Priority

## Simulation Assumptions

The simulation uses synthetic customer data.

Arrival times follow a uniform distribution across an
eight-hour arrival window.

Service times follow a triangular distribution with:
- Minimum: 2 minutes
- Maximum: 8 minutes
- Mode: 4 minutes

20% of customers are classified as high priority.

Service is non-preemptive.

All customers eventually receive service, including
those whose service extends beyond operating hours.

## Evaluation Metrics

- Mean waiting time
- Maximum waiting time
- 95th-percentile waiting time
- Customers completed before closing
- Server utilization
- Mean waiting time by priority group
- Waiting-time differences between priority groups

## Experiment Results

Individual simulations:

results/experiments.csv

Aggregated results:

results/summary.csv

Paired statistical comparisons:

results/comparison.csv

Generated charts:

results/figures/

## Project Limitations

The simulation uses synthetic workloads rather than
measured real-world customer data.

Service durations are assumed to be known before
scheduling.

Customer abandonment is not modeled.

Employees do not take breaks or experience
unexpected interruptions.

Results are specific to the selected simulation
assumptions and should not be interpreted as
validated predictions for a real service center.