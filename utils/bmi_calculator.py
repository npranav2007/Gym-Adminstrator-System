def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI using weight in kg and height in cm
    BMI = weight(kg) / height(m)²
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 2)


def calculate_calories(weight_kg, height_cm, age, goal):
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5

    maintenance_calories = bmr * 1.55

    if goal == 'weight_loss':
        return round(maintenance_calories * 0.8)
    elif goal == 'weight_gain':
        return round(maintenance_calories * 1.15)
    else:
        # Maintenance
        return round(maintenance_calories)