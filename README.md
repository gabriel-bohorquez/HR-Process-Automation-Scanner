## HR Process Automation Scanner

People Analytics · HR Operations · Machine Learning · Automation · Streamlit · Tableau

Presentación: https://canva.link/lkbbkp0jv0y2bum

HR Process Automation Scanner es un proyecto end-to-end de análisis de datos, Machine Learning y visualización ejecutiva diseñado para identificar, priorizar y recomendar oportunidades de automatización en procesos de HR Operations.

El proyecto transforma datos operativos de tickets en una matriz de decisión que permite responder una pregunta de negocio concreta:

¿Qué procesos, sistemas, regiones y canales internos de HR Operations deberían priorizarse para automatización?

La solución combina:

análisis exploratorio de datos;
reglas de negocio;
feature engineering;
Automation Opportunity Score;
modelo predictivo de Machine Learning;
dashboard ejecutivo en Tableau;
aplicación interactiva en Streamlit;
recomendaciones accionables para negocio.


## 1. Resumen ejecutivo

Las áreas de HR Operations gestionan grandes volúmenes de solicitudes internas relacionadas con empleados, documentación, accesos, nómina, beneficios, plataformas, incidencias, tickets y servicios internos.

Sin embargo, no todos los procesos deben automatizarse al mismo tiempo.

Automatizar sin priorización puede generar:

inversión tecnológica mal dirigida;
bajo retorno operativo;
automatización de procesos poco relevantes;
pérdida de control en procesos complejos;
saturación de equipos de transformación digital;
falta de conexión entre datos, negocio y decisión.

Este proyecto propone una solución analítica para pasar de una gestión reactiva de tickets a una lógica de priorización basada en datos.

El resultado final es una herramienta capaz de:

analizar procesos HR;
detectar fricción operativa;
estimar ahorro potencial;
clasificar oportunidades de automatización;
recomendar soluciones tecnológicas;
visualizar resultados en Tableau;
simular escenarios en Streamlit.


## 2. Problema de negocio

En muchas organizaciones, los equipos de HR Operations reciben miles de solicitudes internas a través de diferentes canales: email, portales de autoservicio, herramientas colaborativas, asistentes virtuales o sistemas internos.

Estas solicitudes pueden estar relacionadas con:

payroll;
beneficios;
documentación;
accesos;
onboarding;
employee data;
HRIS;
incidencias de sistemas;
soporte interno;
consultas administrativas.

El problema no es únicamente el volumen de tickets. El verdadero reto es saber dónde actuar primero.

La pregunta de negocio central es:

¿Qué unidades operativas presentan mayor potencial de automatización y deberían priorizarse para generar impacto operativo real?

## 3. Objetivo del proyecto

El objetivo del proyecto es construir una solución analítica que permita:

analizar datos operativos de tickets;
adaptar un dataset de soporte a un contexto de HR Operations;
transformar variables operativas en variables de People Analytics;
crear una unidad de análisis basada en proceso, sistema, región y canal;
calcular un Automation Opportunity Score;
clasificar oportunidades en prioridad alta, media o baja;
entrenar un modelo predictivo de Machine Learning;
construir un dashboard ejecutivo en Tableau;
desarrollar una aplicación interactiva en Streamlit;
traducir datos operativos en decisiones de automatización.

## 4. Mapa mental del proyecto
HR Process Automation Scanner
│
├── Problema de negocio
│   ├── Alto volumen de tickets HR
│   ├── Procesos manuales repetitivos
│   ├── Incumplimientos de SLA
│   ├── Escalaciones frecuentes
│   └── Dificultad para priorizar automatizaciones
│
├── Datos
│   ├── Tickets operativos
│   ├── Procesos HR
│   ├── Sistemas HR
│   ├── Canales internos
│   ├── Regiones
│   └── Métricas de eficiencia
│
├── Análisis
│   ├── Limpieza de datos
│   ├── Transformación de variables
│   ├── Feature engineering
│   ├── EDA
│   └── Reglas de negocio
│
├── Scoring
│   ├── Automation Opportunity Score
│   ├── Priorización alta / media / baja
│   ├── Solución recomendada
│   └── Ahorro operativo estimado
│
├── Machine Learning
│   ├── Clasificación multiclase
│   ├── Comparación de modelos
│   ├── Evaluación
│   └── Predicción de prioridad
│
├── Visualización
│   ├── Dashboard Tableau
│   ├── KPIs ejecutivos
│   ├── Ranking de oportunidades
│   └── Storytelling visual
│
└── Producto final
    ├── Streamlit App
    ├── Simulador predictivo
    ├── Recomendación tecnológica
    └── Soporte a la toma de decisiones


