def get_recommendations(bmi, bp, chol, smoke, activity, fruit, veg, age, prediction):

    diet = []
    exercise = []
    water = ""
    sleep = ""

    # ---------------- DIET ----------------
    if prediction == 2:  # Diabetes
        diet = [
            "Avoid sugar, sweets, soft drinks",
            "Eat high fiber foods (vegetables, oats)",
            "Low carb balanced meals",
            "Increase protein intake"
        ]
    elif prediction == 1:  # Pre-diabetes
        diet = [
            "Reduce sugar intake",
            "Eat whole grains",
            "Add fruits moderately",
            "Avoid processed food"
        ]
    else:
        diet = [
            "Maintain balanced diet",
            "Eat fruits and vegetables daily",
            "Avoid junk food"
        ]

    # ---------------- EXERCISE ----------------
    if bmi > 30:
        exercise = [
            "30-45 min walking daily",
            "Light cardio exercises",
            "Yoga for weight loss"
        ]
    else:
        exercise = [
            "30 min walking or jogging",
            "Light gym workout",
            "Stretching exercises"
        ]

    # ---------------- WATER ----------------
    if age > 50:
        water = "Drink 2.5–3 liters of water daily"
    else:
        water = "Drink 3–4 liters of water daily"

    # ---------------- SLEEP ----------------
    if prediction == 2:
        sleep = "Sleep 7–8 hours, maintain strict routine"
    else:
        sleep = "Sleep 6–8 hours daily"

    return {
        "diet": diet,
        "exercise": exercise,
        "water": water,
        "sleep": sleep
    }