from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


# ---------- Step 1: Extract ----------
def extract_from_postgres():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    query = "SELECT sale_date, quantity, price FROM sales"
    df = pd.read_sql(query, conn)
    conn.close()

    #os.makedirs("/opt/airflow/data", exist_ok=True)
    df.to_csv("sales_data.csv", index=False)
    print(f"Extracted {len(df)} rows from Postgres.")
    return "sales_data.csv"


# ---------- Step 2: Transform ----------
def calculate_daily_revenue():
    df = pd.read_csv("sales_data.csv")
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["revenue"] = df["quantity"] * df["price"]

    daily_revenue = df.groupby("sale_date")["revenue"].sum().reset_index()
    daily_revenue.to_csv("daily_revenue.csv", index=False)

    target_date = "1996-08-08"
    revenue_on_date = daily_revenue.loc[
        daily_revenue["sale_date"] == target_date, "revenue"
    ]
    if not revenue_on_date.empty:
        print(f"Total revenue on {target_date}: {revenue_on_date.values[0]:.2f}")
    else:
        print(f"No data for {target_date}")
    return "daily_revenue.csv"


# ---------- Step 3: Visualize ----------
def visualize_revenue():
    df = pd.read_csv("/airflow/datasets/daily_revenue.csv")
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    plt.figure(figsize=(10, 5))
    plt.plot(df["sale_date"], df["revenue"], marker="o", linestyle="-")
    plt.title("Daily Sales Revenue Over Time")
    plt.xlabel("Date")
    plt.ylabel("Revenue ($)")
    plt.grid(True)

    output_path = "/airflow/datasets/daily_revenue_plot.png"
    plt.savefig(output_path)
    print(f"Chart saved to {output_path}")

# ---------- DAG Definition ----------
with DAG(
    dag_id="sales_revenue_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["postgres", "etl", "visualization"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_from_postgres,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=calculate_daily_revenue,
    )

    extract_task >> transform_task