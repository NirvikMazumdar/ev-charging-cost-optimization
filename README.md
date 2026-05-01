# EV Charging Cost Optimization System

## Overview
This project models and optimizes electric vehicle (EV) charging behavior using real electricity market price data.

It simulates charging sessions and evaluates multiple strategies to minimize cost while ensuring required battery levels (state of charge) are achieved.

---

## Problem
Electricity prices fluctuate significantly over time, making naive charging strategies inefficient and costly.

Key constraints:
- Charging must meet required energy demand (SOC target)
- Power is limited by infrastructure (e.g., 11 kW chargers)
- Time windows for charging are finite

---

## Solution
The system combines simulation and optimization to determine cost-efficient charging behavior.

It:
- Simulates realistic charging sessions with varying durations and SOC levels
- Applies multiple predefined charging strategies
- Implements a dynamic cost-minimizing optimization approach
- Enhances results using Fourier-based smoothing and price-aware adjustments

---

## Features

### Charging Strategies
- Max Power
- Ramp Up / Ramp Down
- Delayed Charging
- Uniform Charging

### Optimization
- Dynamic cost-based decision making
- Constraint-aware scheduling (energy + time limits)
- Fourier-based power profile refinement

### Simulation
- Randomized charging sessions
- Variable SOC requirements
- Strategy benchmarking across thousands of events

---

## Outputs

The system generates:

- Average cost per strategy
- Cost distribution comparisons
- SOC success rates
- Summary results in CSV format

Outputs are saved in:

outputs/figures/  
outputs/results/

---

## Project Structure
