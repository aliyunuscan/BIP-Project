# data_handler.py
import numpy as np
import pandas as pd
import config

def get_data(hours=8760):
    time_index = np.arange(hours)
    
    # =========================================================
    # 1. REALISTIC LOAD PROFILE (Dual-Peak Residential Model)
    # =========================================================
    daily_t = (time_index % 24)
    
    # Morning (08:00) and Evening (19:00) peaks using Gaussian curves
    morning_peak = 0.35 * np.exp(-0.5 * ((daily_t - 8) / 1.5)**2)
    evening_peak = 0.60 * np.exp(-0.5 * ((daily_t - 19) / 2.0)**2)
    daily_curve = 1.0 + morning_peak + evening_peak
    
    # Seasonal Consumption Multiplier: Heating in winter, light HVAC in summer
    seasonal_curve = 1.05 + 0.15 * np.cos(2 * np.pi * time_index / 8760)
    
    # Base load modified by profiles and realistic Gaussian noise
    base_load = config.BASE_LOAD_KW
    noise = np.random.normal(0, 80, hours) # Mean 0, Std Dev 80 kW
    
    load_kw = (base_load * daily_curve * seasonal_curve) + noise
    
    # =========================================================
    # 2. PHYSICAL RIVER FLOW SIMULATION
    # =========================================================
    annual_cycle = -np.cos((time_index / 8760) * 2 * np.pi) 
    flow_multiplier = config.MIN_FLOW_MULTIPLIER + ((annual_cycle + 1) / 2) * (config.MAX_FLOW_MULTIPLIER - config.MIN_FLOW_MULTIPLIER)
    flow_multiplier += np.random.normal(0, 0.05, hours) 
    flow_multiplier = np.clip(flow_multiplier, 0, 1)

    # =========================================================
    # 3. INJECTING EXTREME WEATHER EVENTS
    # =========================================================
    
    # Event 1: Winter Freeze (High load, low flow)
    flow_multiplier[config.EVENT_WINTER_FREEZE_START:config.EVENT_WINTER_FREEZE_END] = config.EXTREME_DROUGHT_RATIO
    load_kw[config.EVENT_WINTER_FREEZE_START:config.EVENT_WINTER_FREEZE_END] *= 1.20 

    # Event 2: Summer Heatwave (High load, low flow due to evaporation)
    flow_multiplier[config.EVENT_SUMMER_HEATWAVE_START:config.EVENT_SUMMER_HEATWAVE_END] = 0.15
    load_kw[config.EVENT_SUMMER_HEATWAVE_START:config.EVENT_SUMMER_HEATWAVE_END] *= 1.15

    # Event 3: Vaia Storm (Zero hydro flow due to intake blockage)
    flow_multiplier[config.EVENT_VAIA_STORM_START:config.EVENT_VAIA_STORM_END] = 0.0

    return pd.DataFrame({
        'Load_kW': np.clip(load_kw, base_load * 0.5, config.PEAK_LOAD_KW * 1.5),
        'Flow_Ratio': flow_multiplier
    })