"""
Funciones reutilizables para el proyecto HR Process Automation Scanner.

Este módulo concentra la lógica repetible utilizada en los notebooks:

1. Carga e inspección de datos.
2. Adaptación de tickets genéricos a HR Operations.
3. Creación de unidades operativas.
4. Cálculo del Automation Opportunity Score.
5. Clasificación de prioridad y recomendación tecnológica.
6. Estimación de horas operativas ahorrables.
7. Creación de rankings y resúmenes ejecutivos.
8. Preparación, entrenamiento y evaluación de modelos de Machine Learning.

Autor: Gabriel Bohorquez Correa
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


# ---------------------------------------------------------------------------
# CONSTANTES DEL PROYECTO
# ---------------------------------------------------------------------------

COLUMN_RENAME_MAP: dict[str, str] = {
    "ticket_id": "case_id",
    "product": "hr_system",
    "category": "hr_process",
    "issue_description": "case_description",
    "priority": "case_priority",
    "status": "case_status",
    "channel": "contact_channel",
    "customer_tenure_months": "employee_tenure_months",
    "previous_tickets": "previous_cases",
    "customer_satisfaction_score": "employee_satisfaction_score",
    "issue_complexity_score": "process_complexity_score",
    "customer_segment": "employee_segment",
}

COLUMNS_TO_DROP: tuple[str, ...] = (
    "customer_name",
    "customer_email",
    "customer_age",
    "customer_gender",
    "operating_system",
    "browser",
    "payment_method",
)

HR_PROCESS_MAPPING: dict[str, str] = {
    "Feature Request": "HR System Enhancement Request",
    "Subscription Cancellation": "Benefits Cancellation Request",
    "Performance Issue": "HR System Performance Issue",
    "Security Concern": "Compliance & Access Security Review",
    "Login Issue": "HRIS Login Issue",
    "Payment Problem": "Payroll Support Request",
    "Bug Report": "HR Platform Bug Report",
    "Refund Request": "Benefits Reimbursement Request",
    "Data Sync Issue": "Employee Data Update",
    "Account Suspension": "HRIS Access Suspension",
}

HR_SYSTEM_MAPPING: dict[str, str] = {
    "Billing System": "Payroll System",
    "CRM Platform": "HR Case Management Platform",
    "E-commerce Store": "Benefits Portal",
    "Cloud Storage": "HR Document Management System",
    "Mobile App": "Employee Mobile App",
    "Analytics Dashboard": "People Analytics Dashboard",
    "Web Portal": "Employee Self-Service Portal",
    "Payment Gateway": "Payroll Payment Gateway",
    "Subscription Service": "Benefits Administration System",
    "API Service": "HRIS Integration API",
}

AUTOMATION_SCORE_WEIGHTS: dict[str, float] = {
    "volume_score": 0.20,
    "resolution_time_score": 0.15,
    "sla_risk_score": 0.15,
    "escalation_score": 0.10,
    "complexity_score": 0.10,
    "first_response_score": 0.10,
    "previous_cases_score": 0.05,
    "high_priority_score": 0.075,
    "urgent_priority_score": 0.075,
}

SAVINGS_RATE_MAPPING: dict[str, float] = {
    "Alta": 0.35,
    "Media": 0.20,
    "Baja": 0.05,
}

MANUAL_WORK_RATE_MAPPING: dict[str, float] = {
    "Alta": 0.18,
    "Media": 0.12,
    "Baja": 0.08,
}


# ---------------------------------------------------------------------------
# 1. CARGA E INSPECCIÓN
# ---------------------------------------------------------------------------

def load_csv(file_path: str | Path, **read_csv_kwargs: Any) -> pd.DataFrame:
    """
    Carga un archivo CSV y devuelve un DataFrame.

    Raises
    ------
    FileNotFoundError
        Si la ruta no existe.
    ValueError
        Si el archivo está vacío.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    df = pd.read_csv(path, **read_csv_kwargs)

    if df.empty:
        raise ValueError(f"El archivo está vacío: {path}")

    return df


