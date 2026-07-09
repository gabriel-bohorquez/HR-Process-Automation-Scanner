# PROJECT_FACTS — HR Process Automation Scanner

## 1. Project Identity

**Official name:** HR Process Automation Scanner

**Category:** Data Analytics · Machine Learning · HR Operations · Process Automation

**Project type:** End-to-end analytical prototype for prioritizing automation opportunities.

**Primary users:** HR Operations teams, People Analytics teams, Digital Transformation teams, and automation decision-makers.

**Business problem:** Organizations manage large volumes of operational tickets, but they do not always have an objective framework to determine which processes should be automated first.

**Decision supported:** Prioritize HR Operations units according to their automation potential.

**Final solution:** An integrated solution combining data analysis, an Automation Opportunity Score, a Machine Learning model, a Tableau dashboard, and a Streamlit application.

## 2. Dataset and Provenance

**Original dataset:** Public customer support ticket dataset.

**Data nature:** Public support-ticket data conceptually adapted to an HR Operations use case.

**Original record count:** 200,000 tickets.

**Final operational units:** 3,000.

**Time period:** Not reliably documented in the original dataset.

**License:** Apache License 2.0.

**Source platform:** Kaggle.

**Dataset title:** Customer Support Tickets Dataset (200K+ Records).

**Dataset author:** Mirza Yasir Abdullah.

**Source URL:** https://www.kaggle.com/datasets/mirzayasirabdullah07/customer-support-tickets-dataset-200k-records

**Primary dataset used for analysis and modeling:** `customer_support_tickets_200k.csv`

**Secondary dataset reviewed:** `customer_support_tickets.csv` — used only for comparison and backup purposes; not used to train the final model.

**Complementary process dataset reviewed:** `helpdesk_event_log.csv` — used to understand ticket-process structure; not used to train the final model.

**Dataset integration statement:** The three raw datasets were not merged. The final analytical workflow was built from `customer_support_tickets_200k.csv`.

**Adaptation performed:** The original support-ticket fields were reinterpreted to represent HR processes, HR systems, regions, internal contact channels, operational complexity, SLA pressure, and automation potential.

**Methodological warning:** The dataset does not come from a real HR Operations environment. Therefore, the project must be presented as an analytical prototype rather than as a solution validated with real enterprise HR data.

### Raw Data Quality Summary

- Dataset dimensions: `200,000` rows and `30` columns.
- Exact duplicate rows: `0`.
- Missing values: `40,023` missing values in the original `browser` field.
- Missing-value rate in `browser`: approximately `20.01%`.
- The `browser` field was not used in the final prioritization model.
- No other missing values were identified in the raw dataset.
- Numeric variables were found within plausible source ranges.
- `ticket_created_date` and `ticket_resolved_date` were originally stored as text and were converted to datetime during data preparation.
- The raw dataset was preserved without overwriting.

## 3. Data Transformation and Feature Engineering

**Original analytical level:** Individual support tickets.

**Final analytical level:** HR operational units.

**Operational unit definition:** A unique combination of HR process, HR system, region, and internal contact channel.

**Main conceptual transformations:**

* `product` → HR system
* `category` → HR process
* `channel` → internal HR contact channel
* `priority` → case priority
* `satisfaction_score` → employee satisfaction score
* `complexity_score` → process complexity score

**Data-quality steps performed:**

* Standardization of column names
* Review of missing values
* Review of duplicated records
* Validation of data types
* Standardization of categorical values
* Removal of fields not relevant to automation prioritization

**Main engineered variables:**

* `automation_score`
* `automation_priority`
* `recommended_solution`
* `estimated_operational_hours_saved`
* Operational-unit identifier

**Business logic applied:** Higher ticket volume, longer resolution times, greater SLA pressure, more escalations, higher operational complexity, and greater process repetition were treated as signals of higher automation potential.

**Important limitation:** These transformations represent a business-oriented reinterpretation of the original support-ticket data. They do not convert the source into genuine HR operational data.

## 4. Target Definition and Prioritization Logic

**Target variable:** `automation_priority`

**Target type:** Multiclass classification target.

**Target classes:**

- `Alta`
- `Media`
- `Baja`

**Target construction:** The target was not provided by the original dataset. It was created from the `automation_score`, which was itself derived from operational variables and business rules.

**Automation Opportunity Score inputs:**

