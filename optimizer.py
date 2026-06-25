# optimizer.py
import pulp
import config

def get_optimal_capacities():
    print("\n--- RUNNING MILP OPTIMIZATION: REAL ENGINEERING (TOTEX & SPINNING RESERVE) ---")
    model = pulp.LpProblem("Pieve_di_Cadore_True_Optimization", pulp.LpMinimize)

    # 20-Year Lifecycle Costs (TOTEX)
    LIFETIME_YEARS = 20
    LIFETIME_COST_HYDRO = config.COST_PER_KW_HYDRO + (15 * LIFETIME_YEARS)
    LIFETIME_COST_BIOMASS = config.COST_PER_KW_BIOMASS + (180 * LIFETIME_YEARS) # High OpEx penalty
    LIFETIME_COST_BESS = config.COST_PER_KWH_BESS + (15 * LIFETIME_YEARS)

    # Modern LFP Battery 1C discharge rate
    BATTERY_C_RATE = 1.0

    cap_hydro = pulp.LpVariable('Hydro_Capacity_kW', lowBound=config.BASE_LOAD_KW, upBound=6000)
    cap_biomass = pulp.LpVariable('Biomass_Capacity_kW', lowBound=0, upBound=6000)
    cap_bess = pulp.LpVariable('BESS_Capacity_kWh', lowBound=0, upBound=5000) 

    # Objective Function
    model += (LIFETIME_COST_HYDRO * cap_hydro) + \
             (LIFETIME_COST_BIOMASS * cap_biomass) + \
             (LIFETIME_COST_BESS * cap_bess), "Total_Lifecycle_Cost"

    winter_peak_kw = config.PEAK_LOAD_KW * 1.20
    avg_load_kw = config.BASE_LOAD_KW + (config.PEAK_LOAD_KW - config.BASE_LOAD_KW) / 2
    winter_avg_kw = avg_load_kw * 1.20
    
    critical_ratio = getattr(config, 'CRITICAL_LOAD_RATIO', 0.30)
    critical_peak_load = winter_peak_kw * critical_ratio
    critical_avg_load = winter_avg_kw * critical_ratio

    # ====================================================
    # 1. DAILY PEAK SHAVING
    # ====================================================
    battery_power = cap_bess * BATTERY_C_RATE
    model += cap_hydro + battery_power >= config.PEAK_LOAD_KW, "Daily_Peak_Shaving"

    # ====================================================
    # 2. WINTER AUTONOMY
    # ====================================================
    model += (cap_hydro * config.MIN_FLOW_MULTIPLIER) + cap_biomass >= winter_avg_kw, "Winter_Autonomy"

    # ====================================================
    # 3. EXTREME STORM SURVIVAL
    # ====================================================
    model += (cap_hydro * config.EXTREME_DROUGHT_RATIO) + cap_biomass + battery_power >= critical_peak_load, "Storm_Critical_Peak"

    # ====================================================
    # 4. SPINNING RESERVE (BESS Sizing Core Logic)
    # ====================================================
    # BESS must sustain critical load independently for 1 hour during biomass synchronization
    usable_battery = cap_bess * (1 - config.SOC_MIN_RATIO) * config.DISCHARGE_EFF
    model += usable_battery >= (critical_avg_load * 1.0), "One_Hour_Spinning_Reserve"

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    optimal_caps = {
        'hydro_kw': cap_hydro.varValue,
        'biomass_kw': cap_biomass.varValue,
        'bess_kwh': cap_bess.varValue,
        'total_capex': (config.COST_PER_KW_HYDRO * cap_hydro.varValue) + \
                       (config.COST_PER_KW_BIOMASS * cap_biomass.varValue) + \
                       (config.COST_PER_KWH_BESS * cap_bess.varValue)
    }
    
    print(f"Status: {pulp.LpStatus[model.status]}")
    print(f"Optimized Hydro Capacity  : {optimal_caps['hydro_kw']:.1f} kW")
    print(f"Optimized Biomass Capacity: {optimal_caps['biomass_kw']:.1f} kW")
    print(f"Optimized BESS Capacity   : {optimal_caps['bess_kwh']:.1f} kWh")
    print(f"Estimated Initial CapEx   : € {optimal_caps['total_capex']:,.2f}")
    print(f"20-Year Lifecycle Cost    : € {pulp.value(model.objective):,.2f}")
    print("--------------------------------------------------------\n")
    
    return optimal_caps