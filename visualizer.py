# visualizer.py
import os
import matplotlib.pyplot as plt
import config

def plot_and_save(results, start_hour, end_hour, filename, title_prefix):
    test_data = results.iloc[start_hour:end_hour]
    x_vals = test_data.index.to_numpy()
    
    fig, (ax_flow, ax_power, ax_soc) = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
    
    # --- 1. RIVER FLOW AND EXTREME EVENTS ---
    ax_flow.plot(x_vals, test_data['Flow_Ratio'].to_numpy() * 100, color='teal', linewidth=2, label='River Flow Potential (%)')
    
    # Event 1: Winter Freeze
    if config.EVENT_WINTER_FREEZE_START < end_hour and config.EVENT_WINTER_FREEZE_END > start_hour:
        ax_flow.axvspan(max(start_hour, config.EVENT_WINTER_FREEZE_START), 
                        min(end_hour, config.EVENT_WINTER_FREEZE_END), 
                        color='blue', alpha=0.15, label='Winter Freeze (Drought)')
                        
    # Event 2: Summer Heatwave
    if config.EVENT_SUMMER_HEATWAVE_START < end_hour and config.EVENT_SUMMER_HEATWAVE_END > start_hour:
        ax_flow.axvspan(max(start_hour, config.EVENT_SUMMER_HEATWAVE_START), 
                        min(end_hour, config.EVENT_SUMMER_HEATWAVE_END), 
                        color='orange', alpha=0.15, label='Summer Heatwave')
                        
    # Event 3: Vaia Storm
    if config.EVENT_VAIA_STORM_START < end_hour and config.EVENT_VAIA_STORM_END > start_hour:
        ax_flow.axvspan(max(start_hour, config.EVENT_VAIA_STORM_START), 
                        min(end_hour, config.EVENT_VAIA_STORM_END), 
                        color='red', alpha=0.2, label='Vaia Storm (Grid Failure)')

    ax_flow.set_ylabel('Flow Ratio (%)')
    ax_flow.set_title(f'{title_prefix} - Hydrological Conditions & Extreme Event Windows')
    ax_flow.legend(loc='upper right')
    ax_flow.grid(True, alpha=0.3)

    # --- 2. GENERATION MIX AND LOAD (Stackplot) ---
    ax_power.stackplot(x_vals, 
                  test_data['Hydro_Gen_kW'], 
                  test_data['Biomass_kW'], 
                  labels=['Optimized Hydro', 'Biomass Backup'],
                  colors=['#3498db', '#e67e22'],
                  alpha=0.85)
    
    ax_power.plot(x_vals, test_data['Load_kW'].to_numpy(), label='Original Demand', color='gray', linewidth=1, linestyle=':')
    ax_power.plot(x_vals, test_data['Served_Load_kW'].to_numpy(), label='Actual Served Load (Drops to 30%)', color='black', linewidth=2, linestyle='--')
    
    if test_data['Unmet_Load_kW'].sum() > 0:
         ax_power.bar(x_vals, test_data['Unmet_Load_kW'].to_numpy(), color='red', alpha=0.9, label='UNMET LOAD (BLACKOUT)')
         
    ax_power.set_ylabel('Power (kW)')
    ax_power.set_title(f'{title_prefix} - Generation Mix vs Community Load Response')
    ax_power.legend(loc='upper right', fontsize='small')
    ax_power.grid(True, alpha=0.3)

    # --- 3. BESS STATE OF CHARGE (SoC) ---
    ax_soc.plot(x_vals, test_data['Battery_SoC_kWh'].to_numpy(), label='BESS State of Charge', color='purple', linewidth=2)
    
    soc_min_val = results['Battery_SoC_kWh'].max() * config.SOC_MIN_RATIO
    ax_soc.axhline(y=soc_min_val, color='red', linestyle=':', label='Min SoC Limit (20%)')
    
    ax_soc.set_xlabel('Hour of the Year')
    ax_soc.set_ylabel('Energy (kWh)')
    ax_soc.set_title(f'{title_prefix} - Battery Energy Storage System (BESS) Dynamics')
    ax_soc.legend(loc='upper right')
    ax_soc.grid(True, alpha=0.3)

    plt.tight_layout()
    
    # Save the figure to the 'results' directory
    os.makedirs('results', exist_ok=True)
    filepath = os.path.join('results', filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Plot saved successfully: {filepath}")
    plt.close(fig)

def generate_and_save_plots(results):
    # 1. Weekly Stress Test Plot (e.g., Winter Freeze window)
    plot_and_save(results, start_hour=450, end_hour=650, filename='weekly_stress_test.png', title_prefix='Weekly Stress Test')
    
    # 2. Annual Complete Plot
    plot_and_save(results, start_hour=0, end_hour=8760, filename='annual_overview.png', title_prefix='Annual Overview')