* Case volume
* Average resolution time
* Average first-response time
* SLA breach rate
* Escalation rate
* Process complexity
* Previous-case volume
* High-priority case rate
* Urgent-priority case rate

**Prioritization rule:** Operational units with higher automation scores were assigned a higher automation priority.

**Final score thresholds:**

- `Baja`: automation score below `46.0075`
- `Media`: automation score from `46.0075` up to, but not including, `52.92`
- `Alta`: automation score equal to or above `52.92`

**Final class distribution:**

- `Baja`: `750` operational units (`25.0%`)
- `Media`: `1,497` operational units (`49.9%`)
- `Alta`: `753` operational units (`25.1%`)

**Relative classification warning:** These classes are defined using the 25th and 75th percentiles of the current dataset. Therefore, priority is relative to the analyzed population and should not be interpreted as a universal business threshold.

**Business interpretation:

* Alta: Strong automation potential and higher expected operational impact
* Media: Partial or progressive automation potential
* Baja: Limited immediate automation potential or a greater need for human review

**Critical methodological warning:** The target is business-rule-derived rather than externally observed. The Machine Learning model therefore learns to reproduce an existing prioritization policy; it does not independently validate whether an automation initiative will succeed in a real organization.

**Circularity risk:** Because the target and the predictive features originate from closely related operational signals, high model performance is expected. This must be disclosed whenever the model metrics are presented.

## 5. Model Development and Validation

**Machine Learning task:** Multiclass classification.

**Objective:** Predict the automation-priority class of new HR operational units.

**Models evaluated:**

* Logistic Regression
* Decision Tree
* Random Forest
* Gradient Boosting

**Train-test split:** 80% training and 20% testing.

**Split strategy:** Stratified random split to preserve the class distribution across training and test sets.

**Random state:** `42`

**Primary evaluation metric:** Macro F1 score.

**Metric rationale:** Macro F1 was selected because it evaluates performance across all three classes without allowing the most frequent class to dominate the final result.

**Selected model:** Logistic Regression.

**Verified serialized-model configuration:**

- scikit-learn version: `1.6.1`
- Estimator: `LogisticRegression`
- Regularization strength (`C`): `1.0`
- Penalty: `l2`
- Solver: `lbfgs`
- Multiclass handling: multinomial classification through the `lbfgs` solver; the legacy `multi_class` parameter appears as deprecated in scikit-learn `1.6.1`.
- Maximum iterations: `1000`
- Class weighting: `None`
- Random state parameter: `42` — stored in the estimator configuration, although it does not affect the deterministic `lbfgs` solver.
- Learned classes: `Alta`, `Baja`, `Media`
- Coefficient matrix shape: `(3, 42)`
- Intercept vector shape: `(3,)`

**Interpretation:** The final pipeline expands the original features into 42 model inputs after preprocessing and one-hot encoding.

**Final test metrics:**

* Accuracy: `0.9683`
* Macro precision: `0.9681`
* Macro recall: `0.9689`
* Macro F1 score: `0.9685`

**Model-selection criterion:** Highest Macro F1 score among the evaluated models.

**Interpretation:** The selected model correctly classifies approximately 97 out of every 100 operational units in the test set and performs consistently across the `Alta`, `Media`, and `Baja` classes.

**Important methodological interpretation:** These metrics measure how accurately the model reproduces the business-rule-derived prioritization logic. They do not demonstrate that the predicted priority will lead to successful automation outcomes in a real organization.

**Overfitting risk:** Limited evidence of overfitting was observed in the reported test performance, but the model must still be validated with independent real-world HR Operations data before any production use.

**Decision threshold:** No custom probability threshold was applied. The predicted class was selected using the model’s highest estimated class probability.

## 6. Production Features, Exclusions, and Leakage Control

**Predictive feature groups:**

* HR process
* HR system
* Region
* Internal contact channel
* Total case volume
* Average resolution time
* Average first-response time
* SLA breach rate
* Escalation rate
* Average process-complexity score
* Average employee-satisfaction score
* Average number of previous cases
* Average employee tenure
* High-priority case rate
* Urgent-priority case rate

**Verified production features from the serialized pipeline:**

**Numeric features:**

