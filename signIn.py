from customerprofile import customer_profile

def login(con):
    """
    Handles user login based on the mobile number.
    """
    try:
        mob_no = input("Enter your mobile number to log in: ")
        with con.cursor() as cur:
            cur.execute("SELECT id, user_name FROM customer WHERE mob_no = %s LIMIT 1", (mob_no,))
            customer = cur.fetchone()

            if customer:
                print(f"{customer[1]} logged in successfully")
                customer_profile(con, customer[0])
            else:
                print("This mobile number is not registered. Please enter a valid mobile number.")
    except Exception as e:
        print(f"An error occurred: {e}")
