from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Azure SQL Database connection string
# connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:datasql.database.windows.net,1433;Initial Catalog=AssignmentDB;Persist Security Info=False;User ID=sqladmin;Password={your_password};MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;'
connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:datasql.database.windows.net,1433;Database=AssignmentDB;Uid=sqladmin;Pwd={@gp#1234};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Function to initialize database
def initialize_database():
    conn = pyodbc.connect(connection_string)
    conn.close()


# Function to add product to the database
def add_product(name, description, price, stock_quantity):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Products (Name, Description, Price, StockQuantity)
                     VALUES (?, ?, ?, ?)''', (name, description, price, stock_quantity))
    conn.commit()
    conn.close()

# Function to delete product from the database
def delete_product(product_id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Products WHERE ProductID = ?', (product_id,))
    conn.commit()
    conn.close()

# Route to handle deleting a product
@app.route('/delete_product', methods=['POST'])
def delete_product_route():
    product_id = request.form['product_id']
    delete_product(product_id)
    return redirect('/products')

# Route to display index.html and handle adding product
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product_route():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock_quantity = int(request.form['stock_quantity'])
        add_product(name, description, price, stock_quantity)
        return redirect('/products')
    elif request.method == 'GET':
        return render_template('index.html')  # Assuming add_product.html is the template for adding a product


# Route to display products.html and fetch products from database
@app.route('/products')
def products():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