def inspect_dataset(
    file_path: str | Path,
    nrows: int = 5,
    **read_csv_kwargs: Any,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Carga un CSV y genera un resumen estructurado de calidad de datos.

    Returns
    -------
    tuple[pd.DataFrame, dict]
        DataFrame cargado y diccionario con dimensiones, tipos y nulos.
    """
    df = load_csv(file_path, **read_csv_kwargs)

    summary = {
        "file_name": Path(file_path).name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "preview": df.head(nrows).copy(),
    }

    return df, summary


# ---------------------------------------------------------------------------
# 2. ADAPTACIÓN DEL DATASET A HR OPERATIONS
# ---------------------------------------------------------------------------

def _to_binary_flag(series: pd.Series) -> pd.Series:
    """Convierte valores sí/no, true/false y 1/0 en una bandera binaria."""
    mapping = {
        "yes": 1,
        "no": 0,
        "true": 1,
        "false": 0,
        "1": 1,
        "0": 0,
    }

    return (
        series.astype(str)
        .str.lower()
        .str.strip()
        .map(mapping)
        .astype("Int64")
    )


def adapt_tickets_to_hr(
    df: pd.DataFrame,
    column_rename_map: Mapping[str, str] | None = None,
    process_mapping: Mapping[str, str] | None = None,
    system_mapping: Mapping[str, str] | None = None,
    columns_to_drop: Sequence[str] | None = None,
) -> pd.DataFrame:
    """
    Adapta un dataset genérico de soporte al contexto de HR Operations.

    La función:
    - renombra variables;
    - elimina columnas no relevantes;
    - mapea procesos y sistemas;
    - convierte fechas;
    - crea variables temporales;
    - crea banderas binarias de SLA, escalación y prioridad.
    """
    result = df.copy()

    rename_map = dict(column_rename_map or COLUMN_RENAME_MAP)
    process_map = dict(process_mapping or HR_PROCESS_MAPPING)
    system_map = dict(system_mapping or HR_SYSTEM_MAPPING)
    drop_columns = list(columns_to_drop or COLUMNS_TO_DROP)

    result = result.rename(columns=rename_map)

    existing_drop_columns = [
        column for column in drop_columns if column in result.columns
    ]
    result = result.drop(columns=existing_drop_columns)

    required_mapping_columns = {"hr_process", "hr_system"}
    missing_mapping_columns = required_mapping_columns.difference(result.columns)
    if missing_mapping_columns:
        raise KeyError(
            "Faltan columnas necesarias para adaptar el dataset: "
            f"{sorted(missing_mapping_columns)}"
        )

    result["hr_process_name"] = result["hr_process"].map(process_map)
    result["hr_system_name"] = result["hr_system"].map(system_map)

    for date_column in ("ticket_created_date", "ticket_resolved_date"):
        if date_column in result.columns:
            result[date_column] = pd.to_datetime(
                result[date_column],
                errors="coerce",
            )

    if "ticket_created_date" in result.columns:
        result["created_year"] = result["ticket_created_date"].dt.year
        result["created_month"] = result["ticket_created_date"].dt.month
        result["created_dayofweek"] = result["ticket_created_date"].dt.dayofweek
        result["created_quarter"] = result["ticket_created_date"].dt.quarter

    if "escalated" in result.columns:
        result["escalated_flag"] = _to_binary_flag(result["escalated"])

    if "sla_breached" in result.columns:
        result["sla_breached_flag"] = _to_binary_flag(result["sla_breached"])

    if "case_priority" in result.columns:
        normalized_priority = (
            result["case_priority"]
            .astype(str)
            .str.lower()
            .str.strip()
        )
        result["high_priority_flag"] = normalized_priority.eq("high").astype(int)
        result["urgent_priority_flag"] = normalized_priority.eq("urgent").astype(int)

    return result


def validate_hr_mapping(df: pd.DataFrame) -> dict[str, list[Any]]:
    """
    Devuelve los procesos y sistemas originales que no pudieron mapearse.
    """
    unmapped_processes: list[Any] = []
    unmapped_systems: list[Any] = []

    if {"hr_process", "hr_process_name"}.issubset(df.columns):
        unmapped_processes = (
            df.loc[df["hr_process_name"].isna(), "hr_process"]
            .dropna()
            .unique()
            .tolist()
        )

    if {"hr_system", "hr_system_name"}.issubset(df.columns):
        unmapped_systems = (
            df.loc[df["hr_system_name"].isna(), "hr_system"]
            .dropna()
            .unique()
            .tolist()
        )

    return {
        "unmapped_processes": unmapped_processes,
        "unmapped_systems": unmapped_systems,
    }


# ---------------------------------------------------------------------------
# 3. UNIDADES OPERATIVAS
# ---------------------------------------------------------------------------

def create_process_unit_id(
    df: pd.DataFrame,
    output_column: str = "process_unit_id_v2",
) -> pd.DataFrame:
    """
    Crea el identificador de unidad operativa:

    proceso HR + sistema HR + región + canal.
    """
    result = df.copy()

    required_columns = [
        "hr_process_name",
        "hr_system_name",
        "region",
        "contact_channel",
    ]
    missing_columns = set(required_columns).difference(result.columns)

    if missing_columns:
        raise KeyError(
            "Faltan columnas para crear la unidad operativa: "
            f"{sorted(missing_columns)}"
        )

    result[output_column] = (
        result[required_columns]
        .astype("string")
        .fillna("Unknown")
        .agg(" | ".join, axis=1)
    )

    return result


def aggregate_operational_units(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega los tickets al nivel de unidad operativa HR.
    """
    required_columns = {
        "process_unit_id_v2",
        "hr_process_name",
        "hr_system_name",
        "region",
        "contact_channel",
        "case_id",
        "resolution_time_hours",
        "first_response_time_hours",
        "sla_breached_flag",
        "escalated_flag",
        "process_complexity_score",
        "employee_satisfaction_score",
        "previous_cases",
        "employee_tenure_months",
        "high_priority_flag",
        "urgent_priority_flag",
    }

    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise KeyError(
            "Faltan columnas para agregar las unidades operativas: "
            f"{sorted(missing_columns)}"
        )

    summary = (
        df.groupby(
            [
                "process_unit_id_v2",
                "hr_process_name",
                "hr_system_name",
                "region",
                "contact_channel",
            ],
            dropna=False,
        )
        .agg(
            total_cases=("case_id", "count"),
            avg_resolution_time_hours=("resolution_time_hours", "mean"),
            avg_first_response_time_hours=("first_response_time_hours", "mean"),
            sla_breach_rate=("sla_breached_flag", "mean"),
            escalation_rate=("escalated_flag", "mean"),
            avg_complexity_score=("process_complexity_score", "mean"),
            avg_satisfaction_score=("employee_satisfaction_score", "mean"),
            avg_previous_cases=("previous_cases", "mean"),
            avg_employee_tenure_months=("employee_tenure_months", "mean"),
            high_priority_rate=("high_priority_flag", "mean"),
            urgent_priority_rate=("urgent_priority_flag", "mean"),
        )
        .reset_index()
    )

    return summary


# ---------------------------------------------------------------------------
# 4. AUTOMATION OPPORTUNITY SCORE
# ---------------------------------------------------------------------------

def min_max_scale(series: pd.Series) -> pd.Series:
    """
    Normaliza una serie entre 0 y 1.

    Si todos los valores son iguales, devuelve una serie de ceros.
    """
    numeric_series = pd.to_numeric(series, errors="coerce")
    minimum = numeric_series.min()
    maximum = numeric_series.max()

    if pd.isna(minimum) or pd.isna(maximum) or maximum == minimum:
        return pd.Series(0.0, index=series.index)

    return (numeric_series - minimum) / (maximum - minimum)


def add_normalized_score_components(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea las variables normalizadas utilizadas en el score.
    """
    result = df.copy()

    source_to_score = {
        "total_cases": "volume_score",
        "avg_resolution_time_hours": "resolution_time_score",
        "avg_first_response_time_hours": "first_response_score",
        "sla_breach_rate": "sla_risk_score",
        "escalation_rate": "escalation_score",
        "avg_complexity_score": "complexity_score",
        "avg_previous_cases": "previous_cases_score",
        "high_priority_rate": "high_priority_score",
        "urgent_priority_rate": "urgent_priority_score",
    }

    missing_columns = set(source_to_score).difference(result.columns)
    if missing_columns:
        raise KeyError(
            "Faltan columnas para calcular los componentes del score: "
            f"{sorted(missing_columns)}"
        )

    for source_column, score_column in source_to_score.items():
        result[score_column] = min_max_scale(result[source_column])

    return result


def calculate_automation_score(
    df: pd.DataFrame,
    weights: Mapping[str, float] | None = None,
) -> pd.DataFrame:
    """
    Calcula el Automation Opportunity Score en una escala de 0 a 100.
    """
    result = add_normalized_score_components(df)
    score_weights = dict(weights or AUTOMATION_SCORE_WEIGHTS)

    if not np.isclose(sum(score_weights.values()), 1.0):
        raise ValueError("Los pesos del score deben sumar 1.0.")

    missing_columns = set(score_weights).difference(result.columns)
    if missing_columns:
        raise KeyError(
            "Faltan componentes normalizados para calcular el score: "
            f"{sorted(missing_columns)}"
        )

    weighted_score = sum(
        result[column] * weight
        for column, weight in score_weights.items()
    )

    result["automation_score"] = (weighted_score * 100).round(2)

    return result


def classify_automation_priority(
    df: pd.DataFrame,
    score_column: str = "automation_score",
    low_quantile: float = 0.25,
    high_quantile: float = 0.75,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """
    Clasifica la prioridad mediante percentiles del score.

    Returns
    -------
    tuple[pd.DataFrame, dict]
        DataFrame clasificado y umbrales utilizados.
    """
    if not 0 <= low_quantile < high_quantile <= 1:
        raise ValueError(
            "Los cuantiles deben cumplir: 0 <= low < high <= 1."
        )

    result = df.copy()

    if score_column not in result.columns:
        raise KeyError(f"No existe la columna: {score_column}")

    low_threshold = float(result[score_column].quantile(low_quantile))
    high_threshold = float(result[score_column].quantile(high_quantile))

    conditions = [
        result[score_column] >= high_threshold,
        result[score_column] >= low_threshold,
    ]
    choices = ["Alta", "Media"]

    result["automation_priority"] = np.select(
        conditions,
        choices,
        default="Baja",
    )

    thresholds = {
        "low_threshold": round(low_threshold, 4),
        "high_threshold": round(high_threshold, 4),
    }

    return result, thresholds


def recommend_automation_solution(row: pd.Series) -> str:
    """
    Recomienda una solución tecnológica según prioridad y señales operativas.
    """
    priority = row.get("automation_priority")
    complexity = float(row.get("avg_complexity_score", 0))
    sla_breach_rate = float(row.get("sla_breach_rate", 0))
    contact_channel = str(row.get("contact_channel", ""))

    if priority == "Alta":
        if complexity >= 6.5 and sla_breach_rate >= 0.5:
            return "IA asistida con revisión humana"
        if contact_channel in {"Email", "Web Form"} and complexity < 6:
            return "Workflow automation"
        if contact_channel in {"Chat", "Social Media"} and complexity < 6:
            return "Chatbot o asistente virtual"
        if sla_breach_rate >= 0.5:
            return "Automatización parcial con alertas SLA"
        return "Automatización prioritaria"

    if priority == "Media":
        if complexity >= 6:
            return "Rediseño del proceso antes de automatizar"
        if sla_breach_rate >= 0.5:
            return "Automatización parcial con alertas SLA"
        return "Automatización parcial"

    if complexity >= 7:
        return "Mantener revisión humana"

    return "Baja prioridad de automatización"


def add_recommended_solution(df: pd.DataFrame) -> pd.DataFrame:
    """Añade la recomendación tecnológica a cada unidad operativa."""
    result = df.copy()
    result["recommended_solution"] = result.apply(
        recommend_automation_solution,
        axis=1,
    )
    return result


# ---------------------------------------------------------------------------
# 5. AHORRO OPERATIVO Y RANKING
# ---------------------------------------------------------------------------

def estimate_operational_savings(
    df: pd.DataFrame,
    savings_rate_mapping: Mapping[str, float] | None = None,
    manual_work_rate_mapping: Mapping[str, float] | None = None,
) -> pd.DataFrame:
    """
    Estima el tiempo manual y las horas operativas potencialmente ahorrables.
    """
    result = df.copy()
    savings_map = dict(savings_rate_mapping or SAVINGS_RATE_MAPPING)
    manual_work_map = dict(
        manual_work_rate_mapping or MANUAL_WORK_RATE_MAPPING
    )

    required_columns = {
        "automation_priority",
        "total_cases",
        "avg_resolution_time_hours",
    }
    missing_columns = required_columns.difference(result.columns)

    if missing_columns:
        raise KeyError(
            "Faltan columnas para estimar el ahorro operativo: "
            f"{sorted(missing_columns)}"
        )

    result["estimated_manual_work_rate"] = (
        result["automation_priority"].map(manual_work_map)
    )
    result["estimated_manual_handling_time_hours"] = (
        result["avg_resolution_time_hours"]
        * result["estimated_manual_work_rate"]
    ).round(2)

    result["estimated_savings_rate"] = (
        result["automation_priority"].map(savings_map)
    )
    result["estimated_operational_hours_saved"] = (
        result["total_cases"]
        * result["estimated_manual_handling_time_hours"]
        * result["estimated_savings_rate"]
    ).round(2)

    return result


def build_automation_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ordena las oportunidades y añade una columna de ranking.
    """
    required_columns = {
        "automation_score",
        "estimated_operational_hours_saved",
    }
    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise KeyError(
            "Faltan columnas para crear el ranking: "
            f"{sorted(missing_columns)}"
        )

    ranking = (
        df.sort_values(
            by=[
                "automation_score",
                "estimated_operational_hours_saved",
            ],
            ascending=[False, False],
        )
        .reset_index(drop=True)
    )

    ranking["ranking"] = ranking.index + 1

    return ranking


def build_executive_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea el resumen ejecutivo utilizado en el dashboard y la presentación.
    """
    required_columns = {
        "automation_score",
        "automation_priority",
        "estimated_operational_hours_saved",
    }
    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise KeyError(
            "Faltan columnas para crear el resumen ejecutivo: "
            f"{sorted(missing_columns)}"
        )

    return pd.DataFrame(
        {
            "métrica": [
                "Unidades operativas analizadas",
                "Score promedio de automatización",
                "Score máximo",
                "Score mínimo",
                "Unidades de prioridad alta",
                "Unidades de prioridad media",
                "Unidades de prioridad baja",
                "Horas operativas estimadas ahorrables totales",
            ],
            "valor": [
                len(df),
                round(df["automation_score"].mean(), 2),
                round(df["automation_score"].max(), 2),
                round(df["automation_score"].min(), 2),
                int((df["automation_priority"] == "Alta").sum()),
                int((df["automation_priority"] == "Media").sum()),
                int((df["automation_priority"] == "Baja").sum()),
                round(df["estimated_operational_hours_saved"].sum(), 2),
            ],
        }
    )


def build_dimension_summary(
    df: pd.DataFrame,
    dimension: str,
) -> pd.DataFrame:
    """
    Crea un resumen agregado por proceso, sistema, región, canal o solución.
    """
    if dimension not in df.columns:
        raise KeyError(f"No existe la dimensión solicitada: {dimension}")

    required_columns = {
        "process_unit_id_v2",
        "total_cases",
        "automation_score",
        "estimated_operational_hours_saved",
    }
    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise KeyError(
            "Faltan columnas para crear el resumen dimensional: "
            f"{sorted(missing_columns)}"
        )

    return (
        df.groupby(dimension, dropna=False)
        .agg(
            total_units=("process_unit_id_v2", "count"),
            total_cases=("total_cases", "sum"),
            avg_automation_score=("automation_score", "mean"),
            total_estimated_hours_saved=(
                "estimated_operational_hours_saved",
                "sum",
            ),
        )
        .reset_index()
        .sort_values(
            "total_estimated_hours_saved",
            ascending=False,
        )
    )


# ---------------------------------------------------------------------------
# 6. PIPELINE COMPLETO DE SCORING
# ---------------------------------------------------------------------------

def build_scored_operational_dataset(
    tickets_df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """
    Ejecuta el flujo completo desde tickets adaptados hasta ranking final.

    Nota
    ----
    El DataFrame debe contener los tickets originales antes de la adaptación.
    """
    hr_df = adapt_tickets_to_hr(tickets_df)
    hr_df = create_process_unit_id(hr_df)
    units_df = aggregate_operational_units(hr_df)
    scored_df = calculate_automation_score(units_df)
    scored_df, thresholds = classify_automation_priority(scored_df)
    scored_df = add_recommended_solution(scored_df)
    scored_df = estimate_operational_savings(scored_df)
    ranking_df = build_automation_ranking(scored_df)

    return ranking_df, thresholds


# ---------------------------------------------------------------------------
# 7. MACHINE LEARNING
# ---------------------------------------------------------------------------

def split_features_target(
    df: pd.DataFrame,
    target_column: str = "automation_priority",
    excluded_columns: Sequence[str] | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Separa variables predictoras y variable objetivo.
    """
    if target_column not in df.columns:
        raise KeyError(f"No existe la variable objetivo: {target_column}")

    default_excluded = {
        target_column,
        "process_unit_id_v2",
        "ranking",
        "recommended_solution",
        "estimated_savings_rate",
        "estimated_manual_work_rate",
        "estimated_manual_handling_time_hours",
        "estimated_operational_hours_saved",
    }
    default_excluded.update(excluded_columns or [])

    feature_columns = [
        column for column in df.columns
        if column not in default_excluded
    ]

    return df[feature_columns].copy(), df[target_column].copy()


def build_preprocessor(
    X: pd.DataFrame,
) -> tuple[ColumnTransformer, list[str], list[str]]:
    """
    Crea el preprocesador para variables numéricas y categóricas.
    """
    categorical_features = (
        X.select_dtypes(include=["object", "string", "category"])
        .columns
        .tolist()
    )
    numeric_features = (
        X.select_dtypes(include=[np.number])
        .columns
        .tolist()
    )

    numeric_transformer = Pipeline(
        steps=[("scaler", StandardScaler())]
    )
    categorical_transformer = Pipeline(
        steps=[
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=True,
                ),
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric_features),
            (
                "categorical",
                categorical_transformer,
                categorical_features,
            ),
        ]
    )

    return preprocessor, numeric_features, categorical_features


