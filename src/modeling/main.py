import uuid
from typing import Union
from pathlib import Path
from fastapi import FastAPI
from src.config import MODELS_DIR, PROCESSED_DATA_DIR
from src.modeling.predict import make_prediction

app = FastAPI()

# ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
features_path: Path = PROCESSED_DATA_DIR / "test_features.csv"
model_path: Path = MODELS_DIR / "model.pkl"
predictions_path: Path = PROCESSED_DATA_DIR / "test_predictions.csv"
test_labels_path: Path = PROCESSED_DATA_DIR / "test_labels.csv"
item_path : Path = PROCESSED_DATA_DIR / "item.txt"
# -----------------------------------------


@app.get("/")
def read_root():
    with open(item_path, "r") as f:
        items = f.read()
    items = items.strip().split("\n")
    # Return as a list of items
    list(items)
    return {"items": items}

    # with open(features_path, "r") as f1:
    #     features_items = f1.readlines()
    # with open (predictions_path, "r") as f2:
    #     predictions_items = f2.readlines()
    # with open (test_labels_path, "r") as f3:
    #     labels_items = f3.readlines()
    # # Combine features, predictions, labels into a list of dictionaries
    # # Use first line as header
    # header = features_items[0].strip().split(",")
    # data = []
    # for i in range(1, len(features_items)):
    #     feature_values = features_items[i].strip().split(",")
    #     prediction_value = predictions_items[i].strip().split(",")[0]
    #     label_value = labels_items[i].strip().split(",")[0]
    #     item = {header[j]: feature_values[j] for j in range(len(header))}
    #     item["prediction"] = prediction_value
    #     item["true_label"] = label_value
    #     data.append(item)
    # return {"data": data}
    
@app.get("/items/{item_id}")
def read_item(id: str):

    # Read the item file
    with open(item_path, "r") as f:
        items = f.read()
    items = items.strip().split("\n")
    # Find the item with the given id
    for item in items:
        if item.startswith(f"ID: {id},"):
            return {"item": item}
    return {"error": "Item not found"}, 404
    
    # # --- TEMPORARY DIAGNOSTIC PRINTS START ---
    # print(f"\n--- DEBUG START ---")
    # print(f"1. Raw item_id received: '{item_id}'")
    
    # try:
    #     # 1. Parse the string input (item_id) into a list of floats
    #     feature_string = item_id.split(',')
    #     print(f"2. After split: {feature_string}")
        
    #     features = []
    #     for i, f in enumerate(feature_string):
    #         stripped_f = f.strip()
    #         print(f"3. Processing element #{i}: Raw='{f}', Stripped='{stripped_f}'")
            
    #         # Check if stripped string is empty (handles extra commas)
    #         if not stripped_f:
    #             print(f"   Skipping empty element #{i}.")
    #             continue
            
    #         # This is where the ValueError is likely happening
    #         features.append(float(stripped_f))

    #     # We will not use the list comprehension for now to isolate the error better:
    #     # features = [float(f.strip()) for f in feature_string if f.strip()]
        
    #     # --- TEMPORARY DIAGNOSTIC PRINTS END ---
    #     print(f"4. Final features list (len={len(features)}): {features}")
    #     print(f"--- DEBUG END ---\n")
    #     # -------------------------------------
        
        
    #     # You should validate that you have the correct number of features!
    #     if len(features) != 11: # Assuming 11 features from your example input
    #          # We include the 400 status code as the second element in the tuple
    #          return {"error": f"Invalid feature count. Expected 11 features, received {len(features)}."}, 400

    #     # 2. Call the refactored function
    #     prediction = make_prediction(features) 

    #     # 3. Return the result
    #     return {
    #         "features": features,
    #         "prediction": prediction
    #     }
        
    # except ValueError as ve:
    #     # Now we can catch the exact value error message
    #     print(f"!!! CRITICAL ERROR: ValueError during float conversion: {ve}")
    #     return {"error": "Invalid input format. Features must be comma-separated numbers."}, 400
    # except Exception as e:
    #     print(f"!!! CRITICAL ERROR: General Exception: {e}")
    #     return {"error": f"An error occurred during prediction: {e}"}, 500
    
@app.post("/create_item/")
def create_item(fixed_acidity: str, volatile_acidity: str, citric_acid: str, residual_sugar: str,
                chlorides: str, free_sulfur_dioxide: str, total_sulfur_dioxide: str,
                density: str, pH: str, sulphates: str, alcohol: str):
    # Construct item_id string
    item = f"{fixed_acidity},{volatile_acidity},{citric_acid},{residual_sugar},{chlorides},{free_sulfur_dioxide},{total_sulfur_dioxide},{density},{pH},{sulphates},{alcohol}"
    #fixed acidity,volatile acidity,citric acid,residual sugar,chlorides,free sulfur dioxide,total sulfur dioxide,density,pH,sulphates,alcohol,quality,Id

    id = str(uuid.uuid4())

    # --- TEMPORARY DIAGNOSTIC PRINTS START ---
    print(f"\n--- DEBUG START ---")
    print(f"1. Raw item_id received: '{item}'")
    
    try:
        # 1. Parse the string input (item_id) into a list of floats
        feature_string = item.split(',')
        print(f"2. After split: {feature_string}")
        
        features = []
        for i, f in enumerate(feature_string):
            stripped_f = f.strip()
            print(f"3. Processing element #{i}: Raw='{f}', Stripped='{stripped_f}'")
            
            # Check if stripped string is empty (handles extra commas)
            if not stripped_f:
                print(f"   Skipping empty element #{i}.")
                continue
            
            # This is where the ValueError is likely happening
            features.append(float(stripped_f))

        # We will not use the list comprehension for now to isolate the error better:
        # features = [float(f.strip()) for f in feature_string if f.strip()]
        
        # --- TEMPORARY DIAGNOSTIC PRINTS END ---
        print(f"4. Final features list (len={len(features)}): {features}")
        print(f"--- DEBUG END ---\n")
        # -------------------------------------
        
        
        # You should validate that you have the correct number of features!
        if len(features) != 11: # Assuming 11 features from your example input
             # We include the 400 status code as the second element in the tuple
             return {"error": f"Invalid feature count. Expected 11 features, received {len(features)}."}, 400

        # 2. Call the refactored function
        prediction = make_prediction(features)

        # Append the string representation of the item dictionary to the file
        with open(item_path, "a") as f:
            f.write(f'ID: {id}, features: {str(features)}, prediction: {str(prediction)}' + "\n")
    #     return {"message": "Item created", "item": item}

        # 3. Return the result
        return {
            "ID": id,
            "features": features,
            "prediction": prediction
        }
        
    except ValueError as ve:
        # Now we can catch the exact value error message
        print(f"!!! CRITICAL ERROR: ValueError during float conversion: {ve}")
        return {"error": "Invalid input format. Features must be comma-separated numbers."}, 400
    except Exception as e:
        print(f"!!! CRITICAL ERROR: General Exception: {e}")
        return {"error": f"An error occurred during prediction: {e}"}, 500


    # get, post, put, patch, delete