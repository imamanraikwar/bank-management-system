from db import dbConnection
from sqlTables import createTable
from signUP import createAccount
from signIn import login

# Establish a database connection
con = dbConnection()

# Create required tables if they do not exist
createTable(con)

# Display available tables for debugging purposes
with con.cursor() as cur:
    cur.execute("SHOW TABLES")
    print(cur.fetchall())

# Main loop to interact with the user
while True:
    print("Enter 1 for login \nEnter 2 to Create Your Bank Account \nEnter 0 to Exit")

    try:
        ch = int(input())
        if ch == 1:
            login(con)
        elif ch == 2:
            createAccount(con)
        elif ch == 0:
            break
        else:
            print("Please enter a correct option")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Close the database connection at the end
con.close()
