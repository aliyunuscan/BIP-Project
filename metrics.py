# metrics.py
import pandas as pd

def print_analysis_report(results, capacities=None):
    from config import HYDRO_DAM_CAPACITY, HYDRO_RIVER_CAPACITY, BIOMASS_CAPACITY, DIESEL_CAPACITY, BATTERY_CAPACITY
    
    bess_cap = capacities['bess'] if capacities else BATTERY_CAPACITY

    total_load = results['Load_kW'].sum() / 1000
    hydro_dam_total = results['Hydro_Dam_Gen_kW'].sum() / 1000
    hydro_river_total = results['Hydro_River_Gen_kW'].sum() / 1000
    biomass_total = results['Biomass_kW'].sum() / 1000
    diesel_total = results['Diesel_kW'].sum() / 1000
    
    total_supply = hydro_dam_total + hydro_river_total + biomass_total + diesel_total
    total_system_cap = HYDRO_DAM_CAPACITY + HYDRO_RIVER_CAPACITY + BIOMASS_CAPACITY + DIESEL_CAPACITY
    
    unmet_load = results['Unmet_Load_kW'].sum() / 1000
    dump_load = results['Dump_Load_kW'].sum() / 1000
    
    lpsp = (unmet_load / total_load) * 100 
    coverage = 100 - lpsp
    ren_fraction = ((hydro_dam_total + hydro_river_total + biomass_total) / total_supply) * 100 if total_supply > 0 else 0

    print("\n" + "="*65)
    print(" SYSTEM PERFORMANCE METRICS")
    print("="*65 + "\n")
    
    print(f"Total Annual Energy Demand: {total_load:,.1f} MWh\n")
    
    print("--- Annual Generation Mix and Capacities ---")
    print(f"Micro-Hydro (Dam)   | {HYDRO_DAM_CAPACITY:,.1f} kW    | {hydro_dam_total:,.1f} MWh    | {(hydro_dam_total/total_supply)*100:.1f} %")
    print(f"Micro-Hydro (River) | {HYDRO_RIVER_CAPACITY:,.1f} kW    | {hydro_river_total:,.1f} MWh    | {(hydro_river_total/total_supply)*100:.1f} %")
    print(f"Biomass CHP         | {BIOMASS_CAPACITY:,.1f} kW    | {biomass_total:,.1f} MWh    | {(biomass_total/total_supply)*100:.1f} %")
    print(f"Diesel (Backup)     | {DIESEL_CAPACITY:,.1f} kW    | {diesel_total:,.1f} MWh       | {(diesel_total/total_supply)*100:.2f} %")
    print(f"Total System        | {total_system_cap:,.1f} kW   | {total_supply:,.1f} MWh    | 100.0 %")
    print("----------------------------------------------------------\n")
    
    print(f"BESS Capacity                     : {bess_cap:,.1f} kWh")
    print(f"Dump Load / Surplus               : {dump_load:,.1f} MWh")
    print(f"Renewable Penetration Rate        : {ren_fraction:.2f} %")
    print(f"Energy Consumption Coverage       : {coverage:.4f} %")
    print(f"LPSP / Blackout Risk              : {lpsp:.4f} %")
    print(f"Diesel Generation Used            : {diesel_total:.1f} MWh")
    
    print("\n" + "="*65)