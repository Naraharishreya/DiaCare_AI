def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


def calculate_health_score(bmi, bp, chol, smoke, act, fruit, veg):

    score = 100

    # BMI penalty
    if bmi > 25:
        score -= 15
    if bmi > 30:
        score -= 25

    # risk factors
    score -= bp * 15
    score -= chol * 15
    score -= smoke * 20

    # good habits
    score += act * 10
    score += fruit * 5
    score += veg * 5

    return max(0, min(score, 100))