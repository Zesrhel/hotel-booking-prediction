import os

import joblib
import pandas as pd


ARTIFACT_PATH = os.path.join("artifacts", "hotel_cancellation_model.joblib")
DATA_PATH = os.path.join("data", "hotel_bookings.csv")


def make_features(df: pd.DataFrame) -> pd.DataFrame:
    feature_df = df.drop(columns=["is_canceled"], errors="ignore")
    feature_df = feature_df.drop(columns=["reservation_status", "reservation_status_date"], errors="ignore")

    feature_df["total_nights"] = (
        feature_df.get("stays_in_weekend_nights", 0).fillna(0)
        + feature_df.get("stays_in_week_nights", 0).fillna(0)
    )
    feature_df["party_size"] = (
        feature_df.get("adults", 0).fillna(0)
        + feature_df.get("children", 0).fillna(0)
        + feature_df.get("babies", 0).fillna(0)
    )

    return feature_df


def main():
    if not os.path.exists(ARTIFACT_PATH):
        raise FileNotFoundError(
            f"Model artifact not found at '{ARTIFACT_PATH}'. Run notebook1.ipynb to generate it."
        )

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at '{DATA_PATH}'.")

    model = joblib.load(ARTIFACT_PATH)

    df = pd.read_csv(DATA_PATH)
    sample_row = df.sample(1, random_state=42)

    X_sample = make_features(sample_row)

    proba = float(model.predict_proba(X_sample)[:, 1][0])
    pred = int(proba >= 0.5)

    print("Sample input (1 row):")
    print(X_sample.T.head(40))
    print()
    print(f"Predicted cancellation probability: {proba:.4f}")
    print("Predicted class:", "Canceled" if pred == 1 else "Not Canceled")


if __name__ == "__main__":
    main()
