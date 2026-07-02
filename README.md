# HR Process Automation Scanner

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![Tableau](https://img.shields.io/badge/Tableau-Dashboard-E97627?logo=tableau)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-success)

### End-to-End Data Analytics & Machine Learning Project

![HR Process Automation Scanner Dashboard](images/dashboard.png)

This project identifies, prioritizes and recommends HR processes with the highest automation potential using data analytics, business rules, machine learning, Tableau and Streamlit.

It transforms operational HR ticket data into a decision-support tool that helps teams understand where automation can generate the highest operational impact.

## Live Demo

Try the application online:

Streamlit App:** Coming soon
---

## Project Overview

HR departments manage thousands of operational requests every day, but not every process should be automated first.

This project combines exploratory data analysis, business rules, feature engineering and machine learning to identify where automation can generate the greatest operational impact.

The final solution includes:

- Interactive Streamlit application
- Machine Learning prediction model
- Business automation scoring
- Executive Tableau dashboard
- Operational decision support

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Tableau |
| Web App | Streamlit |
| Data Processing | Feature Engineering |
| Business | HR Analytics · Process Automation · Decision Support |

---

# Model Performance

| Metric | Value |
|---------|------:|
| Accuracy | **96.83%** |
| Macro F1 Score | **96.85%** |
| Algorithm | Logistic Regression |
| Classes | Alta · Media · Baja |
| Task | Multiclass Classification |

The model predicts the automation priority of HR operational units with high overall performance, making it suitable for decision-support scenarios.

---

## Key Features

- Prioritizes HR processes based on automation potential.
- Predicts automation priority using Machine Learning.
- Estimates operational hours that can be saved.
- Interactive filtering by HR Process, System, Region and Channel.
- Business recommendation engine.
- Executive dashboard for decision makers.

---

## Project Structure

```text
HR-Process-Automation-Scanner
│
├── app/
│   └── Streamlit application
│
├── data/
│   └── Dataset
│
├── images/
│   └── Dashboard screenshots
│
├── models/
│   └── Trained Machine Learning model
│
├── notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_Exploratory_Analysis.ipynb
│   └── 03_Machine_Learning.ipynb
│
├── reports/
│   └── Tableau dashboard
│
├── src/
│   └── Helper functions
│
├── requirements.txt
└── README.md
```

---

## Machine Learning Pipeline

```mermaid
flowchart TD

A[Operational HR Data]
--> B[Data Cleaning]

B --> C[Feature Engineering]

C --> D[Business Rules]

D --> E[Machine Learning Model]

E --> F[Automation Priority Prediction]

F --> G[Technology Recommendation]

G --> H[Estimated Hours Saved]
```

---

# Application Showcase

## Executive Dashboard

The executive dashboard provides an overview of automation opportunities across HR Operations.

- Operational KPIs
- Automation opportunity score
- Estimated hours saved
- Priority distribution
- Top automation candidates

---
## Full Project Showcase

### 1. Executive Dashboard

The executive dashboard provides a high-level overview of automation opportunities across HR Operations, including KPIs, automation scores, priority distribution and estimated operational impact.

![Executive Dashboard](images/dashboard.png)

---

### 2. Automation Opportunity Ranking

This interactive ranking identifies the operational units with the highest automation potential based on business rules and machine learning predictions.

![Automation Ranking](images/ranking.png)

---

### 3. Predictive Simulator

Users can simulate new HR operational scenarios and instantly receive the predicted automation priority, confidence score, technology recommendation and estimated hours saved.

![Predictive Simulator](images/simulator.png)

---

### 4. Project Methodology

This section explains the complete analytical workflow used to build the solution, from business understanding and feature engineering to machine learning and deployment.

![Project Methodology](images/methodology.png)

