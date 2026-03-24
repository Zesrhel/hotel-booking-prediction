# Hotel Booking Cancellation Prediction

## Dataset and Problem Definition

### Dataset overview
The dataset used is the hotel bookings dataset, containing 119,390 rows and 32 columns, sourced from `data/hotel_bookings.csv`. It includes various features related to hotel bookings.

### Target variable
The target variable is `is_canceled`, a binary variable where 0 indicates the booking was not canceled and 1 indicates it was canceled. The cancellation rate is approximately 37.04%.

### Classification or Regression task
This is a binary classification task aimed at predicting whether a hotel booking will be canceled.

## Data Preparation and Feature Engineering

### Data cleaning
Data cleaning involved removing columns that could cause leakage, such as `reservation_status` and `reservation_status_date`, as they are post-booking outcomes.

### Handling missing values
Missing values were handled by imputing numeric features with the median and categorical features with the most frequent value. The top missing values were: company (94%), agent (14%), country (0.4%), and children (minimal).

### Feature encoding or scaling
Categorical features (10 in total) were one-hot encoded, while numeric features (21 in total) were imputed with median values. No scaling was applied beyond imputation.

### Important features
Feature importance was derived from the Random Forest model, aggregated back to original features. Top features include: country (13.39%), lead_time (9.94%), deposit (9.52%), adr (6.16%), total_of_special_requests (5.41%), and others.

## Predictive Modeling Approaches

### Human-selected model
Logistic Regression was selected as a baseline model due to its interpretability and simplicity.

### AI-recommended model
Random Forest was chosen for its ability to handle non-linear relationships and provide higher predictive accuracy.

### Reason for selecting each model
Logistic Regression was selected for its speed and ease of interpretation, making it suitable for initial baselines. Random Forest was recommended for its robustness to overfitting and better performance on complex datasets.

## Initial Model Training

### Train/test split
The data was split into training and test sets using an 80/20 ratio with stratification to maintain the target distribution.

### Initial model training results
Logistic Regression achieved an ROC-AUC of 0.8886 and accuracy of 80.46%. Random Forest achieved an ROC-AUC of 0.9593 and accuracy of 89.38%.

### Initial evaluation metrics
Evaluation included classification reports, confusion matrices, and ROC curves for both models.

## Model Refinement

### Steps taken to improve performance
To address class imbalance, class_weight parameters were used ("balanced" for Logistic Regression, "balanced_subsample" for Random Forest). Random Forest was tuned with n_estimators=400.

### Example: hyperparameter tuning or feature improvements
Hyperparameter tuning focused on increasing the number of estimators in Random Forest to improve stability and accuracy.

## Evaluation Results

### Final performance metrics
The final model (Random Forest) has an ROC-AUC of 0.9593. Detailed metrics include precision, recall, and F1-score for each class.

### Comparison of models
Random Forest outperforms Logistic Regression across all key metrics, including accuracy and ROC-AUC.

## Final Model and Feature Importance

### Selected final model
The final model selected is Random Forest, chosen based on the highest ROC-AUC score.

### Important features affecting predictions
Key features influencing predictions are country, lead_time, deposit, adr, total_of_special_requests, market, arrival_date_day_of_month, agent, and arrival_date_week_number.

## Business Insights and Deployment

### Key insights for the business
Business insights include that lead time and country are significant predictors of cancellations. Hotels can focus on bookings from high-risk countries or with long lead times to reduce cancellations.

### Possible deployment of the model
The model is saved as `artifacts/hotel_cancellation_model.joblib`. Possible deployments include creating a Flask API for real-time predictions or a Streamlit web app for user interaction.

## How to Run (Deployment + Testing)

### Local Testing

#### Streamlit app (Local)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure the model exists:
   - Run `notebook1.ipynb` to generate `artifacts/hotel_cancellation_model.joblib`
   - Or run: `papermill notebook1.ipynb notebook1_executed.ipynb`
3. Start the app:
   ```bash
   streamlit run app.py
   ```
4. Open http://localhost:8501 in your browser

Notes:
- The app uses a configurable `Decision threshold` slider. If `probability >= threshold`, it predicts `Canceled`.
- You can tune the threshold in the notebook (see the `Threshold tuning` section) to trade off precision vs recall.

#### Validation script (sample input)
Run:
```bash
python validate_sample.py
```

### Deployment to GitHub

1. **Create a new GitHub repository** at https://github.com/new
   - Repository name: `hotel-booking-prediction` (or your preferred name)
   - Add a description: "Hotel booking cancellation predictor with Streamlit web interface"
   - Choose "Public" (to use Streamlit Community Cloud for free)

2. **Clone and push your code:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/hotel-booking-prediction.git
   cd hotel-booking-prediction
   
   # Copy ALL files from the local project
   cp -r ../Predictive_Modeling_v3/* .
   
   # Add all files to git
   git add .
   git commit -m "Initial commit: Hotel booking prediction model with Streamlit app"
   git branch -M main
   git push -u origin main
   ```

3. **Repository structure (should include):**
   - `app.py` — Streamlit web interface
   - `validate_sample.py` — Model validation script
   - `notebook1.ipynb` — Model training notebook
   - `data/hotel_bookings.csv` — Dataset
   - `requirements.txt` — Python dependencies
   - `.gitignore` — Ignored files
   - `.github/workflows/train-model.yml` — GitHub Actions workflow
   - `.streamlit/config.toml` — Streamlit configuration
   - `README.md` — This file

### Deployment to Streamlit Community Cloud 

1. **Sign up for Streamlit Community Cloud** (if you haven't already):
   - Go to https://streamlit.io/cloud
   - Sign in with your GitHub account

2. **Deploy the app:**
   - Click "New app" button
   - Select your GitHub repository: `YOUR_USERNAME/hotel-booking-prediction`
   - Select the main branch
   - Set the main file path to: `app.py`
   - Click "Deploy"

3. **Share your app:**
   - Once deployed, Streamlit provides a public URL like:
     ```
     https://hotel-booking-prediction.streamlit.app
     ```
   - Share this link with anyone to access your live predictor!

4. **Auto-deployment:**
   - Every push to the `main` branch automatically redeploys your app
   - The GitHub Actions workflow runs the notebook to retrain the model on each push

### GitHub Actions (Automated Model Training)

The `.github/workflows/train-model.yml` file automates model training:

- **Trigger:** Runs on every push to `main` branch
- **What it does:**
  1. Sets up Python 3.11 environment
  2. Installs dependencies from `requirements.txt`
  3. Executes `notebook1.ipynb` using papermill
  4. Validates the model with `validate_sample.py`
  5. Uploads the trained model as an artifact

To view workflow status:
- Go to your GitHub repo → **Actions** tab
- See the latest workflow run and logs