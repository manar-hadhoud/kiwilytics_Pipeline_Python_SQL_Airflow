# Capstone - Kiwilytics ETL Pipeline

## Overview
This Airflow pipeline extracts data from PostgreSQL, transforms and aggregates it,  
and visualizes results to answer key business questions.

## Steps
- **Extract:** Connect to PostgreSQL using Airflow PostgresHook  
- **Transform:** Clean and aggregate order and product data  
- **Load/Visualize:** build plots using matplotlib

## Business Questions
- Which products generate the most revenue?
- Which shippers are most frequently used?
- What is the monthly sales trend?

## Tools Used
- Apache Airflow  
- PostgreSQL  
- Pandas  
- Matplotlib for visualization  

