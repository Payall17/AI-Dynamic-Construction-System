import numpy as np

# ------------------------------
# MATERIAL PROPERTIES DATABASE
# ------------------------------

MATERIALS = {
    "Concrete": {
        "allowable_stress": 5e6,   # Pa (5 MPa)
        "cost_per_m3": 5000       # ₹ per cubic meter
    },
    "Steel": {
        "allowable_stress": 250e6, # Pa (250 MPa)
        "cost_per_m3": 60000
    }
}

# ------------------------------
# STRUCTURAL CALCULATIONS
# ------------------------------

def calculate_bending_moment(load_per_m, span):
    """
    M = wL^2 / 8
    """
    return (load_per_m * span**2) / 8


def calculate_section_modulus(width, depth):
    """
    Z = b*d^2 / 6
    """
    return (width * depth**2) / 6


def calculate_stress(moment, section_modulus):
    """
    sigma = M/Z
    """
    return moment / section_modulus


    # ------------------------------
# GENERATIVE DESIGN ENGINE
# ------------------------------

def optimize_beam(span, load_per_m, material, width=0.3):
    """
    Returns optimal depth, cost, and safety factor
    """

    allowable_stress = MATERIALS[material]["allowable_stress"]
    cost_per_m3 = MATERIALS[material]["cost_per_m3"]

    moment = calculate_bending_moment(load_per_m, span)

    best_solution = None

    # Try depths from 0.2m to 1.0m
    for depth in np.arange(0.2, 1.0, 0.01):

        Z = calculate_section_modulus(width, depth)
        stress = calculate_stress(moment, Z)

        if stress < allowable_stress:

            volume = width * depth * span
            cost = volume * cost_per_m3
            safety_factor = allowable_stress / stress

            best_solution = {
                "depth": round(depth, 3),
                "stress": round(stress, 2),
                "cost": round(cost, 2),
                "safety_factor": round(safety_factor, 2)
            }

            break   # choose minimum safe depth

    return best_solution

# ------------------------------
# SENSOR SIMULATION
# ------------------------------

def simulate_sensor_load(expected_load):
    """
    Simulates real site load variation (±20%)
    """
    variation = np.random.uniform(-0.2, 0.2)
    actual_load = expected_load * (1 + variation)
    return round(actual_load, 2)

# ------------------------------
# RECALIBRATION ENGINE
# ------------------------------

def recalibrate_design(span, expected_load, material, width=0.3):

    print("\n--- Initial Design ---")
    initial_design = optimize_beam(span, expected_load, material, width)
    print(initial_design)

    actual_load = simulate_sensor_load(expected_load)
    print("\nSensor detected load:", actual_load, "N/m")

    print("\n--- Recalibrated Design ---")
    updated_design = optimize_beam(span, actual_load, material, width)
    print(updated_design)

    return initial_design, updated_design



if __name__ == "__main__":

    span = 5              # meters
    expected_load = 20000 # N/m
    material = "Concrete"

    recalibrate_design(span, expected_load, material)