def get_default_classification_models(
    random_state: int = 42,
) -> dict[str, BaseEstimator]:
    """Devuelve los modelos comparados en el notebook."""
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=random_state,
        ),
        "Decision Tree": DecisionTreeClassifier(
            random_state=random_state,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            random_state=random_state,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            random_state=random_state,
        ),
    }


def train_and_evaluate_models(
    X: pd.DataFrame,
    y: pd.Series,
    models: Mapping[str, BaseEstimator] | None = None,
    test_size: float = 0.20,
    random_state: int = 42,
) -> dict[str, Any]:
    """
    Entrena, compara y selecciona el modelo con mayor F1 macro.
    """
    if y.nunique() < 2:
        raise ValueError(
            "La variable objetivo debe contener al menos dos clases."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    preprocessor, numeric_features, categorical_features = (
        build_preprocessor(X)
    )
    candidate_models = dict(models or get_default_classification_models(
        random_state=random_state
    ))

    results: list[dict[str, Any]] = []
    trained_models: dict[str, Pipeline] = {}

    for model_name, model in candidate_models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        results.append(
            {
                "model": model_name,
                "accuracy": accuracy_score(y_test, predictions),
                "precision_macro": precision_score(
                    y_test,
                    predictions,
                    average="macro",
                    zero_division=0,
                ),
                "recall_macro": recall_score(
                    y_test,
                    predictions,
                    average="macro",
                    zero_division=0,
                ),
                "f1_macro": f1_score(
                    y_test,
                    predictions,
                    average="macro",
                    zero_division=0,
                ),
            }
        )
        trained_models[model_name] = pipeline

    comparison = (
        pd.DataFrame(results)
        .sort_values("f1_macro", ascending=False)
        .reset_index(drop=True)
    )

    best_model_name = str(comparison.loc[0, "model"])
    best_model = trained_models[best_model_name]
    best_predictions = best_model.predict(X_test)

    final_metrics = pd.DataFrame(
        {
            "métrica": [
                "Modelo ganador",
                "Accuracy",
                "Precision macro",
                "Recall macro",
                "F1 macro",
            ],
            "valor": [
                best_model_name,
                round(accuracy_score(y_test, best_predictions), 4),
                round(
                    precision_score(
                        y_test,
                        best_predictions,
                        average="macro",
                        zero_division=0,
                    ),
                    4,
                ),
                round(
                    recall_score(
                        y_test,
                        best_predictions,
                        average="macro",
                        zero_division=0,
                    ),
                    4,
                ),
                round(
                    f1_score(
                        y_test,
                        best_predictions,
                        average="macro",
                        zero_division=0,
                    ),
                    4,
                ),
            ],
        }
    )

    return {
        "comparison": comparison,
        "trained_models": trained_models,
        "best_model_name": best_model_name,
        "best_model": best_model,
        "final_metrics": final_metrics,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "y_pred": best_predictions,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
    }


def get_logistic_coefficients(
    trained_pipeline: Pipeline,
) -> pd.DataFrame:
    """
    Extrae los coeficientes por clase de una Regresión Logística entrenada.
    """
    preprocessor = trained_pipeline.named_steps.get("preprocessor")
    model = trained_pipeline.named_steps.get("model")

    if preprocessor is None or model is None:
        raise ValueError(
            "El pipeline debe contener los pasos 'preprocessor' y 'model'."
        )

    if not isinstance(model, LogisticRegression):
        raise TypeError(
            "Esta función solo admite modelos LogisticRegression."
        )

    feature_names = preprocessor.get_feature_names_out()

    return pd.DataFrame(
        model.coef_,
        columns=feature_names,
        index=model.classes_,
    )


def get_top_features_by_class(
    coefficients_df: pd.DataFrame,
    top_n: int = 15,
) -> dict[str, pd.DataFrame]:
    """
    Devuelve las variables con mayor coeficiente positivo para cada clase.
    """
    return {
        str(class_name): (
            coefficients_df.loc[class_name]
            .sort_values(ascending=False)
            .head(top_n)
            .rename_axis("feature")
            .reset_index(name="coefficient")
        )
        for class_name in coefficients_df.index
    }


def save_model(
    model: BaseEstimator,
    output_path: str | Path,
) -> Path:
    """
    Guarda un modelo entrenado en formato Joblib.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    return path
