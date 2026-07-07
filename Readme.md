# 🏦 Default Risk Platform

> **An Explainable AI Platform for Probability of Default (PD) Prediction and Credit Risk Assessment**

A proof-of-concept platform that predicts the **Probability of Default (PD)** for Retail and SME borrowers using machine learning, converts the prediction into a standardized credit score, and explains every prediction using SHAP-based explainability.

---

## 📌 Problem Statement

Traditional credit risk assessment often relies on fragmented models, manual underwriting, and limited interpretability. Financial institutions require a scalable solution that can:

* Predict borrower default risk.
* Support multiple borrower segments.
* Provide consistent and explainable decisions.
* Serve as a foundation for future document-driven credit underwriting.

This project demonstrates that foundation through an end-to-end explainable credit risk platform.

| Capability                              | Current PoC | Production Vision |
| --------------------------------------- | ----------- | ----------------- |
| Retail PD Prediction                    | ✅           | ✅                 |
| SME PD Prediction                       | ✅           | ✅                 |
| Credit Scorecard                        | ✅           | ✅                 |
| SHAP Explainability                     | ✅           | ✅                 |
| Recommendation Engine                   | ✅           | ✅                 |
| Structured Data                         | ✅           | ✅                 |
| Document Upload (OCR)                   | 🔄 Planned  | ✅                 |
| Bank Statement Analysis                 | 🔄 Planned  | ✅                 |
| GST & Financial Statement Parsing       | 🔄 Planned  | ✅                 |
| Institution-specific 12-month PD Models | 🔄 Planned  | ✅                 |
| Multi-segment MSME Portfolio Monitoring | 🔄 Planned  | ✅                 |

---

## 🚀 Features

### Retail Credit Risk

* Manual borrower information entry
* Probability of Default prediction
* Credit Score generation
* Risk Tier classification
* Recommendation engine
* SHAP-based explainability

### SME Credit Risk

* CSV upload containing company financial ratios
* Bankruptcy probability prediction
* Credit Score generation
* Risk Tier classification
* Recommendation engine
* SHAP-based explainability

---

## 🏗 System Architecture

```
                     User Input
                         │
         ┌───────────────┴───────────────┐
         │                               │
     Retail Form                  SME CSV Upload
         │                               │
         └───────────────┬───────────────┘
                         │
                  Prediction Engine
                         │
          ┌──────────────┼──────────────┐
          │              │              │
      XGBoost       Calibration      Scorecard
          │              │              │
          └──────────────┼──────────────┘
                         │
             Probability of Default
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     Credit Score   Risk Tier      SHAP Explainability
                         │
                  Recommendation Engine
                         │
                    Gradio Interface
```

---

## 🧠 Machine Learning Pipeline

### Data Preparation

* Missing value handling
* Feature selection
* Train/Test split

### Model Development

Baseline:

* Logistic Regression

Production Model:

* XGBoost Classifier

### Calibration

Raw model probabilities are calibrated using **Isotonic Regression** to improve probability estimation.

### Credit Scorecard

Calibrated probabilities are transformed into an industry-style credit score using a configurable scorecard.

### Explainability

Predictions are interpreted using **SHAP (SHapley Additive exPlanations)** and mapped into business-friendly reason codes.

---

## 📊 Datasets

### Dataset A — Retail

**Give Me Some Credit (Kaggle)**

Consumer credit dataset used for retail default prediction.

Features include:

* Revolving utilization
* Monthly income
* Debt ratio
* Payment history
* Credit lines
* Dependents

---

### Dataset B — SME

**Company Bankruptcy Prediction (Taiwan Economic Journal)**

Corporate financial dataset containing nearly 100 financial indicators including:

* Profitability ratios
* Liquidity ratios
* Cash flow indicators
* Leverage ratios
* Asset turnover
* Solvency metrics

Used as a proxy for SME credit risk prediction.

---

## 📈 Model Performance

### Retail

| Model               |       AUC |      Gini |        KS |
| ------------------- | --------: | --------: | --------: |
| Logistic Regression |     0.800 |     0.601 |     0.447 |
| **XGBoost**         | **0.869** | **0.738** | **0.579** |

---

### SME

| Model               |       AUC |      Gini |        KS |
| ------------------- | --------: | --------: | --------: |
| Logistic Regression |     0.847 |     0.694 |     0.616 |
| **XGBoost**         | **0.954** | **0.908** | **0.798** |

---

## 💡 Explainability

Instead of only predicting default risk, the platform explains **why** a prediction was made.

