# Mercados La Colina S.A. - Data Mining

Data mining project to analyze inventory and predict **stockouts** at Mercados La Colina S.A. The project includes a Python ETL pipeline, a dimensional model in PostgreSQL, data quality and governance rules, predictive feature generation, and a notebook to benchmark machine learning models.

## Objectives

* Consolidate information across stores, sales channels, promotions, products, and inventory.
* Standardize and validate data prior to feeding it into models.
* Engineer features related to supplier lead-time delays, inventory coverage, digital sales channels, ABC classification, and historical stockouts.
* Prepare datasets for predictive modeling and association rule mining.
* Benchmark classification models using accuracy, recall, F1-score, and ROC-AUC.

## Architecture

```text
etl/extract.py
      |
      v
etl/transform.py  --->  staging_rechazos_calidad
      |
      v
etl/features.py
      |
      v
etl/load.py  ------->  dw_inventario_predictivo
                         dw_promociones_apriori

```

The current extractor generates reproducible synthetic data using a fixed random seed. The `generar_datos_crudos()` function creates 15,000 weekly records across five stores, four sales channels, and various product families and promotional campaigns.

## Project Structure

| File | Description |
| --- | --- |
| `main.py` | Orchestrates the end-to-end ETL pipeline stages. |
| `etl/extract.py` | Generates the raw inventory dataset. |
| `etl/transform.py` | Handles standardization, filtering, imputation, and rejection separation. |
| `etl/features.py` | Computes predictive features KPI 6 through KPI 10. |
| `etl/load.py` | Loads the resulting datasets into PostgreSQL. |
| `datawarehouse.sql` | Creates the dimensional star schema. |
| `modelos.ipynb` | Trains and evaluates classification and Apriori models. |
| `verify_installation.py` | Verifies that key dependencies are installed. |
| `test_connection.py` | Tests the PostgreSQL database connection. |

## Requirements

* Python 3.10 or higher.
* PostgreSQL 14 or higher recommended.
* A database named `LaColinaSA`.
* Jupyter Notebook or JupyterLab to run `modelos.ipynb`.

Core dependencies:

* `pandas`, `numpy`
* `scikit-learn`, `xgboost`, `lightgbm`, `mlxtend`
* `matplotlib`, `seaborn`
* `SQLAlchemy`, `psycopg`
* `python-dotenv`

## Installation

From the project root directory (`la_colina_sa`), create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows PowerShell

```

Install dependencies:

```bash
python -m pip install pandas numpy matplotlib seaborn scikit-learn \
  xgboost lightgbm mlxtend sqlalchemy psycopg python-dotenv \
  jupyter

```

Verify installation:

```bash
python verify_installation.py

```

## PostgreSQL Configuration

Configure credentials using environment variables. You can create a `.env` file inside `etl/` using the following template:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=LaColinaSA

```

Do not commit real credentials to the repository. Keep any local `.env` files untracked in version control.

Next, create the dimensional model tables by running `datawarehouse.sql` on the `LaColinaSA` database (for example, using `psql`):

```bash
psql -U postgres -d LaColinaSA -f datawarehouse.sql

```

Test the connection:

```bash
python test_connection.py

```

## Running the Pipeline

Run the pipeline from the `la_colina_sa` directory:

```bash
python main.py

```

The process executes through the following stages:

1. **Extract:** Generates raw data with weekly dates, stores, channels, promotions, inventory levels, and the target variable `quiebre_stock`.
2. **Transform:** Normalizes promotional naming conventions, filters sales outside the operational boundary of 5 to 240 units, imputes missing channel values, and separates rows missing the target variable.
3. **Feature engineering:** Calculates:
* `kpi6_retraso_critico`: Supplier delay greater than four days.
* `kpi7_tension_cobertura`: Stock coverage less than or equal to five days.
* `kpi8_es_digital`: Sale made via Web or WhatsApp.
* `kpi9_prioridad_A`: Product classified as Class A.
* `kpi10_quiebre_t_menos_1`: Historical stockout (t-1) for the same store and product category.


4. **Load:** Writes outputs to PostgreSQL:
* `dw_inventario_predictivo`
* `dw_promociones_apriori`
* `staging_rechazos_calidad`



If writing to PostgreSQL fails, the pipeline saves `dw_inventario_predictivo.csv` locally as a fallback.

## Modeling

Launch the notebook:

```bash
jupyter lab modelos.ipynb

```

The notebook queries `dw_inventario_predictivo`, uses `quiebre_stock` as the target variable, and benchmarks eight classification models—including Decision Tree, Random Forest, Naive Bayes, and SVM. It also structures `dw_promociones_apriori` for association rule mining.

When comparing models, pay close attention to **recall**, **F1-score**, and **ROC-AUC** alongside accuracy. Detecting true stockouts is critical in this scenario, so accuracy alone can misrepresent model effectiveness on imbalanced classes.

## Dimensional Model

`datawarehouse.sql` provisions a star schema comprising:

* Dimensions: `dim_tienda`, `dim_canal`, `dim_promocion`, `dim_producto`, and `dim_tiempo`.
* Fact table: `hecho_inventario`.
* Constraints enforcing binary values for `quiebre_stock` and non-negative operational metrics.

The ETL pipeline outputs analytical datasets tailored for downstream modeling. The fact table and dimensions form the target dimensional architecture for the enterprise warehouse.

## Data Quality & Governance

The pipeline applies these checks before modeling:

* Promotion category standardization.
* Sales range validation.
* Missing channel imputation defaulted to `Sin Especificar` (Unspecified).
* Segregation of null `quiebre_stock` rows into a quality rejects table.
* Casting target variable values to binary integers.
* Parsing `inicio_semana` into date format.

Flagged records are routed to `staging_rechazos_calidad` for auditing and data quality tracking.

## Troubleshooting

**Unable to connect to PostgreSQL**

1. Verify the PostgreSQL service is active.
2. Check `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, and `DB_NAME`.
3. Confirm the `LaColinaSA` database exists.
4. Run `python test_connection.py` to inspect the exact exception.

**Missing dependencies**

Run `python verify_installation.py` and reinstall missing libraries using `python -m pip install ...` inside the active virtual environment.

**Notebook cannot find tables**

Run `python main.py` first, confirm the load stage completed successfully, and ensure the notebook points to the same credentials and database specified in `.env`.

## Project Status

The included extraction generates synthetic data intended for demonstration and development purposes. To deploy with live business data, replace the logic in `etl/extract.py` with authorized production connectors while preserving the pipeline's validation, lineage, and access controls.