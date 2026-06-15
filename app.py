import streamlit as st
from model import solve_product_mix

st.set_page_config(page_title="Product Mix Optimizer", layout="centered")

st.title("📊 Product Mix Optimization Engine")
st.markdown("Adjust the available resource capacities below to calculate the optimal production mix.")

st.sidebar.header("Resource Constraints Input")
# Defaults are set to your original baseline values (16,000 and 15,000)
input_labour = st.sidebar.number_input("Total Labour Capacity:", min_value=0.0, value=16000.0, step=500.0)
input_material = st.sidebar.number_input("Total Material Capacity:", min_value=0.0, value=15000.0, step=500.0)

if st.sidebar.button("Run Optimization"):
    results = solve_product_mix(input_labour, input_material)
    
    if results["status"] == "Optimal":
        st.success(f"Solver Status: {results['status']}")
        
        # Display key metric cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Optimal x Units", f"{results['optimal_x']:,}")
        col2.metric("Optimal y Units", f"{results['optimal_y']:,}")
        col3.metric("Max Contribution (C)", f"£{results['max_contribution']:,}")
        
    else:
        st.error(f"Solver could not find an optimal solution. Status: {results['status']}")
