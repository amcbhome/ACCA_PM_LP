import streamlit as st
import pulp

# =============================================================================
# 1. PAGE CONFIGURATION & ARCHITECTURE
# =============================================================================
st.set_page_config(
    page_title="Operations Optimization Suite", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧮 Operations & Logistics Optimization Suite")
st.markdown("---")

# Navigation Sidebar to switch between the two models
app_mode = st.sidebar.selectbox(
    "Choose Optimization Model:",
    ["Product Mix (PM) Optimizer", "SBL Depot Dispatch Optimizer"]
)

# =============================================================================
# 2. MODEL 1: PRODUCT MIX (PM) OPTIMIZER
# =============================================================================
if app_mode == "Product Mix (PM) Optimizer":
    st.header("📊 Product Mix Optimization Engine")
    st.markdown(
        "Adjust available resource capacities to maximize total contribution margin ($C$). "
        "The model dynamically calculates the ideal production quantities for products $x$ and $y$."
    )
    
    # User Inputs via Sidebar
    st.sidebar.header("PM Resource Constraints")
    # 16000 and 15000 are the original baseline values
    input_labour = st.sidebar.number_input("Total Labour Capacity (Hrs):", min_value=0.0, value=16000.0, step=500.0)
    input_material = st.sidebar.number_input("Total Material Capacity (Units):", min_value=0.0, value=15000.0, step=500.0)
    
    if st.sidebar.button("Run PM Optimization"):
        # Setup PuLP Maximization Problem
        pm_model = pulp.LpProblem("Maximize_Product_Mix", pulp.LpMaximize)
        
        # Decision Variables
        x = pulp.LpVariable('x', lowBound=0, cat='Continuous')
        y = pulp.LpVariable('y', lowBound=0, cat='Continuous')
        
        # Objective Function
        pm_model += 30 * x + 40 * y, "Objective_Function"
        
        # Constraints based on user input
        pm_model += 4 * x + 4 * y <= input_labour, "Labour_Constraint"
        pm_model += 3 * x + 5 * y <= input_material, "Material_Constraint"
        
        # Solve
        status = pm_model.solve()
        status_str = pulp.LpStatus[status]
        
        if status_str == "Optimal":
            st.success(f"Solver Status: {status_str}")
            
            # Display KPI Metric Cards
            col1, col2, col3 = st.columns(3)
            col1.metric("Optimal x Units", f"{pulp.value(x):,}")
            col2.metric("Optimal y Units", f"{pulp.value(y):,}")
            col3.metric("Max Contribution (C)", f"£{pulp.value(pm_model.objective):,}")
            
            # Clear mathematical verification summary
            st.info(
                f"**Verification:** Producing **{pulp.value(x):,}** units of x and **{pulp.value(y):,}** units of y "
                f"utilizes {4*pulp.value(x) + 4*pulp.value(y):,} hours of labour and "
                f"{3*pulp.value(x) + 5*pulp.value(y):,} units of material."
            )
        else:
            st.error(f"Solver could not find an optimal solution. Status: {status_str}")

# =============================================================================
# 3. MODEL 2: SBL DEPOT DISPATCH OPTIMIZER
# =============================================================================
elif app_mode == "SBL Depot Dispatch Optimizer":
    st.header("🚛 SBL Logistics & Dispatch Transportation Optimizer")
    st.markdown(
        "Input required dispatch targets across distribution nodes to minimize total systemic transit costs ($Z$). "
        "Destination capacities remain bounded to upper thresholds."
    )
    
    # User Inputs via Sidebar
    st.sidebar.header("Depot Dispatch Volume Targets")
    # 2500, 3100, and 1250 are the original baseline values
    d1 = st.sidebar.number_input("Depot 1 Required Target:", min_value=0.0, value=2500.0, step=50.0)
    d2 = st.sidebar.number_input("Depot 2 Required Target:", min_value=0.0, value=3100.0, step=50.0)
    d3 = st.sidebar.number_input("Depot 3 Required Target:", min_value=0.0, value=1250.0, step=50.0)
    
    if st.sidebar.button("Run Dispatch Optimization"):
        # Setup PuLP Minimization Problem
        sbl_model = pulp.LpProblem("Minimize_Z", pulp.LpMinimize)
        
        # 9 Decision Variables for Routes
        X = {i: pulp.LpVariable(f"X{i}", lowBound=0, cat='Continuous') for i in range(1, 10)}
        
        # Constant matrices (Costs and multipliers)
        Y = {
            1: 22, 2: 33, 3: 40,
            4: 27, 5: 30, 6: 22,
            7: 36, 8: 20, 9: 25
        }
        z_multiplier = 5
        
        # Objective Function
        sbl_model += pulp.lpSum(X[i] * Y[i] * z_multiplier for i in range(1, 10)), "Objective_Function"
        
        # Dynamic Source/Depot Constraints matching user inputs
        sbl_model += X[1] + X[2] + X[3] == d1, "Equality_Constraint_1"
        sbl_model += X[4] + X[5] + X[6] == d2, "Equality_Constraint_2"
        sbl_model += X[7] + X[8] + X[9] == d3, "Equality_Constraint_3"
        
        # Boundary Destination Capacity Constraints (Fixed upper bounds)
        sbl_model += X[1] + X[4] + X[7] <= 2000, "Inequality_Constraint_1"
        sbl_model += X[2] + X[5] + X[8] <= 3000, "Inequality_Constraint_2"
        sbl_model += X[3] + X[6] + X[9] <= 2000, "Inequality_Constraint_3"
        
        # Solve
        status = sbl_model.solve()
        status_str = pulp.LpStatus[status]
        
        if status_str == "Optimal":
            st.success("System Status: Optimized successfully.")
            st.metric(label="Minimum Total Cost (Z)", value=f"£{pulp.value(sbl_model.objective):,2f}")
            
            st.subheader("Optimal Route Allocation Matrix")
            
            # Formatted 3-Column Layout for clear viewing
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("**Depot 1 Direct Routes**")
                st.metric("Route X1 Allocation", f"{X[1].varValue:,.1f}")
                st.metric("Route X2 Allocation", f"{X[2].varValue:,.1f}")
                st.metric("Route X3 Allocation", f"{X[3].varValue:,.1f}")
                
            with col2:
                st.info("**Depot 2 Direct Routes**")
                st.metric("Route X4 Allocation", f"{X[4].varValue:,.1f}")
                st.metric("Route X5 Allocation", f"{X[5].varValue:,.1f}")
                st.metric("Route X6 Allocation", f"{X[6].varValue:,.1f}")
                
            with col3:
                st.info("**Depot 3 Direct Routes**")
                st.metric("Route X7 Allocation", f"{X[7].varValue:,.1f}")
                st.metric("Route X8 Allocation", f"{X[8].varValue:,.1f}")
                st.metric("Route X9 Allocation", f"{X[9].varValue:,.1f}")
        else:
            st.error(
                f"Optimization failed. The input distribution criteria cannot be balanced against "
                f"downstream destination bounds. (Status: {status_str})"
            )
