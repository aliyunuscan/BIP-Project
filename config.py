# config.py

# ==========================================
# 1. LOAD PROFILE PARAMETERS
# ==========================================
BASE_LOAD_KW = 1100.0         # Continuous base load
PEAK_LOAD_KW = 2200.0         # Standard peak load
ANNUAL_DEMAND_GWH = 9.7       # Total annual demand for 3,600 inhabitants

# ==========================================
# 2. HYDROLOGICAL & EXTREME PARAMETERS
# ==========================================
MAX_FLOW_MULTIPLIER = 0.95    # Max flow efficiency during spring
MIN_FLOW_MULTIPLIER = 0.25    # Min flow during normal winter/summer drought
EXTREME_DROUGHT_RATIO = 0.05  # Flow drop during extreme freezing events

# ==========================================
# 3. ECONOMIC PARAMETERS (CAPEX - Euro)
# ==========================================
COST_PER_KW_HYDRO = 1250      # Hydro cost per kW
COST_PER_KW_BIOMASS = 1200    # Biomass cost per kW
COST_PER_KWH_BESS = 200       # Battery cost per kWh

# ==========================================
# 4. BATTERY (BMS) PARAMETERS
# ==========================================
SOC_MIN_RATIO = 0.20          # Minimum allowable State of Charge (20%)
CHARGE_EFF = 0.95             # Charging efficiency
DISCHARGE_EFF = 0.95          # Discharging efficiency
BATTERY_C_RATE = 0.5          # Instantaneous discharge capability
CRITICAL_LOAD_RATIO = 0.30    # Tier 1 critical load (Hospital, emergency, pumps)

# ==========================================
# 5. REALISTIC LOAD & EXTREME EVENT PARAMETERS
# ==========================================
# Event 1: Winter Freeze (Drives system sizing)
EVENT_WINTER_FREEZE_START = 500       # Late January
EVENT_WINTER_FREEZE_END = 572         # Lasts 3 days (Flow drops, heating load peaks)

# Event 2: Summer Heatwave
EVENT_SUMMER_HEATWAVE_START = 4500    # Early July
EVENT_SUMMER_HEATWAVE_END = 4668      # Lasts 1 week (HVAC load increases, flow drops)

# Event 3: Vaia-Style Super Storm
EVENT_VAIA_STORM_START = 7000         # October/November
EVENT_VAIA_STORM_END = 7048           # Lasts 2 days (Grid fails, hydro intakes blocked)