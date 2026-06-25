# ems_core.py
import numpy as np
import pandas as pd
import config

def run_simulation(data, capacities):
    hours = len(data)
    battery_soc = np.zeros(hours)
    biomass_gen = np.zeros(hours)
    
    shedded_load = np.zeros(hours)        
    unmet_critical_load = np.zeros(hours) 
    served_load = np.zeros(hours) 
    
    bess_cap = capacities['bess_kwh']
    hydro_cap = capacities['hydro_kw']
    biomass_cap = capacities['biomass_kw']
    
    soc_min = config.SOC_MIN_RATIO * bess_cap
    soc_max = bess_cap
    current_soc = bess_cap * 0.8 
    
    critical_ratio = getattr(config, 'CRITICAL_LOAD_RATIO', 0.30)
    hydro_gen = data['Flow_Ratio'] * hydro_cap
    
    for t in range(hours):
        load_t = data['Load_kW'].iloc[t]
        
        # PROACTIVE EMERGENCY CONTROL (Load Shedding)
        is_emergency = data['Flow_Ratio'].iloc[t] <= (config.EXTREME_DROUGHT_RATIO + 0.05)
        
        if is_emergency:
            actual_load = load_t * critical_ratio 
            shedded_load[t] = load_t - actual_load
        else:
            actual_load = load_t
            shedded_load[t] = 0
            
        ren_t = hydro_gen.iloc[t]
        net_load = actual_load - ren_t
        
        biomass_used = 0
        battery_space = (soc_max - current_soc) / config.CHARGE_EFF
        
        # --- SCENARIO A: HYDRO DEFICIT ---
        if net_load > 0:
            if biomass_cap >= net_load:
                biomass_to_load = net_load
                biomass_left = biomass_cap - net_load
                
                # Aggressively charge battery with excess biomass power
                biomass_to_batt = min(biomass_left, battery_space)
                biomass_used = biomass_to_load + biomass_to_batt
                
                current_soc += biomass_to_batt * config.CHARGE_EFF
                deficit = 0
            else:
                biomass_used = biomass_cap
                deficit = net_load - biomass_cap
                
                # Biomass maxed out, discharge battery
                available_battery_power = min((current_soc - soc_min) * config.DISCHARGE_EFF, bess_cap * config.BATTERY_C_RATE)
                if available_battery_power >= deficit:
                    current_soc -= deficit / config.DISCHARGE_EFF
                    deficit = 0
                else:
                    current_soc -= available_battery_power / config.DISCHARGE_EFF
                    deficit -= available_battery_power
                    unmet_critical_load[t] = deficit # True blackout condition
                    
        # --- SCENARIO B: HYDRO SURPLUS ---
        else:
            surplus = abs(net_load)
            
            # Charge battery with hydro surplus
            hydro_to_batt = min(surplus, battery_space)
            current_soc += hydro_to_batt * config.CHARGE_EFF
            battery_space -= hydro_to_batt
            
            # AGGRESSIVE CHARGING RULE: Force biomass if BESS is not 100%
            if battery_space > 0:
                biomass_to_batt = min(biomass_cap, battery_space)
                biomass_used = biomass_to_batt
                current_soc += biomass_to_batt * config.CHARGE_EFF

        battery_soc[t] = current_soc
        biomass_gen[t] = biomass_used
        served_load[t] = actual_load - unmet_critical_load[t]

    results_df = data.copy()
    results_df['Hydro_Gen_kW'] = hydro_gen
    results_df['Biomass_kW'] = biomass_gen
    results_df['Battery_SoC_kWh'] = battery_soc
    results_df['Shedded_Load_kW'] = shedded_load
    results_df['Unmet_Critical_Load_kW'] = unmet_critical_load
    
    # Log actual blackout vs intentional load shedding
    results_df['Unmet_Load_kW'] = unmet_critical_load 
    results_df['Served_Load_kW'] = served_load 
     
    return results_df