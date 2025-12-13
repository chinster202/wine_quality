from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd
import pickle
import xgboost as xgb
# import random forest regressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from src.config import MODELS_DIR, PROCESSED_DATA_DIR, DATA_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    training_features_path: Path = PROCESSED_DATA_DIR / "features.csv",
    training_labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
    data_path: Path = DATA_DIR / "raw" / "WineQT.csv",
    test_features_path: Path = PROCESSED_DATA_DIR / "test_features.csv",
    test_labels_path: Path = PROCESSED_DATA_DIR / "test_labels.csv",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    df = pd.read_csv(data_path)

    # Drop Id column if it exists
    if 'Id' in df.columns:
        df = df.drop(columns=['Id'])

    # Split data into training and test sets
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    training_labels_df = train_df['quality']
    training_features_df = train_df.drop(columns=['quality'])

    # Write features and labels to processed data directory
    training_features_df.to_csv(training_features_path, index=False)
    training_labels_df.to_csv(training_labels_path, index=False)

    test_features_df = test_df.drop(columns=['quality'])
    test_labels_df = test_df['quality']

    test_features_df.to_csv(test_features_path, index=False)
    test_labels_df.to_csv(test_labels_path, index=False)

    # Train a simple RandomForestRegressor model

    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train an XGBoost model

    # model = xgb.XGBRegressor(
    #     objective ='reg:squarederror',
    #     colsample_bytree = 0.3,
    #     learning_rate = 0.1,
    #     max_depth = 5,
    #     alpha = 10,
    #     n_estimators = 100
    # )

    model.fit(training_features_df, training_labels_df)

    logger.info("Training some model...")

    # Save the trained model in a pkl file
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    # for i in tqdm(range(10), total=10):
    #     if i == 5:
    #         logger.info("Something happened for iteration 5.")
    logger.success("Modeling training complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
