import pulp

def solve_product_mix(max_labour, max_material):
    """
    Solves the PM Maximization problem based on dynamic resource constraints.
    
    Parameters:
    max_labour (float): Maximum available units for Constraint 1 (originally 16,000)
    max_material (float): Maximum available units for Constraint 2 (originally 15,000)
    """
    # Define the problem
    [span_1](start_span)model = pulp.LpProblem("Maximize_Product_Mix", pulp.LpMaximize)[span_1](end_span)
    
    # Define decision variables
    [span_2](start_span)x = pulp.LpVariable('x', lowBound=0, cat='Continuous')[span_2](end_span)
    [span_3](start_span)y = pulp.LpVariable('y', lowBound=0, cat='Continuous')[span_3](end_span)
    
    # Objective Function (Contribution margins remain static, or can be parameterized later)
    [span_4](start_span)model += 30 * x + 40 * y, "Objective_Function"[span_4](end_span)
    
    # Dynamic Constraints based on user input
    [span_5](start_span)model += 4 * x + 4 * y <= max_labour, "Labour_Constraint"[span_5](end_span)
    [span_6](start_span)model += 3 * x + 5 * y <= max_material, "Material_Constraint"[span_6](end_span)
    
    # Solve
    [span_7](start_span)status = model.solve()[span_7](end_span)
    [span_8](start_span)status_str = pulp.LpStatus[status][span_8](end_span)
    
    [span_9](start_span)if status_str == "Optimal":[span_9](end_span)
        return {
            [span_10](start_span)"status": status_str,[span_10](end_span)
            [span_11](start_span)"optimal_x": pulp.value(x),[span_11](end_span)
            [span_12](start_span)"optimal_y": pulp.value(y),[span_12](end_span)
            [span_13](start_span)"max_contribution": pulp.value(model.objective)[span_13](end_span)
        }
    else:
        return {
            "status": status_str,
            "optimal_x": 0.0,
            "optimal_y": 0.0,
            "max_contribution": 0.0
        }
