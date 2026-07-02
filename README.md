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