## 5. Enfoque analítico

El proyecto sigue un flujo completo de análisis de datos:

Business Problem
↓
Data Understanding
↓
Data Cleaning
↓
Data Transformation
↓
Feature Engineering
↓
Exploratory Data Analysis
↓
Automation Opportunity Scoring
↓
Machine Learning
↓
Tableau Dashboard
↓
Streamlit App
↓
Business Recommendations

Este flujo permite demostrar no solo conocimiento técnico, sino también pensamiento de negocio y capacidad para convertir datos en una solución utilizable.

## 6. Dataset utilizado

El proyecto parte de un dataset público de tickets de soporte, adaptado a un contexto de HR Operations.

El dataset original fue transformado para representar procesos internos de Recursos Humanos.

Adaptación conceptual del dataset
Variable original    Variable adaptada
product    hr_system
category    hr_process
issue_description    case_description
priority    case_priority
status    case_status
channel    hr_contact_channel
customer_tenure_months    employee_tenure_months
customer_satisfaction_score    employee_satisfaction_score
issue_complexity_score    process_complexity_score

Esta adaptación permite simular un entorno de People Operations donde los tickets representan solicitudes internas de empleados y procesos administrativos de RR. HH.

## 7. Unidad de análisis

La unidad principal del análisis es una unidad operativa HR.

Cada unidad operativa combina:

Proceso HR
+
Sistema HR
+
Región
+
Canal interno

Ejemplo:

Payroll Support Request
+
Payroll Payment Gateway
+
Europe
+
Internal Collaboration Tool

Esta granularidad permite analizar oportunidades de automatización de forma más precisa que si solo se observaran procesos generales.

## 8. Variables principales
Variable    Descripción
hr_process_name    Proceso HR adaptado
hr_system_name    Sistema o plataforma HR
region    Región operativa
hr_contact_channel    Canal interno de contacto
total_cases    Volumen total de casos
avg_resolution_time_hours    Tiempo medio de resolución
avg_first_response_time_hours    Tiempo medio de primera respuesta
sla_breach_rate    Tasa de incumplimiento SLA
escalation_rate    Tasa de escalación
avg_complexity_score    Complejidad media del proceso
avg_satisfaction_score    Satisfacción media
avg_previous_cases    Casos previos promedio
high_priority_rate    Proporción de casos de prioridad alta
urgent_priority_rate    Proporción de casos urgentes
automation_score    Score de oportunidad de automatización
automation_priority    Prioridad de automatización
recommended_solution    Solución tecnológica recomendada
estimated_operational_hours_saved    Horas operativas estimadas ahorrables


## 9. Automation Opportunity Score

Se construyó un Automation Opportunity Score para priorizar oportunidades de automatización.

Este score combina señales de impacto operativo, fricción y criticidad.

Factores considerados
volumen de casos;
tiempo medio de resolución;
tiempo medio de primera respuesta;
incumplimiento de SLA;
tasa de escalación;
complejidad del proceso;
prioridad de los casos;
recurrencia operativa;
satisfacción asociada al proceso.
Lógica de negocio

La lógica aplicada fue:

A mayor volumen, mayor tiempo de resolución, mayor incumplimiento de SLA, mayor tasa de escalación y mayor complejidad, mayor oportunidad potencial de automatización.

## 10. Mapa mental del scoring
Automation Opportunity Score
│
├── Volumen
│   └── Más casos = mayor impacto potencial
│
├── Tiempo
│   ├── Mayor tiempo de resolución
│   └── Mayor tiempo de primera respuesta
│
├── Riesgo operativo
│   ├── SLA breach rate
│   ├── Escalation rate
│   └── Casos urgentes
│
├── Complejidad
│   ├── Procesos simples → candidatos a workflow automation
│   └── Procesos complejos → candidatos a IA asistida o revisión humana
│
├── Impacto esperado
│   ├── Horas ahorrables
│   ├── Reducción de fricción
│   └── Liberación de capacidad operativa
│
└── Resultado
    ├── Prioridad Alta
    ├── Prioridad Media
    └── Prioridad Baja


