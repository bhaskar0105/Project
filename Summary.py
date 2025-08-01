import csv

inventory = []
with open('inventory.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        row['Stock'] = int(row["Stock"])
        row['UnitsSold'] = int(row['UnitsSold'])
        row["Price"] = float(row["Price"])
        row['Revenue'] = round(row["UnitsSold"] * row["Price"], 2)
        inventory.append(row)

#print("\nInventory loaded successfully. Sample data:")
#for book in inventory[:3]:
   # print(book)

# Function to search books
def search_books(inventory, field, value):
    results = []
    for book in inventory:
        if value.lower() in book[field].lower():
            results.append(book)
    return results

valid_fields = ["Title", "Author", "Genre"]

# Get valid search field
while True:
    field = input("\nSearch by Title, Author, or Genre: ").strip().title()
    if field in valid_fields:
        break
    else:
        print("Invalid field. Please choose from Title, Author, Genre")

value = input(f"Enter {field} to search for: ").strip()

matches = search_books(inventory, field, value)

if matches:
    print(f"\nBook Found: {len(matches)} result(s):\n")
    for book in matches:
        print(f"Title   : {book['Title']}")
        print(f"Author  : {book['Author']}")
        print(f"Genre   : {book['Genre']}")
        print(f"Stock   : {book['Stock']}")
        print(f"Sold    : {book['UnitsSold']}")
        print(f"Price   : ₹{book['Price']}")
        print(f"Revenue : ₹{book['Revenue']}")
        print("-" * 50)

    # Ask if user wants to purchase
    buy = input("Would you like to purchase a book? (yes/no): ").strip().lower()
    if buy == "yes":
        selected_title = input("Enter the title of the book to purchase: ").strip()
        quantity = int(input("Enter number of copies: "))

        for book in inventory:
            if book['Title'].lower() == selected_title.lower():
                if book['Stock'] >= quantity:
                    book['Stock'] -= quantity
                    book['UnitsSold'] += quantity
                    book['Revenue'] = round(book['UnitsSold'] * book['Price'], 2)
                    print(f"\n{quantity} copies of '{book['Title']}' purchased successfully.")
                else:
                    print(f"\nNot enough stock. Only {book['Stock']} available.")
                break

        # Save updated inventory
        with open('inventory.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=inventory[0].keys())
            writer.writeheader()
            writer.writerows(inventory)

else:
    print("\nNo book available.")

    choice = input("Would you like to add this book to the inventory? (yes/no): ").strip().lower()
    if choice == "yes":
        new_title = input("Enter book title: ").strip()
        new_author = input("Enter author name: ").strip()
        new_genre = input("Enter genre: ").strip()
        new_price = float(input("Enter price: ₹").strip())
        new_stock = int(input("Enter number of copies: ").strip())

        new_book = {
            'Title': new_title,
            'Author': new_author,
            'Genre': new_genre,
            'Price': new_price,
            'Stock': new_stock,
            'UnitsSold': 0,
            'Revenue': 0.0
        }

        inventory.append(new_book)

        with open('inventory.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=new_book.keys())
            writer.writeheader()
            writer.writerows(inventory)

        print(f"\n'{new_title}' added successfully to inventory!")
