import pickle
import numpy as np

model = pickle.load(open("fertilizer_module/models/fertilizer_model.pkl","rb"))

soil_encoder = pickle.load(open("fertilizer_module/models/soil_encoder.pkl","rb"))
crop_encoder = pickle.load(open("fertilizer_module/models/crop_encoder.pkl","rb"))
fert_encoder = pickle.load(open("fertilizer_module/models/fert_encoder.pkl","rb"))


def predict_fertilizer(data):

    soil = soil_encoder.transform([data["soil_type"]])[0]
    crop = crop_encoder.transform([data["crop"]])[0]


    features = np.array([[

        data["temperature"],
        data["humidity"],
        data["ph"],
        data["rainfall"],
        soil,
        crop,
        data["N"],
        data["P"],
        data["K"]

    ]])

    prediction = model.predict(features)

    fertilizer = fert_encoder.inverse_transform(prediction)

    return fertilizer[0]