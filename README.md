Book Inventory Management System

A Streamlit-based web application for managing a book inventory. This project allows users to search for books, purchase copies, add new books to the inventory, and visualize inventory data through interactive charts.

Features



Search & Purchase: Search books by Title, Author, or Genre, view results in a table, and purchase books with stock validation.


Add Books: Add new books to the inventory via a user-friendly form.


Data Visualizations:


Bar chart of stock levels by book title, colored by genre.



Pie chart of revenue distribution by genre.



Full inventory table display.



Data Persistence: Inventory is stored in a CSV file (inventory.csv) for persistent storage.



Professional UI: Built with Streamlit for an intuitive and responsive interface.

Requirements


Python 3.8+


Packages listed in requirements.txt:

streamlit==1.39.0
pandas==2.2.3
plotly==5.24.1

Installation



Clone the repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name



Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate



Install dependencies:

pip install -r requirements.txt



Ensure an inventory.csv file exists in the project directory with headers: Title,Author,Genre,Price,Stock,UnitsSold,Revenue. If not, the app will create an empty one on first run.

Usage





Run the Streamlit app:

streamlit run app.py



Open the provided URL : https://bookinventory.streamlit.app/



Use the app:




Search & Purchase Tab: Search for books and buy copies.



Add Book Tab: Add new books to the inventory.



Visualizations Tab: View stock levels, revenue by genre, and the full inventory.

Project Structure

├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── inventory.csv       # Inventory data file (created automatically if missing)
└── README.md           # This file






License

This project is licensed under the MIT License. See the LICENSE file for details.

Contact

For issues or questions, please open an issue on GitHub or contact anilbhaskar0105@gmail.com
