CREATE TABLE IF NOT EXISTS customers(
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY,
    cust_id INTEGER, 
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY(cust_id) REFERENCES customers(customer_id)
);



CREATE TABLE IF NOT EXISTS line_items(
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_name VARCHAR(100) NOT NULL,
    qty INTEGER NOT NULL, 
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id)
);


-- RESET EXISTING DATA


TRUNCATE TABLE line_items, orders, customers CASCADE;

-- INSERT CUSTOMERS

INSERT INTO customers (customer_id, name, region)
SELECT 
  n,
  'Customer ' || n,
  CASE
    WHEN n% 10 = 0 THEN NULL
    WHEN n % 4 = 0 THEN 'North'
    WHEN n % 4 = 1 THEN 'South'
    ELSE 'West'
  END
FROM generate_series(1, 100) AS n;

-- INSERT ORDERS


INSERT INTO orders (order_id, cust_id, total_amount)
SELECT
    n AS order_id,
    ((n-1) % 100) + 1 AS cust_id,
    ROUND((100 + RANDOM() * 9900)::numeric, 2 ) AS total_amount
FROM generate_series(1, 500) AS n;

-- INSERT LINE ITEMS


INSERT INTO line_items(item_id, order_id, product_name, qty, unit_price)
SELECT
    n AS item_id, 
    ((n-1)/ 3) + 1 as order_id, 
    CASE 
        WHEN n % 10 = 0 THEN 'Mouse'
        WHEN n % 4 = 0 THEN 'Keyboard'
        WHEN n % 4 = 1 THEN 'Laptop'
        WHEN n % 4 = 2 THEN 'GPU'
        ELSE 'RAM'
    END AS product_name,

    FLOOR(RANDOM() * 5 + 1):: INTEGER AS qty, 

    ROUND((50 + RANDOM() * 950)::NUMERIC, 2 ) AS unit_price

FROM generate_series(1, 1500) AS n;

