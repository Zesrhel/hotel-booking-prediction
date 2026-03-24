import os

import joblib
import pandas as pd
import requests
import streamlit as st


ARTIFACT_PATH = os.path.join("artifacts", "hotel_cancellation_model.joblib")
DATA_PATH = os.path.join("data", "hotel_bookings.csv")

@st.cache_resource
def load_model():
    if not os.path.exists(ARTIFACT_PATH):
        raise FileNotFoundError(
            f"Model artifact not found at '{ARTIFACT_PATH}'. Run notebook1.ipynb to generate it."
        )
    return joblib.load(ARTIFACT_PATH)


@st.cache_data
def load_schema_columns():
    # Hardcoded to match the exact columns used during model training
    return [
        "lead_time",
        "arrival_date_month",
        "arrival_date_week_number",
        "arrival_date_day_of_month",
        "stays_in_weekend_nights",
        "stays_in_week_nights",
        "market_segment",
        "distribution_channel",
        "previous_cancellations",
        "total_nights",
        "person",
        "adults",
        "previous_bookings_not_canceled",
        "arrival_date_year",
        "is_repeated_guest",
    ]


def build_input_row(schema_cols: list[str], raw: dict) -> pd.DataFrame:
    row = {c: pd.NA for c in schema_cols}
    for k, v in raw.items():
        if k in row:
            row[k] = v

    stays_wkend = float(raw.get("stays_in_weekend_nights", 0) or 0)
    stays_week = float(raw.get("stays_in_week_nights", 0) or 0)
    row["total_nights"] = stays_wkend + stays_week

    person = float(raw.get("person", 0) or 0)
    row["person"] = person

    # Provide defaults for columns that were dropped but model expects
    row["adults"] = person  # Assume adults = person since babies/children are 0
    row["previous_bookings_not_canceled"] = 0
    row["arrival_date_year"] = 2016  # Arbitrary default
    row["is_repeated_guest"] = 0

    return pd.DataFrame([row], columns=schema_cols)


st.set_page_config(page_title="Hotel Cancellation Prediction", layout="centered")

st.title("Hotel Booking Cancellation Prediction")

model = load_model()
schema_cols = load_schema_columns()

with st.sidebar:
    st.header("Inputs")

    decision_threshold = st.slider(
        "Decision threshold",
        min_value=0.05,
        max_value=0.95,
        value=0.50,
        step=0.05,
        help="If predicted probability >= threshold, the app predicts 'Canceled'.",
    )

    lead_time = st.number_input("Lead time (days)", min_value=0, max_value=1000, value=50)

    arrival_date_month = st.selectbox(
        "Arrival month",
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        index=6,
    )
    arrival_date_week_number = st.number_input("Arrival week number", min_value=1, max_value=53, value=27)
    arrival_date_day_of_month = st.number_input("Arrival day of month", min_value=1, max_value=31, value=1)

    stays_in_weekend_nights = st.number_input("Weekend nights", min_value=0, max_value=30, value=1)
    stays_in_week_nights = st.number_input("Week nights", min_value=0, max_value=30, value=2)

    person = st.number_input("Number of people", min_value=1, max_value=20, value=2)

    previous_cancellations = st.number_input("Previous cancellations", min_value=0, max_value=50, value=0)

raw_inputs = {
    "lead_time": lead_time,
    "arrival_date_month": arrival_date_month,
    "arrival_date_week_number": arrival_date_week_number,
    "arrival_date_day_of_month": arrival_date_day_of_month,
    "stays_in_weekend_nights": stays_in_weekend_nights,
    "stays_in_week_nights": stays_in_week_nights,
    "person": person,
    "market_segment": "Online TA",  # Default hidden value
    "distribution_channel": "TA/TO",  # Default hidden value
    "previous_cancellations": previous_cancellations,
}

X_input = build_input_row(schema_cols, raw_inputs)

st.subheader("Prediction")

if st.button("Predict"):
    proba = float(model.predict_proba(X_input)[:, 1][0])
    pred = int(proba >= float(decision_threshold))

    st.metric("Cancellation probability", f"{proba:.3f}")
    st.write(f"Decision threshold: {float(decision_threshold):.2f}")

    if pred == 1:
        st.error("Predicted: Canceled")
    else:
        st.success("Predicted: Not Canceled")


st.caption("Model: artifacts/hotel_cancellation_model.joblib")
