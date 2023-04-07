import os
import csv
import pyperclip
import tkinter as tk
from tkinter import ttk, messagebox

if not os.path.isfile("data.csv"):
    with open("data.csv", "w", newline="") as file:
        pass

# Define functions for data operations
def add_person():
    # Get data from entry fields
    id = id_entry.get()
    name = name_entry.get()
    phone = phone_entry.get()
    place = place_entry.get()
    birth = birth_entry.get()

    # Validate input
    if not id.isdigit():
        messagebox.showerror("Error", "The ID can be only a number.")
        return

    # Read data from csv file
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        person_list = list(reader)

    # Check if the ID already exists
    for person in person_list:
        if person[0] == id:
            messagebox.showerror("Error", "This ID already exists.")
            return

    if not id or not name or not phone or not place or not birth:
        messagebox.showerror("Error", "Fill all of the info.")
        return

    # Create a list of data
    person = [id, name, phone, place, birth]

    # Append data to csv file
    with open("data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(person)

    # Clear entry fields
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    place_entry.delete(0, tk.END)
    birth_entry.delete(0, tk.END)

    # Show success message
    messagebox.showinfo("Success", "The person has been saved.")

def modificar_persona():
    # Get ID of person to modify
    id_modify = edit_id_entry.get()

    # Validate that is a valid ID
    if not id_modify.isdigit():
        messagebox.showerror("Error", "The ID need to be a number.")
        return

    # Read data from csv file
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        person_list = list(reader)
    
    # Search a person in list
    person_modify = None
    for i, person in enumerate(person_list):
        if person[0] == id_modify:
            person_modify = person
            break

    # Validate that find a person
    if person_modify is None:
        messagebox.showerror("Error", "Can't find a person with that ID.")
        return

    # Obtain new values from fields
    new_name = edit_name_entry.get()
    new_place = edit_place_entry.get()
    new_phone = edit_phone_entry.get()
    new_birth = edit_birth_entry.get()

    # Validate that at least one field has been modified
    if not (new_name or new_place or new_phone or new_birth):
        messagebox.showerror("Error", "Enter at least one new value.")
        return

    # Maintain unmodified fields
    if not new_name:
        new_name = person_modify[1]

    if not new_phone:
        new_phone = person_modify[2]

    if not new_place:
        new_place = person_modify[3]
    
    if not new_birth:
        new_birth = person_modify[4]

    # Update fields
    person_modify[1] = new_name
    person_modify[2] = new_phone
    person_modify[3] = new_place
    person_modify[4] = new_birth

    # Update persons list
    person_list[i] = person_modify

    # Write the updated data to CSV
    with open("data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(person_list)

    # Clean input fields
    edit_id_entry.delete(0, tk.END)
    edit_name_entry.delete(0, tk.END)
    edit_place_entry.delete(0, tk.END)
    edit_phone_entry.delete(0, tk.END)
    edit_birth_entry.delete(0, tk.END)

    # Show success message
    messagebox.showinfo("Éxito", "The information has been updated.")

def fill_fields():
    id = edit_id_entry.get()

    if not id.isdigit():
        messagebox.showerror("Error", "The ID can be only a number.")
        return

    found = False
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == id:
                edit_name_entry.delete(0, tk.END)
                edit_name_entry.insert(0, row[1])
                edit_phone_entry.delete(0, tk.END)
                edit_phone_entry.insert(0, row[2])
                edit_place_entry.delete(0, tk.END)
                edit_place_entry.insert(0, row[3])
                edit_birth_entry.delete(0, tk.END)
                edit_birth_entry.insert(0, row[4])
                found = True
                break
    
    if not found:
        messagebox.showerror("Error", "Person not found.")

def delete_person():
    # Get id from entry field
    id = delete_id_entry.get()

    # Validate input
    if not id:
        messagebox.showerror("Error", "ID can't be empty.")
        return
    
    if not id.isdigit():
        messagebox.showerror("Error", "The ID can be only a number.")
        return

    # Read data from csv file
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        data = list(reader)

    # Get the length of the original data
    original_length = len(data)

    # Filter out the person with the given id
    data = list(filter(lambda x: x[0] != id, data))

    # Get the length of the filtered data
    filtered_length = len(data)

    # Check if at least one person was deleted
    if filtered_length == original_length:
        messagebox.showerror("Error", "Can't find a person with the specified ID to delete.")
        return

    # Write data back to csv file
    with open("data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    # Clear entry field
    delete_id_entry.delete(0, tk.END)

    # Show success message
    messagebox.showinfo("Success", "The person has been deleted.")

def search_person():
    # Get name or id from entry field
    query = search_entry.get()

    # Validate input
    if not query:
        messagebox.showerror("Error", "The search can't be empty.")
        return

    # Delete existing rows
    for row in search_table.get_children():
        search_table.delete(row)

    # Read data from csv file
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        data = list(reader)

    # Filter data by name or id
    data = list(filter(lambda x: query in x[0] or query in x[1], data))

    # If no results are found, show message
    if not data:
        messagebox.showinfo("Message", "No results.")
        return

    # Clear listbox
    for row in search_table.get_children():
        search_table.delete(row)

    # Insert filtered data into listbox
    for i, person in enumerate(data):
        search_table.insert(parent='', index=i, values=person)

def list_person():
    # Get filter criteria from entry fields
    filter_phone = filter_phone_entry.get()
    filter_place = filter_place_entry.get()
    filter_birth = filter_birth_entry.get()

    # Delete existing rows
    for row in list_table.get_children():
        list_table.delete(row)

    # Read data from csv file
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        data = list(reader)

    # Filter data by criteria
    if filter_phone:
        data = list(filter(lambda x: filter_phone in x[2], data))
    if filter_place:
        data = list(filter(lambda x: filter_place in x[3], data))
    if filter_birth:
        data = list(filter(lambda x: filter_birth in x[4], data))

    # Insert filtered data into treeview
    for i, person in enumerate(data):
        list_table.insert(parent='', index=i, values=person)
    if list_table.get_children() == ():
        messagebox.showinfo("Message", "No results.")

def copy_to_clipboard(value, label):
    pyperclip.copy(value)
    messagebox.showinfo("Copied", f"{label} copied to clipboard.")

def show_person_details(table_name):
    # Get the selected row
    selected_row = table_name.focus()

    # Get the person's details from the selected row
    person = table_name.item(selected_row, "values")

    # Create a new window to display the person's details
    details_window = tk.Toplevel(root)
    details_window.title("Person Details")

    # Add labels to display the person's details
    info_label = tk.Label(details_window, text="Click any data to copy it.")
    info_label.pack()

    id_label = tk.Label(details_window, text="ID: " + person[0])
    id_label.pack()
    id_label.bind("<Button-1>", lambda e: copy_to_clipboard(person[0], "ID"))
    name_label = tk.Label(details_window, text="Name: " + person[1])
    name_label.pack()
    name_label.bind("<Button-1>", lambda e: copy_to_clipboard(person[1], "Name"))
    phone_label = tk.Label(details_window, text="Phone: " + person[2])
    phone_label.pack()
    phone_label.bind("<Button-1>", lambda e: copy_to_clipboard(person[2], "Phone"))
    place_label = tk.Label(details_window, text="Place: " + person[3])
    place_label.pack()
    place_label.bind("<Button-1>", lambda e: copy_to_clipboard(person[3], "Place"))
    birth_label = tk.Label(details_window, text="Birth: " + person[4])
    birth_label.pack()
    birth_label.bind("<Button-1>", lambda e: copy_to_clipboard(person[4], "Birth"))
    details_window.grab_set()  # Set focus to details window, preventing user interaction until message box is closed

# Create root window
root = tk.Tk()
root.title("Personal Data Manager")
root.resizable(False, False)

# Create notebook widget for tabs
notebook = ttk.Notebook(root)
notebook.pack()

# Create frames for tabs
add_frame = tk.Frame(notebook)
edit_person_tab = ttk.Frame(notebook)
delete_frame = tk.Frame(notebook)
search_frame = tk.Frame(notebook)
list_frame = tk.Frame(notebook)

# Add frames to notebook
notebook.add(add_frame, text="Add Person")
notebook.add(edit_person_tab, text="Modify person")
notebook.add(delete_frame, text="Delete Person")
notebook.add(search_frame, text="Search Person")
notebook.add(list_frame, text="List People")

# Create labels and entry fields for add tab
id_label = tk.Label(add_frame, text="ID:")
id_label.grid(row=0, column=0)
id_entry = ttk.Entry(add_frame, width=40)
id_entry.grid(row=0, column=1)

name_label = tk.Label(add_frame, text="Name:")
name_label.grid(row=1, column=0)
name_entry = ttk.Entry(add_frame, width=40)
name_entry.grid(row=1, column=1)

phone_label = tk.Label(add_frame, text="Phone:")
phone_label.grid(row=2, column=0)
phone_entry = ttk.Entry(add_frame, width=40)
phone_entry.grid(row=2, column=1)

place_label = tk.Label(add_frame, text="Place:")
place_label.grid(row=3, column=0)
place_entry = ttk.Entry(add_frame, width=40)
place_entry.grid(row=3, column=1)

birth_label = tk.Label(add_frame, text="Birth:")
birth_label.grid(row=4, column=0)
birth_entry = ttk.Entry(add_frame, width=40)
birth_entry.grid(row=4, column=1)

# Create button for add tab
add_button = ttk.Button(add_frame, text="Add", command=add_person)
add_button.grid(row=5, columnspan=2)

# Create fields to modify person
edit_id_label = ttk.Label(edit_person_tab, text="ID:")
edit_id_label.grid(column=0, row=0)
edit_id_entry = ttk.Entry(edit_person_tab, width=40)
edit_id_entry.grid(column=1, row=0)
edit_name_label = ttk.Label(edit_person_tab, text="Name:")
edit_name_label.grid(column=0, row=1)
edit_name_entry = ttk.Entry(edit_person_tab, width=40)
edit_name_entry.grid(column=1, row=1)
edit_phone_label = ttk.Label(edit_person_tab, text="Phone:")
edit_phone_label.grid(column=0, row=2)
edit_phone_entry = ttk.Entry(edit_person_tab, width=40)
edit_phone_entry.grid(column=1, row=2)
edit_place_label = ttk.Label(edit_person_tab, text="Place:")
edit_place_label.grid(column=0, row=3)
edit_place_entry = ttk.Entry(edit_person_tab, width=40)
edit_place_entry.grid(column=1, row=3)
edit_birth_label = ttk.Label(edit_person_tab, text="Birth:")
edit_birth_label.grid(column=0, row=4)
edit_birth_entry = ttk.Entry(edit_person_tab, width=40)
edit_birth_entry.grid(column=1, row=4)

# Create buttom to modify person
edit_person_button = ttk.Button(edit_person_tab, text="Modify person", command=modificar_persona)
edit_person_button.grid(column=0, row=5)

fill_button = ttk.Button(edit_person_tab, text="Fill with actual info", command=fill_fields)
fill_button.grid(column=1, row=5)

# Create label and entry field for delete tab
delete_id_label = tk.Label(delete_frame, text="ID:")
delete_id_label.pack()
delete_id_entry = ttk.Entry(delete_frame, width=40)
delete_id_entry.pack()

# Create button for delete tab
delete_button = ttk.Button(delete_frame, text="Delete", command=delete_person)
delete_button.pack()

# Create label and entry field for search tab
search_label = tk.Label(search_frame, text="Name or ID:")
search_label.pack()
search_entry = ttk.Entry(search_frame, width=40)
search_entry.pack()

# Create button for search tab
search_button = ttk.Button(search_frame, text="Search", command=search_person)
search_button.pack()

# Create table for list tab
search_table = ttk.Treeview(search_frame)
search_table["columns"] = ("ID Number", "Name", "Phone", "Place", "Birth")

search_table.column("#0", width=0, stretch=tk.NO)
search_table.column("ID Number", anchor=tk.CENTER, width=75)
search_table.column("Name", anchor=tk.CENTER, width=200)
search_table.column("Phone", anchor=tk.CENTER, width=100)
search_table.column("Place", anchor=tk.CENTER, width=75)
search_table.column("Birth", anchor=tk.CENTER, width=75)

search_table.heading("#0", text="", anchor=tk.CENTER)
search_table.heading("ID Number", text="ID Number", anchor=tk.CENTER)
search_table.heading("Name", text="Name", anchor=tk.CENTER)
search_table.heading("Phone", text="Phone", anchor=tk.CENTER)
search_table.heading("Place", text="Place", anchor=tk.CENTER)
search_table.heading("Birth", text="Birth", anchor=tk.CENTER)

search_table.bind("<Double-1>", lambda event: show_person_details(search_table))
search_table.pack(expand=tk.YES, fill=tk.BOTH)

# Create labels and entry fields for filter criteria in list tab
filter_phone_label = tk.Label(list_frame, text="Filter Listing by Some Data (Leave any empty if don't want to use):")
filter_phone_label.grid(row=1, columnspan=2)

filter_phone_label = tk.Label(list_frame, text="Phone:")
filter_phone_label.grid(row=2, column=0)
filter_phone_entry = ttk.Entry(list_frame, width=40)
filter_phone_entry.grid(row=2, column=1)

filter_place_label = tk.Label(list_frame, text="Place:")
filter_place_label.grid(row=3, column=0)
filter_place_entry = ttk.Entry(list_frame, width=40)
filter_place_entry.grid(row=3, column=1)

filter_birth_label = tk.Label(list_frame, text="Birth:")
filter_birth_label.grid(row=4, column=0)
filter_birth_entry = ttk.Entry(list_frame, width=40)
filter_birth_entry.grid(row=4, column=1)

# Create button for list tab
list_button = ttk.Button(list_frame, text="List", command=list_person)
list_button.grid(row=5, columnspan=2)

# Create table for list tab
list_table = ttk.Treeview(list_frame)
list_table["columns"] = ("ID Number", "Name", "Phone", "Place", "Birth")

list_table.column("#0", width=0, stretch=tk.NO)
list_table.column("ID Number", anchor=tk.CENTER, width=75)
list_table.column("Name", anchor=tk.CENTER, width=200)
list_table.column("Phone", anchor=tk.CENTER, width=100)
list_table.column("Place", anchor=tk.CENTER, width=75)
list_table.column("Birth", anchor=tk.CENTER, width=75)

list_table.heading("#0", text="", anchor=tk.CENTER)
list_table.heading("ID Number", text="ID Number", anchor=tk.CENTER)
list_table.heading("Name", text="Name", anchor=tk.CENTER)
list_table.heading("Phone", text="Phone", anchor=tk.CENTER)
list_table.heading("Place", text="Place", anchor=tk.CENTER)
list_table.heading("Birth", text="Birth", anchor=tk.CENTER)

list_table.bind("<Double-1>", lambda event: show_person_details(list_table))
list_table.grid(row=6, columnspan=2)

# Start main loop
root.mainloop()