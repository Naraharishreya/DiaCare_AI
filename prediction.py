import numpy as np

def predict_diabetes(model, bp, chol, bmi, smoke, act, fruit, veg, sex, age):

    # arrange features in EXACT same order as training
    features = np.array([[bp, chol, bmi, smoke, act, fruit, veg, sex, age]])

    prediction = model.predict(features)[0]

    # probability (confidence)
    confidence = max(model.predict_proba(features)[0])

    return prediction, confidence