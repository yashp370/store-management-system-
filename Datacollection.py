# store management system 


import mysql.connector

from datetime import datetime


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mysq001"
)

cursor = db.cursor()



# Admin login function
def admin_login():
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")

    cursor.execute("SELECT * FROM admin01 WHERE email = %s AND password = %s", (email, password))
    admin = cursor.fetchone()

    if admin:
        print(f"Login successful! '{admin[1]}'")
        print("Welcome Boss")
        return True
    else:
        print("Invalid email or password!")
        return False
    
    
    
    

# Customer login function
def customer_login():
    
    while True:
        
        print("1. Sign Up")
        print("2. Login")
        
        sign_up_choice = input("Would you like to sign up or login? (1/2): ").strip()

        if sign_up_choice == "1":
            
            name = input("Enter your name: ").strip()
            
            email = input("Enter your email: ").strip()

            # Check if the inputs are empty
            if not name or not email:
                
                print("Name and email cannot be empty. Please try again.")
                
                continue

            age = input("Enter your age: ")
            gender = input("Enter your gender (M/F): ")
            location = input("Enter your location: ")
            insert_customer(name, email, age, gender, location)
            print(f"Sign up successful! You can now log in, {name}!")
            continue  

        elif sign_up_choice == "2":
            name = input("Enter your name: ").strip()
            email = input("Enter your email: ").strip()

            if not name or not email:
                print("Name and email cannot be empty. Please try again.")
                continue

            cursor.execute("SELECT name, email FROM customers WHERE name = %s AND email = %s", (name, email))
            customer = cursor.fetchone()

            if customer:
                print(f"Login successful! ")
                print(f"Welcome Customer!  '{customer[0]}' ")
                return True
            else:
                print("Invalid name and email!")
                print("Exiting the login process.")
                return False
        else:
            print("Invalid choice. Exiting the login process.")
            return False



# view details
def display_customers():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    print("Displaying all customers:\n")
    for customer in customers:
        print(f"customer_id: {customer[0]}, name: {customer[1]}, email: {customer[2]}, age: {customer[3]}, gender: {customer[4]}, location: {customer[5]}")

def display_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    print("Displaying all products:\n")
    for product in products:
        print(f"product_id: {product[0]}, product_name: {product[1]}, category: {product[2]}, price: {product[3]}")

def display_reviews():
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()
    print("Displaying all reviews:\n")
    for review in reviews:
        print(f"review_id: {review[0]}, customer_id: {review[1]}, product_id: {review[2]}, review_text: {review[3]}, sentiment: {review[4]}, review_date: {review[5]}")

def display_orders():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    print("Displaying all orders:\n")
    for order in orders:
        print(f"order_id: {order[0]}, customer_id: {order[1]}, product_id: {order[2]}, order_date: {order[3]}, quantity: {order[4]}, total_price: {order[5]}")
        
        
        

# Insert 
def insert_customer(name, email, age, gender, location):
    s = "INSERT INTO customers (name, email, age, gender, location) VALUES (%s, %s, %s, %s, %s)"
    v = (name, email, age, gender, location)
    cursor.execute(s, v)
    db.commit()
    print(f"Customer '{name}' inserted successfully!")
    
    


def insert_product(product_name, category, price):
    
    try:
        price = float(price)
        query = "INSERT INTO products (product_name, category, price) VALUES (%s, %s, %s)"
        values = (product_name, category, price)
        cursor.execute(query, values)
        db.commit()
        print(f"Product '{product_name}' inserted successfully!")
    except ValueError:
        print("Error: Price should be a numeric value.")
        
        

def insert_review(customer_id, product_id, review_text, sentiment):
    review_date = datetime.now().strftime('%Y-%m-%d')
    s = "INSERT INTO reviews (customer_id, product_id, review_text, sentiment, review_date) VALUES (%s, %s, %s, %s, %s)"
    v = (customer_id, product_id, review_text, sentiment, review_date)
    cursor.execute(s, v)
    db.commit()
    print("Review inserted successfully!")
    


