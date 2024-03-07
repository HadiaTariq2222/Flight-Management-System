import tkinter as tk
from tkinter import messagebox
import sqlite3
import uuid  # For generating unique IDs

class AirlineManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Management System")
        
        self.conn = sqlite3.connect('airline.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bookings
                            (id TEXT PRIMARY KEY, name TEXT, flight TEXT)''')
        
        self.current_step = 1
        
        self.show_step()
    
    def show_step(self):
        if self.current_step == 1:
            self.booking_step()
        elif self.current_step == 2:
            self.cancellation_step()
        elif self.current_step == 3:
            self.payment_step()
    
    # ...
    def booking_step(self):
        self.clear_frame()
        
        self.label = tk.Label(self.root, text="Step 1: Booking Flight", fg="blue", font=("Helvetica", 16, "bold"))
        self.label.pack(pady=20)
        
        self.name_label = tk.Label(self.root, text="Name:", fg="green", font=("Arial", 12))
        self.name_label.pack()
        
        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack(pady=10, padx=20)
        
        self.flight_label = tk.Label(self.root, text="Flight:", fg="green", font=("Arial", 12))
        self.flight_label.pack()
        
        self.flight_entry = tk.Entry(self.root, font=("Arial", 12))
        self.flight_entry.pack(pady=10, padx=20)
        
        self.next_button = tk.Button(self.root, text="Next", command=self.book_and_next, bg="orange", fg="white", font=("Arial", 14))
        self.next_button.pack(pady=20)
# ...

    
    def cancellation_step(self):
        self.clear_frame()
        
        self.label = tk.Label(self.root, text="Step 2: Cancellation Flight", fg="blue", font=("Helvetica", 16, "bold"))
        self.label.pack(pady=20)
        
        self.name_label = tk.Label(self.root, text="Name:", fg="green", font=("Arial", 12))
        self.name_label.pack()
        
        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack(pady=10, padx=20)
        
        self.cancel_button = tk.Button(self.root, text="Cancel Flight", command=self.cancel_flight, bg="red", fg="white", font=("Arial", 14))
        self.cancel_button.pack(pady=20)
        
        self.prev_button = tk.Button(self.root, text="Previous", command=self.prev_step, bg="gray", fg="white", font=("Arial", 12))
        self.prev_button.pack()
        self.next_button = tk.Button(self.root, text="Next", command=self.next_step, bg="green", fg="white", font=("Arial", 12))
        self.next_button.pack()
    
    def payment_step(self):
        self.clear_frame()
        
        self.label = tk.Label(self.root, text="Step 3: Payment of Ticket", fg="blue", font=("Helvetica", 16, "bold"))
        self.label.pack(pady=20)
        
        self.name_label = tk.Label(self.root, text="Name:", fg="green", font=("Arial", 12))
        self.name_label.pack()
        
        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack(pady=10, padx=20)
        
        self.pay_button = tk.Button(self.root, text="Pay Ticket", command=self.pay_ticket, bg="blue", fg="white", font=("Arial", 14))
        self.pay_button.pack(pady=20)
        
        self.prev_button = tk.Button(self.root, text="Previous", command=self.prev_step, bg="gray", fg="white", font=("Arial", 12))
        self.prev_button.pack()
    
    
    def next_step(self):
        if self.current_step < 3:
            self.current_step += 1
            self.show_step()
    
    def prev_step(self):
        if self.current_step > 1:
            self.current_step -= 1
            self.show_step()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def book_and_next(self):
        name = self.name_entry.get()
        flight = self.flight_entry.get()
        
        if name and flight:
            booking_id = str(uuid.uuid4())  # Generate a unique ID for the booking
            self.cursor.execute("INSERT INTO bookings (id, name, flight) VALUES (?, ?, ?)", (booking_id, name, flight))
            self.conn.commit()
            messagebox.showinfo("Booking", "Flight booked successfully!")
            self.next_step()
        else:
            messagebox.showerror("Error", "Name and flight fields are required.")
    def cancel_flight(self):
        name = self.name_entry.get()
        
        if name:
            self.cursor.execute("DELETE FROM bookings WHERE name = ?", (name,))
            self.conn.commit()
            messagebox.showinfo("Cancellation", "Flight cancelled successfully!")
        else:
            messagebox.showerror("Error", "Name field is required.")
    
    def pay_ticket(self):
        name = self.name_entry.get()
        
        if name:
            self.cursor.execute("SELECT flight FROM bookings WHERE name = ?", (name,))
            flight = self.cursor.fetchone()
            if flight:
                messagebox.showinfo("Payment", f"Payment successful for flight: {flight[0]}")
            else:
                messagebox.showerror("Error", "No booking found for the provided name.")
        else:
            messagebox.showerror("Error", "Name field is required.")
    
    

if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineManagementApp(root)
    root.mainloop()
