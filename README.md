# ERD - Kiwilytics Project

## Overview
This project presents an Entity-Relationship Diagram (ERD) for the Kiwilytics database.  
The design models relationships between customers, orders, products, suppliers, employees, and shippers.

## Tables and Keys
- **Categories**: `category_id` (PK)
- **Customers**: `customer_id` (PK)
- **Employees**: `emp_id` (PK)
- **Orders**: `order_id` (PK), Foreign Keys: `customer_id`, `emp_id`, `shipper_id`
- **Order_Details**: Composite PK (`order_id`, `ProductID`)
- **Products**: `Product_id` (PK), Foreign Keys: `CategoryID`, `SupplierID`
- **Shippers**: `Shipper_id` (PK)
- **Suppliers**: `Supplier_id` (PK)

## Relationships
- Each order belongs to one customer, employee, and shipper.
- Each order can have many products through Order_Details.
- Each product belongs to one category and one supplier.

## Tools Used
- [drawSQL.io](https://drawsql.io/) for ERD creation.

