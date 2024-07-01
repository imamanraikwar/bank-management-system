def createAccount(con):
    """
    Creates a new customer account and a corresponding bank account.
    """
    while True:
        user_name = input("Enter Your Name*: ")
        dob = input("Enter your date of birth in YYYY-MM-DD format: ")
        email = input("Enter your email: ")
        mob_no = input("Enter your mobile number*: ")
        address = input("Enter your address: ")

        if not user_name or not mob_no:
            print("Please enter required fields")
            continue

        try:
            with con.cursor() as cur:
                cur.execute("SELECT mob_no FROM customer WHERE mob_no = %s", (mob_no,))
                if cur.fetchone():
                    print("This mobile number is already registered")
                    return

                customer_query = """
                    INSERT INTO customer (user_name, dob, email, mob_no, address)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cur.execute(customer_query, (user_name, dob, email, mob_no, address))

                last_id = cur.lastrowid
                account_query = """
                    INSERT INTO account (account_id, account_number)
                    VALUES (%s, %s)
                """
                cur.execute(account_query, (last_id, 300000 + last_id))

                print("Account created successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            con.commit()
            return
