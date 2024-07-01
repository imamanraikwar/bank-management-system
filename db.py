import mysql.connector as mysqlconnector

def dbConnection():
    """
    Establishes a connection to the MySQL database.
    If the 'bank1' database does not exist, it creates one.
    """
    con = mysqlconnector.connect(host="localhost", user="root", password="12345")
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS bank1")
    cur.execute("USE bank1")
    return con
