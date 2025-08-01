import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import csv
import os

# Set page configuration
st.set_page_config(page_title="Book Inventory Organizer", layout="wide")

# Load inventory from CSV
@st.cache_data
def load_inventory():
    inventory = []
    with open('inventory.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['Stock'] = int(row['Stock'])
            row['UnitsSold'] = int(row['UnitsSold'])
            row['Price'] = float(row['Price'])
            row['Revenue'] = round(row['UnitsSold'] * row['Price'], 2)
            inventory.append(row)
    return inventory

# Save inventory to CSV
def save_inventory(inventory):
    with open('inventory.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=inventory[0].keys())
        writer.writeheader()
        writer.writerows(inventory)

# Search books function
def search_books(inventory, field, value):
    results = []
    for book in inventory:
        if value.lower() in book[field].lower():
            results.append(book)
    return results

# Initialize session state for inventory
if 'inventory' not in st.session_state:
    st.session_state.inventory = load_inventory()

# Main app
st.title("📚 Book Inventory Organizer")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Search & Purchase", "Add New Book", "Visualizations"])

# Search & Purchase Page
if page == "Search & Purchase":
    st.header("Search & Purchase Books")
    valid_fields = ["Title", "Author", "Genre"]
    field = st.selectbox("Search by", valid_fields)
    value = st.text_input(f"Enter {field} to search for")
    
    if st.button("Search"):
        if value:
            matches = search_books(st.session_state.inventory, field, value)
            if matches:
                st.write(f"**Book Found: {len(matches)} result(s):**")
                for book in matches:
                    st.write(f"**Title**: {book['Title']}")
                    st.write(f"**Author**: {book['Author']}")
                    st.write(f"**Genre**: {book['Genre']}")
                    st.write(f"**Stock**: {book['Stock']}")
                    st.write(f"**Sold**: {book['UnitsSold']}")
                    st.write(f"**Price**: ₹{book['Price']}")
                    st.write(f"**Revenue**: ₹{book['Revenue']}")
                    st.write("---")
                
                st.subheader("Purchase a Book")
                selected_title = st.selectbox("Select book to purchase", [book['Title'] for book in matches])
                quantity = st.number_input("Number of copies", min_value=1, value=1)
                
                if st.button("Purchase"):
                    for book in st.session_state.inventory:
                        if book['Title'].lower() == selected_title.lower():
                            if book['Stock'] >= quantity:
                                book['Stock'] -= quantity
                                book['UnitsSold'] += quantity
                                book['Revenue'] = round(book['UnitsSold'] * book['Price'], 2)
                                save_inventory(st.session_state.inventory)
                                st.success(f"{quantity} copies of '{book['Title']}' purchased successfully.")
                            else:
                                st.error(f"Not enough stock. Only {book['Stock']} available.")
                            break
            else:
                st.warning("No books found.")
        else:
            st.error("Please enter a search value.")

# Add New Book Page
elif page == "Add New Book":
    st.header("Add New Book to Inventory")
    with st.form("add_book_form"):
        new_title = st.text_input("Book Title")
        new_author = st.text_input("Author Name")
        new_genre = st.text_input("Genre")
        new_price = st.number_input("Price (₹)", min_value=0.0, step=0.01)
        new_stock = st.number_input("Number of Copies", min_value=0, step=1)
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if new_title and new_author and new_genre and new_price > 0 and new_stock >= 0:
                new_book = {
                    'Title': new_title,
                    'Author': new_author,
                    'Genre': new_genre,
                    'Price': new_price,
                    'Stock': new_stock,
                    'UnitsSold': 0,
                    'Revenue': 0.0
                }
                st.session_state.inventory.append(new_book)
                save_inventory(st.session_state.inventory)
                st.success(f"'{new_title}' added successfully to inventory!")
            else:
                st.error("Please fill in all fields with valid values.")

# Visualizations Page
elif page == "Visualizations":
    st.header("Inventory Visualizations")
    df = pd.DataFrame(st.session_state.inventory)
    
    # Bar Chart: Stock Levels by Book
    st.subheader("Stock Levels by Book")
    fig_stock = px.bar(df, x='Title', y='Stock', title="Books in Stock",
                       color='Stock', color_continuous_scale='Viridis')
    fig_stock.update_layout(xaxis_title="Book Title", yaxis_title="Stock",
                           xaxis_tickangle=45, showlegend=False)
    st.plotly_chart(fig_stock, use_container_width=True)
    
    # Pie Chart: Genre Distribution
    st.subheader("Genre Distribution")
    genre_counts = df['Genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']
    fig_genre = px.pie(genre_counts, names='Genre', values='Count',
                       title="Distribution of Books by Genre",
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_genre, use_container_width=True)
    
    # Table: Top 5 Revenue-Generating Books
    st.subheader("Top 5 Revenue-Generating Books")
    top_revenue = df.nlargest(5, 'Revenue')[['Title', 'Author', 'Revenue', 'UnitsSold']]
    top_revenue['Revenue'] = top_revenue['Revenue'].map('₹{:,.2f}'.format)
    st.table(top_revenue)

    # Interesting Fact
    st.subheader("Interesting Fact")
    top_book = df.loc[df['Revenue'].idxmax()]
    st.write(f"The book '{top_book['Title']}' by {top_book['Author']} has generated the highest revenue at ₹{top_book['Revenue']:,.2f}, with {top_book['UnitsSold']} copies sold, highlighting its popularity in the {top_book['Genre']} genre.")