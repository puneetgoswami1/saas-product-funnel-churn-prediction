# SaaS Product Funnel & Churn Prediction System

An end-to-end product analytics and user retention engine designed to diagnose activation bottlenecks and predict B2B SaaS account churn before renewal windows.

## Overview
Customer acquisition in subscription software is heavily eroded when accounts churn within the first year. This system combines product milestone tracking (activation funnel) with behavioral machine learning models to identify accounts exhibiting disengagement signals.

## Project Structure
- `funnel_dropoff_analysis.sql`: Multi-step conversion SQL query tracking drop-offs from signup to paid conversion.
- `churn_prediction_engine.py`: Machine learning pipeline training a Random Forest classifier on telemetry metrics (seat usage, active days, ticket escalations).
- `requirements.txt`: Python dependencies.

## Key Insights & Metrics
1. **Activation Bottlenecks:** Measures step-by-step conversion across key milestones (`Signup -> Workspace Setup -> Team Invite -> Core Activation -> Paid Tier`).
2. **Telemetry Churn Drivers:** Pinpoints disengagement signals—identifying low license seat utilization (<40%) and sharp drops in monthly active days as the highest-weight leading indicators of churn.
3. **Proactive Intervention:** Generates probability risk scores enabling Customer Success teams to trigger targeted onboarding interventions before quarterly renewals.

## How to Run

```bash
# Clone the repository
git clone [https://github.com/puneetgoswami1/saas-product-funnel-churn-prediction.git](https://github.com/puneetgoswami1/saas-product-funnel-churn-prediction.git)
cd saas-product-funnel-churn-prediction

# Install requirements
pip install -r requirements.txt

# Run churn engine
python churn_prediction_engine.py