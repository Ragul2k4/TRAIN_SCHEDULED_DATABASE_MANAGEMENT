import tkinter as tk
from tkinter import ttk
import mysql.connector

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1214',
    'database': 'trains',
    'auth_plugin': 'mysql_native_password'  # For MySQL 8.0+
}

# Function to load schedule based on district selection
def load_schedule():
    selected_district = district_combo.get()
    
    # Clear previous data in treeview
    for row in schedule_tree.get_children():
        schedule_tree.delete(row)
    
    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Retrieve schedule data
        query = f"SELECT train_no, train_name, type, time FROM {selected_district}"
        cursor.execute(query)
        schedule_data = cursor.fetchall()
        
        # Insert data into treeview
        for row in schedule_data:
            schedule_tree.insert('', 'end', values=(row['train_no'], row['train_name'], row['type'], row['time']))
        
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Create main window
root = tk.Tk()
root.title("Train Schedule")

# Create UI elements
frame = ttk.Frame(root, padding="30")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# District selection dropdown
ttk.Label(frame, text="Select District:").grid(column=0, row=0, padx=10, pady=10)
district_combo = ttk.Combobox(frame, width=30, state='readonly')
district_combo['values'] = ('Chennai', 'Chengalpattu', 'Tiruvallur', 'Kanchipuram', 'Vellore', 'Tiruvannamalai', 'Namakkal', 'Dharmapuri', 'Salem', 'Cuddalore', 'Viluppuram', 'Erode', 'Coimbatore', 'Tiruppur', 'Nilgiris', 'Perambalur', 'Karur', 'Tiruchirappalli', 'Thanjavur', 'Tiruvarur', 'Nagapattinam', 'Pudukkottai', 'Erode', 'Dindigul', 'Madurai', 'Theni', 'Ariyalur', 'Sivaganga', 'Ramanathapuram', 'Virudhunagar', 'Thoothukudi', 'Krishnagiri', 'Tirunelveli', 'Ranipet', 'Kanyakumari', 'Tenkasi', 'Mayiladuthurai', 'Tirupathur')
district_combo.grid(column=1, row=0, padx=10, pady=10)

# Show Schedule button
show_schedule_button = ttk.Button(frame, text="Show Schedule", command=load_schedule)
show_schedule_button.grid(column=2, row=0, padx=10, pady=10)

# Treeview to display schedule
columns = ('Train Number', 'Train Name', 'Type', 'Departure Time')
schedule_tree = ttk.Treeview(frame, columns=columns, show='headings')
for col in columns:
    schedule_tree.heading(col, text=col)
schedule_tree.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

# Start GUI main loop
root.mainloop()
