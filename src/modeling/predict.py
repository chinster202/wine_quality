from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer
import pickle
import pandas as pd
import xgboost as xgb

from src.config import MODELS_DIR, PROCESSED_DATA_DIR

# app = typer.Typer()

# ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
features_path: Path = PROCESSED_DATA_DIR / "test_features.csv"
model_path: Path = MODELS_DIR / "model.pkl"
predictions_path: Path = PROCESSED_DATA_DIR / "test_predictions.csv"
test_labels_path: Path = PROCESSED_DATA_DIR / "test_labels.csv"
# -----------------------------------------

# @app.command()
def make_prediction(features: list[float] = None) -> int:

    FEATURE_NAMES = [
    "fixed acidity", "volatile acidity", "citric acid", "residual sugar", 
    "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density", 
    "pH", "sulphates", "alcohol"]

    # Read pkl file
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    if features:
        logger.info("Skipping regular prediction as per user request.")

        prediction = model.predict(pd.DataFrame([features], columns=FEATURE_NAMES))[0]

        prediction = int(prediction + 0.5)

        return prediction

    logger.info("Performing inference for model...")

    # Read features csv
    features_df = pd.read_csv(features_path)
    # Perform inference
    predictions = model.predict(features_df)

    # # Round the predictions to nearest integer if the target variable is discrete
    # predictions = [round(pred) for pred in predictions]

    # Round the predictions up to nearest integer if the target variable is discrete
    predictions = [int(pred + 0.5) for pred in predictions]

    # Save predictions to csv
    predictions_df = pd.DataFrame(predictions, columns=["prediction"])
    predictions_df.to_csv(predictions_path, index=False)
    

    # Calculate and log basic statistics about predictions
    logger.info(f"Predictions statistics:")
    logger.info(f"Mean: {predictions_df['prediction'].mean()}")
    logger.info(f"Median: {predictions_df['prediction'].median()}")
    logger.info(f"Std: {predictions_df['prediction'].std()}")

    # Compare test_labels with predictions if test_labels are available
    labels_df = pd.read_csv(test_labels_path)
    comparison_df = pd.DataFrame({
        "true_label": labels_df.squeeze(),
        "prediction": predictions_df["prediction"]
    })
    comparison_df["error"] = comparison_df["true_label"] - comparison_df["prediction"]
    mae = comparison_df["error"].abs().mean()
    logger.info(f"Mean Absolute Error (MAE) on test set: {mae}")

    # Compare accuracy if the target variable is discrete
    accuracy = (comparison_df["true_label"] == comparison_df["prediction"]).mean()
    logger.info(f"Accuracy on test set: {accuracy * 100:.2f}%")

    # for i in tqdm(range(10), total=10):
    #     if i == 5:
    #         logger.info("Something happened for iteration 5.")
    logger.success("Inference complete.")
    # -----------------------------------------

    # # Example of saving a single prediction to a file
    # sample_output = model.predict([[8.5,0.28,0.56,1.8,0.092,35.0,103.0,0.9969,3.3,0.75,10.5]])  # Example input
    # # Expected output: array([5.])
    # print(sample_output)

if __name__ == "__main__":
    make_prediction()
