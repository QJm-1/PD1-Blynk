LIME_DENSITY_G_PER_ROTATION = 2.3   # grams per auger rotation (calibrate this)
TARGET_PH = 6.75
BUFFER_CAPACITY = 8.5               # g CaCO3 per pH unit per kg of cake

def calculate_lime_dose(current_ph, cake_mass_kg=1.0):
    if current_ph >= TARGET_PH:
        return 0.0
    delta_ph = TARGET_PH - current_ph
    grams_needed = delta_ph * BUFFER_CAPACITY * cake_mass_kg
    return round(grams_needed, 2)

def grams_to_rotations(grams):
    return round(grams / LIME_DENSITY_G_PER_ROTATION, 1)