* `total_cases`
* `avg_resolution_time_hours`
* `avg_first_response_time_hours`
* `sla_breach_rate`
* `escalation_rate`
* `avg_complexity_score`
* `avg_satisfaction_score`
* `avg_previous_cases`
* `avg_employee_tenure_months`
* `high_priority_rate`
* `urgent_priority_rate`

**Categorical features:**

* `hr_process_name`
* `hr_system_name`
* `hr_contact_channel`
* `region`

**Verification result:** The serialized production pipeline does not include `automation_score`, `automation_priority`, `recommended_solution`, `ranking`, or savings-related outputs as predictors.

**Variables excluded from model training:**

* `automation_priority`
* `automation_score`
* `ranking`
* `recommended_solution`
* `estimated_operational_hours_saved`
* `estimated_manual_handling_time_hours`
* `estimated_savings_rate`
* Operational-unit identifier

**Reason for exclusion:** These variables are either the target itself, direct outputs of the prioritization logic, downstream business recommendations, or identifiers with no valid predictive meaning.

**Direct target leakage:** No direct target leakage was identified from including the target or obvious downstream outputs in the feature matrix.

**Conceptual circularity:** A methodological circularity remains because the target and several predictive features originate from the same operational logic used to construct the Automation Opportunity Score.

**Temporal availability:** The predictive variables are intended to represent information available before assigning an automation priority. However, this assumption should be validated with real operational timestamps before production use.

**Production inference requirement:** Any new operational unit must provide the same variables, naming conventions, units, and preprocessing structure used during model training.

**Risk statement:** The model should be treated as a policy-replication and decision-support tool, not as an independently validated predictor of automation success.

## 7. Business Rules, Recommended Solutions, and Savings Estimate

**Recommended solution variable:** `recommended_solution`

**Recommendation method:** Rule-based business logic applied after the automation-priority classification.

**Possible recommendation types:**

* Workflow automation
* Chatbot or virtual assistant
* Partial automation
* SLA alerts and partial automation
* AI-assisted processing with human review
* Process redesign before automation
* Human review
* Low automation priority

**Recommendation inputs:**

* Automation priority
* Process complexity
* SLA breach rate
* Internal contact channel

**Important distinction:** The Machine Learning model predicts the automation-priority class. The recommended technological solution is generated separately through business rules.

**Estimated savings variable:** `estimated_operational_hours_saved`

**Savings purpose:** Translate the prioritization results into an operational-efficiency estimate that is easier for business stakeholders to interpret.

**General calculation logic:**

1. Estimate the manual-handling portion of the average resolution time.
2. Apply a savings rate according to the assigned automation-priority class.
3. Multiply the estimated time saved per case by the total case volume.

**Reported total estimated savings:** `739,372` operational hours.

**Critical limitation:** This figure is a scenario-based analytical estimate, not a measured or realized business outcome.

**Required interpretation:** The estimated hours represent theoretical potential under the assumptions embedded in the calculation. They should not be presented as verified savings, financial return, or guaranteed operational impact.

**Time-horizon limitation:** The source dataset does not provide a reliably documented business time horizon. Therefore, the total estimated hours must not be described as annual savings unless an annual period is independently verified.

**Production validation required:** In a real organization, the estimate should be recalibrated using observed handling times, process-level automation rates, implementation costs, exception rates, employee capacity, and realized post-implementation savings.

## 8. Production Artifacts and Application Layer

**Production model artifact:** Serialized Logistic Regression pipeline stored in the `models/` directory.

**Application:** Streamlit application located in `app/app.py`.

**Dashboard:** Tableau workbook used for executive reporting and opportunity prioritization.

**Production dataset:** `data/final/hr_process_automation_ranking_clean.csv`

**Tableau dataset:** `data/final/tableau_hr_automation_dashboard.csv`

**Reusable code module:** `src/hr_automation_utils.py`

**Current application capabilities:**

* Display executive KPIs
* Filter operational units
* Explore automation opportunities
* Review rankings by process, system, region, and channel
* Simulate a new operational unit
* Predict automation priority
* Display model confidence
* Recommend an automation approach
* Estimate potential operational savings

**Product role:** The application converts the analytical workflow into an interactive decision-support prototype for HR Operations.

**Decision-support warning:** The application should support human judgment, not replace it. Final automation decisions require operational validation, stakeholder review, technical feasibility assessment, and cost-benefit analysis.

