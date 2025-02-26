import psycopg2
import getpass

# Database connection details
DB_NAME = "bank_db"
DB_USER = "postgres"
DB_PASSWORD = "Miko2005!"
DB_HOST = "localhost"
DB_PORT = "5432"


# Function to connect to the PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print("❌ Database connection failed:", e)
        return None


# Function to create a new bank account
def create_account():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    owner = input("Enter your name: ")
    password = getpass.getpass("Enter a password: ")  # Hides password input
    balance = float(input("Enter initial deposit amount: "))

    cursor.execute("INSERT INTO accounts (owner, password, balance, is_admin) VALUES (%s, %s, %s, FALSE)",
                   (owner, password, balance))
    conn.commit()

    print("✅ Account created successfully!")
    cursor.close()
    conn.close()


# Function to check account balance
def check_balance():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    owner = input("Enter your name: ")
    password = getpass.getpass("Enter your password: ")

    cursor.execute("SELECT balance FROM accounts WHERE owner = %s AND password = %s", (owner, password))
    result = cursor.fetchone()

    if result:
        print(f"💰 Your balance: {result[0]} USD")
    else:
        print("❌ Invalid credentials!")

    cursor.close()
    conn.close()


# Function to check if a user is an admin
def is_admin(owner, password, cursor):
    cursor.execute("SELECT is_admin FROM accounts WHERE owner = %s AND password = %s", (owner, password))
    result = cursor.fetchone()
    return result and result[0]


# Function for admin to modify user account
def modify_account():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    admin = input("Enter admin name: ")
    admin_password = getpass.getpass("Enter admin password: ")

    if not is_admin(admin, admin_password, cursor):
        print("❌ Access denied! Only admin can modify accounts.")
        return

    account_number = input("Enter account number to modify: ")
    new_balance = float(input("Enter new balance: "))

    cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s AND is_admin = FALSE",
                   (new_balance, account_number))
    conn.commit()

    print("✅ Account modified successfully!")
    cursor.close()
    conn.close()


# Function for admin to delete an account
def delete_account():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    admin = input("Enter admin name: ")
    admin_password = getpass.getpass("Enter admin password: ")

    if not is_admin(admin, admin_password, cursor):
        print("❌ Access denied! Only admin can delete accounts.")
        return

    account_number = input("Enter account number to delete: ")

    cursor.execute("DELETE FROM accounts WHERE account_number = %s AND is_admin = FALSE", (account_number,))
    conn.commit()

    print("✅ Account deleted successfully!")
    cursor.close()
    conn.close()


# Function for admin to export accounts to CSV
def export_accounts():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    admin = input("Enter admin name: ")
    admin_password = getpass.getpass("Enter admin password: ")

    if not is_admin(admin, admin_password, cursor):
        print("❌ Access denied! Only admin can export accounts.")
        return

    file_path = input("Enter the file path to export (e.g., C:/Users/Admin/Desktop/accounts.csv): ")

    cursor.execute("COPY (SELECT * FROM accounts WHERE is_admin = FALSE) TO %s DELIMITER ',' CSV HEADER", (file_path,))
    conn.commit()

    print(f"✅ Accounts exported successfully to {file_path}!")
    cursor.close()
    conn.close()


# Main menu
def menu():
    while True:
        print("\n🏦 Bank System Menu")
        print("1. Create Account")
        print("2. Check Balance")
        print("3. Modify Account (Admin Only)")
        print("4. Delete Account (Admin Only)")
        print("5. Export Accounts (Admin Only)")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            check_balance()
        elif choice == "3":
            modify_account()
        elif choice == "4":
            delete_account()
        elif choice == "5":
            export_accounts()
        elif choice == "6":
            print("👋 Exiting the bank system...")
            break
        else:
            print("❌ Invalid option! Please try again.")


# Run the bank system
if __name__ == "__main__":
    menu()
