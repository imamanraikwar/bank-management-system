def createTable(con):
    """
    Creates the 'customer', 'account', and 'transactions' tables if they do not exist.
    """
    try:
        with con.cursor() as cur:
            customer_query = """
                CREATE TABLE IF NOT EXISTS customer (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_name VARCHAR(30),
                    dob DATE,
                    email VARCHAR(30),
                    mob_no VARCHAR(10) UNIQUE,
                    address VARCHAR(100)
                );
            """
            account_query = """
                CREATE TABLE IF NOT EXISTS account (
                    account_id INT NOT NULL,
                    account_number BIGINT(6) PRIMARY KEY NOT NULL,
                    current_balance FLOAT DEFAULT 0,
                    date_open DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_close DATETIME,
                    account_status BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (account_id) REFERENCES customer(id)
                );
            """
            transactions_query = """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    account_id INT NOT NULL,
                    transaction_type VARCHAR(20),
                    amount FLOAT,
                    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES account(account_id)
                );
            """
            cur.execute(customer_query)
            cur.execute(account_query)
            cur.execute(transactions_query)
    except Exception as e:
        print(f"An error occurred: {e}")
