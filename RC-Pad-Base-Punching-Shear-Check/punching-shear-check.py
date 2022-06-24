import numpy as np

# Transverse Across the pad base
def shear_checkT(ground_pressure,
            effective_depth,
            pad_width,
            column_dim):
    # param ground_pressure: The maximum value of ground pressure exerted by soil on the pad base
    # param...to be completed

    shear_force = ground_pressure * pad_width * ((pad_width/2) - (column_dim/2) - effective_depth)
    shear_area = pad width * effective_depth
    
    shear_stress = shear_force/shear_stress
    ret shear_stress
