# main.py
from optimizer import get_optimal_capacities
from data_handler import get_data
from ems_core import run_simulation
from visualizer import generate_and_save_plots

def main():
    print("======================================================")
    print(" HYBRID MICROGRID END-TO-END SIMULATION (PIEVE DI CADORE)")
    print("======================================================\n")
    
    print("1. Running MILP Optimization for system sizing...")
    optimal_caps = get_optimal_capacities()
    
    print("2. Generating annual data based on physical flow dynamics...")
    df = get_data() 
    
    print("3. Running Energy Management System (EMS) simulation with optimized values...")
    results = run_simulation(df, optimal_caps)
    
    total_unmet = results['Unmet_Load_kW'].sum()
    print(f"\nSimulation Complete. Total Unmet Load: {total_unmet:.2f} kW")
    
    print("4. Generating and saving plots to '/results' directory...")
    generate_and_save_plots(results)

if __name__ == "__main__":
    main()