## 11. Clasificación de prioridad

Cada unidad operativa fue clasificada en tres niveles:

Prioridad    Interpretación
Alta    Candidata fuerte para automatización
Media    Requiere análisis adicional o automatización parcial
Baja    No prioritaria en una primera fase



## 12. Soluciones recomendadas

Según las características de cada unidad operativa, la herramienta recomienda diferentes tipos de solución:

Workflow automation;
Chatbot o asistente virtual;
Automatización parcial con alertas SLA;
IA asistida con revisión humana;
Rediseño del proceso antes de automatizar;
Mantener revisión humana.
Lógica general de recomendación
Solución recomendada
│
├── Workflow automation
│   └── Procesos repetitivos, simples y de alto volumen
│
├── Chatbot o asistente virtual
│   └── Consultas frecuentes a través de canales digitales
│
├── Automatización parcial con alertas SLA
│   └── Procesos con riesgo operativo o retrasos frecuentes
│
├── IA asistida con revisión humana
│   └── Procesos complejos con necesidad de criterio
│
├── Rediseño del proceso
│   └── Casos donde automatizar sin simplificar generaría poco valor
│
└── Mantener revisión humana
    └── Procesos de baja prioridad o alta sensibilidad


##13. Machine Learning

Se entrenó un modelo de clasificación multiclase para predecir la prioridad de automatización de nuevas unidades operativas.

Variable objetivo
automation_priority

Clases:

Alta;
Media;
Baja.
Modelos evaluados
Logistic Regression;
Decision Tree;
Random Forest;
Gradient Boosting.
Modelo seleccionado
Logistic Regression
Métricas principales
Métrica    Resultado aproximado
Accuracy    0.9683
Precision macro    0.9681
Recall macro    0.9689
F1 macro    0.9685

El modelo aprende la lógica de priorización definida a partir de reglas de negocio y permite aplicarla de forma consistente a nuevas unidades operativas.


## 14. Mapa mental del modelo predictivo
Machine Learning Model
│
├── Input
│   ├── Proceso HR
│   ├── Sistema HR
│   ├── Región
│   ├── Canal interno
│   ├── Volumen de casos
│   ├── Tiempo de resolución
│   ├── SLA breach rate
│   ├── Escalation rate
│   ├── Complejidad
│   └── Prioridad operativa
│
├── Processing
│   ├── Encoding de variables categóricas
│   ├── Preprocesamiento
│   ├── Entrenamiento
│   ├── Validación
│   └── Evaluación
│
├── Output
│   ├── Prioridad Alta
│   ├── Prioridad Media
│   └── Prioridad Baja
│
└── Business Value
    ├── Priorización consistente
    ├── Simulación de nuevas unidades
    ├── Apoyo a decisiones de automatización
    └── Traducción del modelo a acción


## 15. Tableau Dashboard

El proyecto incluye un dashboard ejecutivo desarrollado en Tableau para visualizar los principales resultados del análisis.

El dashboard permite analizar:

KPIs generales del proyecto;
distribución de prioridad de automatización;
procesos con mayor ahorro operativo estimado;
sistemas HR con mayor score promedio;
ranking de oportunidades de automatización.

Archivo incluido:

HR_Process_Automation_Dashboard.twbx

El dashboard está diseñado para comunicar resultados de forma ejecutiva, priorizando claridad visual, lectura rápida y toma de decisiones.


## 16. Aplicación Streamlit

El proyecto culmina en una aplicación interactiva desarrollada con Streamlit.

La app permite:

explorar el resumen ejecutivo;
filtrar oportunidades por proceso, sistema, región, canal y prioridad;
visualizar el ranking de oportunidades de automatización;
consultar la matriz de priorización;
simular nuevas unidades operativas;
predecir prioridad de automatización;
obtener una recomendación tecnológica;
estimar horas operativas ahorrables;
visualizar la confianza del modelo.


## 17. Secciones de la app
Resumen ejecutivo

Muestra los indicadores principales del análisis:

unidades operativas analizadas;
casos procesados;
score promedio;
horas operativas estimadas ahorrables;
distribución de prioridad;
procesos con mayor ahorro estimado.
Ranking de automatización