**Current integration risk:** The reusable logic in `src/hr_automation_utils.py`, the notebooks, and the Streamlit application must remain fully aligned. Any duplicated scoring, recommendation, or savings logic creates a risk of inconsistent results.

**Production-readiness limitation:** The application is a portfolio prototype. It has not been validated against live HR systems, real-time ticketing data, enterprise security requirements, or production monitoring standards.

## 9. Limitations, Allowed Claims, and Prohibited Claims

### Main Limitations

* The source data comes from a public customer-support dataset rather than a real HR Operations environment.
* The HR context was created through conceptual adaptation and business-oriented reinterpretation.
* The target variable was derived from the Automation Opportunity Score instead of being externally observed.
* The model therefore reproduces a prioritization policy rather than independently predicting automation success.
* The reported savings are scenario-based estimates and not measured business outcomes.
* The dataset does not provide a reliably documented operational time horizon.
* The model has not been validated with live HRIS, ticketing, payroll, benefits, or employee-support data.
* No causal relationship between automation priority and realized operational improvement has been established.
* Production use would require security, privacy, governance, monitoring, and stakeholder validation.

### Allowed Claims

The project may be described as:

* An end-to-end analytical prototype for prioritizing automation opportunities in HR Operations.
* A decision-support solution combining business rules, Machine Learning, Tableau, and Streamlit.
* A model that reproduces a business-rule-derived prioritization logic with high internal test performance.
* A framework for classifying new operational units into `Alta`, `Media`, and `Baja` automation-priority categories.
* A portfolio project demonstrating data transformation, feature engineering, model comparison, dashboarding, and application development.
* A scenario-based tool for estimating potential operational savings under explicit assumptions.

### Prohibited or Misleading Claims

The project must not be described as:

* A model trained on real enterprise HR Operations data.
* A validated predictor of automation success.
* A system that guarantees cost reduction, productivity gains, or SLA improvement.
* A solution that has generated `739,372` verified or realized hours of savings.
* A production-ready enterprise HR automation platform.
* A causal model proving that a specific process should be automated.
* An autonomous decision-maker that replaces operational or managerial judgment.
* A commercially validated product unless future evidence supports that statement.

### Approved Summary Statement

> HR Process Automation Scanner is an end-to-end analytical prototype that adapts public support-ticket data to an HR Operations use case, applies business rules to prioritize automation opportunities, and uses Machine Learning to scale that prioritization logic through an interactive decision-support application.

## 10. Verified Outputs, Insights, and Next Steps

### Verified Outputs

The project currently includes:

* Three analytical notebooks
* A processed production dataset
* A reduced Tableau dataset
* A serialized Machine Learning pipeline
* A Tableau executive dashboard
* A Streamlit decision-support application
* A reusable Python utilities module
* A professional README
* A presentation deck and demo workflow

### Verified Analytical Results

* Original records: `200,000`
* Final operational units: `3,000`
* Average Automation Opportunity Score: `49.44`
* Estimated potential operational hours saved: `739,372`
* Selected model: Logistic Regression
* Accuracy: `0.9683`
* Macro precision: `0.9681`
* Macro recall: `0.9689`
* Macro F1 score: `0.9685`

### Main Analytical Insights

* Automation potential is not determined by volume alone.
* Resolution time, SLA pressure, escalation rate, complexity, and repetition provide additional operational context.
* The operational-unit level offers more actionable prioritization than process-level analysis alone.
* Simple and interpretable models can be sufficient when the target follows structured business rules.
* The strongest project value comes from the complete decision-support workflow rather than from model complexity alone.

### Next Recommended Improvements

1. Validate the framework using real HR Operations or ticketing data.
2. Replace the rule-derived target with an independently observed business outcome where possible.
3. Recalibrate savings assumptions using real handling times, automation rates, and implementation costs.
4. Add process-level ROI and implementation-effort estimates.
5. Integrate the reusable logic in `src/` directly into the notebooks and Streamlit application.
6. Add automated tests for scoring, prediction, recommendations, and savings calculations.
7. Validate reproducibility in a clean environment.
8. Add model and data monitoring before any production deployment.
9. Introduce NLP features from ticket descriptions if real text data becomes available.
10. Review fairness, privacy, and governance requirements for real employee-related data.

### Primary Future Validation Goal

The highest-priority future improvement is to validate the prioritization framework against real operational decisions and realized automation outcomes.
