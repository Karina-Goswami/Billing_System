import mysql.connector
from datetime import datetime
import pandas as pd

# Connect to MySQL
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL@1234",
        database="Project"
    )
    print("Connected to database successfully!")
except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit()

mydb.autocommit = True
mycursor = mydb.cursor()

# Function to display menu from DB

def display_menu(menu_items):
    print("\n" + "-" * 15 + " MENU " + "-" * 15)
    print(f"{'sr':<5}{'name':<20}{'price($)':<10}")
    for item in menu_items:
        print(f"{item[0]:<5}{item[1]:<20}{item[2]:<10}")
    print("-" * 40)

# Function to get item from menu by serial number

def getitem(sr, menu_items):
    for item in menu_items:
        if item[0] == sr:
            return {"sr": item[0], "name": item[1], "price": item[2]}
    return None

# Main loop
while True:
    mycursor.execute("SELECT * FROM Burger_menu")
    myresult = mycursor.fetchall()

    print("\n======================")
    print("BURGER BILLING SYSTEM ")
    print("======================")

    display_menu(myresult)

    order = []
    while True:
        try:
            choice = int(input("Enter the sr no. from the menu (or 0 to stop order): "))
            if choice == 0:
                break

            item = getitem(choice, myresult)
            if item is None:
                print("Invalid sr no. Try again.")
                continue

            quantity = int(input(f"Enter quantity for {item['name']}: "))
            order.append({
                "sr": item['sr'],
                "name": item['name'],
                "price": item['price'],
                "quantity": quantity,
                "total": item['price'] * quantity
            })

        except ValueError:
            print("Invalid input. Please enter numbers only.")

    if not order:
        print("No items ordered. Returning to menu...\n")
        continue

    student = input("Are you a student (y/n): ").lower()
    delivery = input("Do you want delivery? (y/n): ").lower()
    try:
        tip = int(input("Do you want to give tip (0/5/10)? "))
    except ValueError:
        tip = 0

    print("\n" + "-" * 20 + " Final Bill " + "-" * 20)
    print(f"{'sr':<5}{'name':<20}{'qty':<10}{'total($)':<10}")
    print("-" * 50)

    total = sum(item['total'] for item in order)
    for item in order:
        print(f"{item['sr']:<5}{item['name']:<20}{item['quantity']:<10}{item['total']:<10.2f}")

    print("-" * 50)
    print(f"Subtotal: {total:.2f}")

    final_total = total
    if student == 'y':
        discount = 0.20 * total
        final_total -= discount
        print(f"Student Discount (20%): -{discount:.2f}")

    if delivery == 'y':
        delivery_charge = 0.05 * final_total
        final_total += delivery_charge
        print(f"Delivery Charge (5%): +{delivery_charge:.2f}")

    final_total += tip
    print(f"Tip: +{tip:.2f}")

    print("-" * 50)
    print(f"Total Bill: {final_total:.2f}")
    print("Order Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(" Thank you and come again!\n")

    # Save to database
    for item in order:
        sql = """
        INSERT INTO Burger_orders 
        (item_name, price, quantity, total, student_discount, delivery, tip, final_total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (
            item['name'],
            float(item['price']),
            int(item['quantity']),
            float(item['total']),
            1 if student == 'y' else 0,
            1 if delivery == 'y' else 0,
            tip,
            float(final_total)
        )

        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print("Order saved to the database.")
        except mysql.connector.Error as err:
            print("Error inserting order:", err)

    # Optional: Show all orders
    mycursor.execute("SELECT * FROM Burger_orders")
    for row in mycursor.fetchall():
        print(row)

    # Optional: Save last order as CSV
    pd.DataFrame(order).to_csv("last_order_summary.csv", index=False)
    print("Order summary saved to last_order_summary.csv")