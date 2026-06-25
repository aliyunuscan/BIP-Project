# 🏔️ Pieve di Cadore: Hybrid Microgrid Optimization & EMS Simulation

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Optimization](https://img.shields.io/badge/Solver-PuLP-success.svg)](#)

A mathematical optimization and Energy Management System (EMS) simulation framework designed for the mountainous community of Pieve di Cadore in the Italian Dolomites. This project models a **100% renewable, dispatchable microgrid** (Run-of-River Hydro + Biomass CHP + BESS) to ensure the survival of Tier 1 critical infrastructure during extreme alpine weather events (e.g., Vaia-style super storms and extended winter freezes).

---

## 🧠 Core Algorithms & Engineering Logic

This repository does not rely on simple rule-based energy shifting. Instead, it utilizes an advanced dual-layer algorithmic architecture:

### 1. MILP System Sizing (TOTEX Minimization)
Located in `optimizer.py`, the system uses Mixed-Integer Linear Programming (MILP) to find the absolute minimum hardware capacity required to survive extreme weather, minimizing the 20-Year Total Expenditure (TOTEX).
* **Spinning Reserve Sizing:** The Battery Energy Storage System (BESS) is intentionally restricted. It is sized *only* to sustain the 30% Tier 1 critical load (792 kW) for exactly **1 hour**—the exact time required for the Biomass CHP plant to synchronize with the grid during a sudden hydro failure. 

### 2. Proactive Load Shedding (Emergency Survival)
Located in `ems_core.py`, the EMS continuously monitors the physical river flow potential. 
* If the river flow drops below the extreme drought threshold (10%), the EMS **does not wait for the battery to die**. 
* It immediately executes a controlled blackout of non-essential zones, dropping the total grid load strictly to a **30% Critical Ratio** (Hospital, emergency shelters, water pumps).

### 3. Aggressive Charging Protocol
Instead of slowly charging the BESS with excess energy, the EMS enforces strict grid-readiness:
* The moment the battery discharges during a deficit, the 1.69 MW Biomass plant is dispatched.
* It does not just meet the community load; it runs at **maximum capacity** to force the BESS back to 100% State of Charge (SoC) as aggressively as possible, ensuring the community is mathematically prepared for the next sudden blackout.

---

## 📂 Repository Structure

* `config.py` — Centralized parameters (Load profiles, Extreme event windows, Economic CapEx data, Battery C-rates).
* `data_handler.py` — Generates the 8,760-hour annual profile, injecting Gaussian noise into demand and simulating physical river flow collapses during extreme weather.
* `optimizer.py` — The PuLP-based MILP engine that dictates the exact physical sizing of the generators.
* `ems_core.py` — The hour-by-hour simulation engine that executes Load Shedding and Aggressive Charging.
* `visualizer.py` — Generates high-resolution (300 dpi) plots for stress testing.
* `metrics.py` — Calculates and exports Loss of Power Supply Probability (LPSP), unmet load, and system efficiency.
* `main.py` — The entry point of the pipeline.

---

## 🚀 How to Run the Simulation

**1. Clone the repository:**

```bash
git clone https://github.com/aliyunuscan/Pieve-Microgrid-Optimization
```

**2. Install dependencies:**
It is recommended to use a virtual environment.

```bash
pip install pandas numpy matplotlib pulp
```
**3. Execute the pipeline:**

```bash
python main.py
```
**4. View Results:**
   
Upon execution, the terminal will display the MILP optimization results, TOTEX costs, and performance metrics. The simulation will automatically generate high-resolution operational graphs and save them directly to the /results directory:

- results/annual_overview.png
- results/weekly_stress_test.png

## 📊 Evaluation & Resilience

Under the 72-hour simulated Winter Freeze stress test (where river flow collapses to 5% and heating demand surges by 20%), the Proactive Shedding protocol guarantees a 0% Loss of Power Supply Probability (LPSP) for Tier 1 critical loads, validating the mathematical robustness of the minimized hardware capacities.