Permite explorar las mejores oportunidades de automatización ordenadas por score.

Incluye:

KPIs del ranking;
Top 10 oportunidades por score;
matriz de priorización;
descarga del ranking filtrado.
Simulador predictivo

Permite introducir las características de una nueva unidad operativa y predecir:

prioridad de automatización;
confianza del modelo;
horas estimadas ahorrables;
solución tecnológica recomendada.
Metodología

Explica la lógica de negocio, el enfoque analítico, el modelo y las limitaciones del proyecto.


## 18. Estructura del proyecto
HR-Process-Automation-Scanner/
│
├── app/
│   └── app.py
│
├── assets/
│   ├── app_page_icon.png
│   └── header_icon.png
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
│       ├── hr_process_automation_ranking_clean.csv
│       └── tableau_hr_automation_dashboard.csv
│
├── models/
│   └── automation_priority_model.pkl
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_analisis_exploratorio_automatizacion.ipynb
│   └── 03_machine_learning_model.ipynb
│
├── reports/
│   ├── system_score_summary.csv
│   ├── region_summary.csv
│   ├── channel_summary.csv
│   ├── solution_summary.csv
│   └── final_priority_matrix.csv
│
├── HR_Process_Automation_Dashboard.twbx
├── requirements.txt
└── README.md


## 19. Tecnologías utilizadas
Python;
Pandas;
Scikit-learn;
Plotly;
Streamlit;
Tableau;
Joblib;
Machine Learning;
Feature Engineering;
Business Rules;
People Analytics;
HR Operations Analytics.


## 20. Cómo ejecutar el proyecto
1. Clonar el repositorio
git clone <repository-url>
cd HR-Process-Automation-Scanner
2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

En Windows:

venv\Scripts\activate
3. Instalar dependencias
python3 -m pip install -r requirements.txt
4. Ejecutar la app
python3 -m streamlit run app/app.py
21. Requisitos

El archivo requirements.txt debe incluir:

streamlit
pandas
plotly
joblib
scikit-learn==1.6.1


## 22. Valor de negocio

Este proyecto demuestra cómo un equipo de People Analytics o HR Operations puede pasar de una gestión reactiva de tickets a una lógica proactiva de priorización.

El valor potencial está en:

reducir carga operativa;
identificar procesos con mayor fricción;
priorizar automatizaciones con criterio;
liberar capacidad del equipo HR;
mejorar cumplimiento SLA;
reducir escalaciones;
apoyar decisiones de inversión tecnológica;
conectar datos operativos con decisiones estratégicas.


## 23. Limitaciones

Este proyecto utiliza un dataset público adaptado a un contexto de HR Operations.

Por tanto:

no representa datos reales de empleados;
las variables HR fueron adaptadas desde un dataset de soporte;
el modelo aprende una lógica de priorización basada en reglas de negocio;
los resultados deben interpretarse como una simulación analítica;
en un entorno real, sería necesario validar la lógica con stakeholders de HR Operations, People Analytics, IT y Finance.
24. Próximos pasos

Posibles mejoras futuras:

integrar datos reales de HRIS o plataformas de ticketing;
incorporar costes por proceso y cálculo de ROI;
añadir NLP sobre descripciones de casos;
detectar patrones de procesos repetitivos;
añadir clustering de procesos similares;
desplegar la app en Streamlit Cloud;
conectar la solución a bases de datos reales;
incorporar feedback de usuarios de negocio.

## 25. Competencias demostradas

Este proyecto demuestra competencias en:

People Analytics;
HR Operations Analytics;
Operations Analytics;
Machine Learning aplicado;
automatización de procesos;
análisis exploratorio de datos;
feature engineering;
diseño de dashboards ejecutivos en Tableau;
desarrollo de aplicaciones analíticas con Streamlit;
comunicación de resultados orientados a negocio;
traducción de datos operativos en decisiones accionables.


## 26. Conclusión

HR Process Automation Scanner es una herramienta analítica diseñada para priorizar oportunidades de automatización en procesos de HR Operations.

El proyecto combina análisis operativo, reglas de negocio, Machine Learning, visualización ejecutiva y una aplicación interactiva para apoyar decisiones de automatización con criterio analítico.

Su principal valor está en transformar datos operativos en una matriz de decisión clara, explicable y orientada a impacto.