Example output:

* Leverage / Utilization
* Payment History
* Structural / Demographic

This enables transparent and interpretable credit decisions.

---

## 🛠 Tech Stack

### Machine Learning

* Python
* XGBoost
* Scikit-learn
* SHAP
* Pandas
* NumPy

### Application

* Gradio

### Model Persistence

* Joblib

---

## 📂 Project Structure

```
default-risk-platform/

├── app.py
├── engine.py
├── predictor.py
├── explainability.py
├── loaders.py
├── scoring.py
├── models/
├── samples/
├── tests/
└── README.md
```

---

## ▶ Running Locally

Clone the repository:

```bash
git clone <repository-url>
cd default-risk-platform
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

The application will be available at:

```
http://127.0.0.1:7860
```

---

## 🔮 Production Roadmap

This repository demonstrates the core prediction engine using public benchmark datasets.

Future iterations will extend the platform to support:

* OCR-based document ingestion
* AI extraction from bank statements
* Financial statement parsing
* GST and invoice analysis
* 12-month institution-specific PD models trained on proprietary lending portfolios
* Automated underwriting workflows
* API-first deployment

The prediction engine is intentionally designed to remain reusable while the data ingestion layer evolves.


## 🚀 Future Scope

This repository demonstrates the **core explainable Probability of Default (PD) engine** using publicly available benchmark datasets. The long-term vision is to evolve this proof of concept into an enterprise-grade MSME credit intelligence platform.

### 📄 Intelligent Document Processing

Instead of manually entering borrower information or uploading preprocessed CSVs, the platform will ingest real-world financial documents such as:

* Bank Statements
* GST Returns
* Balance Sheets
* Profit & Loss Statements
* Income Tax Returns
* Invoice Records
* Loan Statements

These documents will be processed using OCR and AI-powered information extraction to automatically generate the required structured financial features.

```
Documents
        │
        ▼
 OCR + AI Extraction
        │
        ▼
Structured Features
        │
        ▼
Existing Prediction Engine
```

---

### 🏦 Institution-Specific 12-Month Default Prediction

The current proof of concept validates the prediction architecture using benchmark public datasets.

In production, the same pipeline would be retrained on institution-specific historical MSME lending data where the target variable is explicitly defined as:

> **"Will this borrower default within the next 12 months?"**

This enables true forward-looking stress prediction aligned with business requirements while preserving the existing prediction engine and explainability framework.

---

### 🏭 Unified MSME Risk Engine

The platform is designed to support multiple MSME borrower segments using a common interpretation framework, including:

* Manufacturing
* Trading
* Services
* Agriculture
* Micro Enterprises
* Small Enterprises
* Medium Enterprises

Each segment can leverage specialized prediction models while producing standardized Probability of Default estimates, credit scores, and explainable risk drivers.

---

### 🤖 AI-Assisted Credit Decisioning

Future versions will extend beyond prediction by assisting credit officers with contextual recommendations, including:

* Automated underwriting recommendations
* Collateral requirement suggestions
* Loan amount recommendations
* Risk-based pricing strategies
* Manual review prioritization
* Portfolio stress monitoring

The objective is to transform the platform from a prediction engine into a comprehensive AI-assisted credit decision support system.

---

### 📊 Continuous Learning Pipeline

Future releases will include:

* Periodic model retraining
* Performance monitoring
* Model drift detection
* Threshold optimization
* Portfolio analytics dashboards
* Regulatory reporting support

This ensures the platform continuously adapts to evolving borrower behavior and macroeconomic conditions while maintaining prediction reliability.

---

### ☁ Enterprise Deployment

The production architecture can evolve into:

```
Financial Documents / APIs
             │
             ▼
      OCR + AI Extraction
             │
             ▼
      Feature Engineering
             │
             ▼
    Explainable ML Engine
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
 Probability  Score   SHAP
     │
     ▼
Decision Support Engine
     │
     ▼
Banking Applications / APIs
```

This separation between data ingestion and prediction allows the same explainable ML engine to be reused across multiple lending products while supporting both structured and unstructured financial data.


---

## ⚠ Disclaimer

This project is a proof of concept built using publicly available benchmark datasets.

The datasets are used to validate the prediction pipeline, explainability framework, and scorecard methodology. Production deployment would require retraining on institution-specific historical lending data and business policy calibration.

---

## 👨‍💻 Author

**Deepak Grandhi**

Built as an end-to-end proof of concept demonstrating explainable AI for credit risk assessment.