def insert_order(customer_id, product_id, quantity):
    
    try:
        quantity = int(quantity)
        cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
        product_price = cursor.fetchone()

        if product_price is None:
            print("Error: Product ID not found!")
            return

        total_price = product_price[0] * quantity
        
        order_date = datetime.now().strftime('%y-%m-%d')

        q = "INSERT INTO orders (customer_id, product_id, order_date, quantity, total_price) VALUES (%s, %s, %s, %s, %s)"
        v = (customer_id, product_id, order_date, quantity, total_price)
        cursor.execute(q, v)
        db.commit()
        print("Order inserted successfully!")
        
    except ValueError:
        print("Error: Quantity should be an integer.")
    except Exception as e:
        print(f"Error: {str(e)}")
        
        
        
        
#The main
def main():
    
    while True:
        print("Welcome to the Ordering System menu!")
        print("11. Admin")
        print("22. Customer")
        
        
        i = int(input("Enter Your option (11 or 22): "))
        
        
        if i == 11:
            if admin_login():
                while True:
                    print("Admin Menu:")
                    print("1. Insert customer information")
                    print("2. Add products")
                    print("3. View customers")
                    print("4. View products")
                    print("5. View reviews")
                    print("6. View orders")
                    print("7. View all (Customers, Products, Reviews, Orders)")
                    print("8. Exit")
                    
                   
                    admin_option = int(input("Enter Your option (1-8): "))

                    
                    if admin_option == 1:
                        name = input("Enter customer name: ")
                        email = input("Enter customer email: ")
                        age = input("Enter customer age: ")
                        gender = input("Enter customer gender (M/F): ")
                        location = input("Enter customer location: ")
                        insert_customer(name, email, age, gender, location)
                        
                    elif admin_option == 2:
                        product_name = input("Enter the product name: ")
                        category = input("Enter the category: ")
                        price = input("Enter the price: ")
                        insert_product(product_name, category, price)
                        
                    elif admin_option == 3:
                        display_customers()
                        
                    elif admin_option == 4:
                        display_products()
                        
                    elif admin_option == 5:
                        display_reviews()
                        
                    elif admin_option == 6:
                        display_orders()
                        
                    elif admin_option == 7:
                        display_customers()
                        
                        display_products()
                        
                        display_reviews()
                        
                        display_orders()
                        
                    elif admin_option == 8:
                        print("Exiting the admin menu.")
                        break
                    else:
                        print("Invalid choice! Please enter a valid option.")
                        
                        

        elif i == 22:
            if customer_login():
                while True:
                    print("Welcome Customer")
                    print("\n 1. View Customers")
                    print("2. View Products")
                    print("3. Place orders")
                    print("4. Give Reviews")
                    print("5. Exit")
                        
                        
                    customer_option = int(input("Enter Your option (1-5): "))

                        
                    if customer_option == 1:
                            display_customers()
                            
                    elif customer_option == 2:
                            display_products()
                            
                    elif customer_option == 3:
                            customer_id = input("Enter customer ID: ")
                            product_id = input("Enter product ID: ")
                            quantity = input("Enter quantity: ")
                            insert_order(customer_id, product_id, quantity)
                            
                    elif customer_option == 4:
                            customer_id = input("Enter customer ID: ")
                            product_id = input("Enter product ID: ")
                            review_text = input("Enter review text: ")
                            sentiment = input("Enter sentiment (Positive/Negative/Neutral): ")
                            insert_review(customer_id, product_id, review_text, sentiment)
                            
                    elif customer_option == 5:
                            print("Exiting the customer menu.")
                            break
                    else:
                            print("Invalid choice! Please enter a valid option.")
            else:
                break
        
        else:
            print("Invalid choice! Please enter a valid option.")



if __name__ == "__main__":
    main()
        
        
cursor.close()
db.close()
