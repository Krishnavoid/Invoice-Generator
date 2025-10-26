import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

items = []

def add_item():
    name = entry_item.get()
    qty = entry_qty.get()
    price = entry_price.get()
    if name and qty and price:
        items.append((name, int(qty), float(price)))
        listbox.insert(tk.END, f"{name} - {qty} x ₹{price}")
        entry_item.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_price.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Enter all item details")

def generate_invoice():
    if not items:
        messagebox.showerror("Error", "No items added")
        return
    client = entry_client.get()
    address = entry_address.get()
    if not client or not address:
        messagebox.showerror("Error", "Enter client details")
        return
    filename = f"Invoice_{client.replace(' ','_')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("Invoice")
    width, height = A4
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 800, "INVOICE")
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(50, 750, f"Client Name: {client}")
    c.drawString(50, 730, f"Address: {address}")
    y = 690
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Item")
    c.drawString(250, y, "Quantity")
    c.drawString(350, y, "Price")
    c.drawString(450, y, "Total")
    c.line(50, y-5, 550, y-5)
    total = 0
    y -= 30
    for item, qty, price in items:
        line_total = qty * price
        c.setFont("Helvetica", 12)
        c.drawString(50, y, item)
        c.drawString(250, y, str(qty))
        c.drawString(350, y, f"{price:.2f}")
        c.drawString(450, y, f"{line_total:.2f}")
        y -= 20
        total += line_total
    c.line(50, y-5, 550, y-5)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y-25, "Grand Total:")
    c.drawString(450, y-25, f"{total:.2f}")
    c.save()
    messagebox.showinfo("Success", f"Invoice saved as {filename}")
    items.clear()
    listbox.delete(0, tk.END)

root = tk.Tk()
root.title("InvoiceGenUI - Invoice Generator")
root.geometry("500x550")

tk.Label(root, text="Client Name").pack()
entry_client = tk.Entry(root, width=40)
entry_client.pack()

tk.Label(root, text="Client Address").pack()
entry_address = tk.Entry(root, width=40)
entry_address.pack()

tk.Label(root, text="Item Name").pack()
entry_item = tk.Entry(root, width=30)
entry_item.pack()

tk.Label(root, text="Quantity").pack()
entry_qty = tk.Entry(root, width=30)
entry_qty.pack()

tk.Label(root, text="Price").pack()
entry_price = tk.Entry(root, width=30)
entry_price.pack()

tk.Button(root, text="Add Item", command=add_item, bg="#4CAF50", fg="white").pack(pady=5)
listbox = tk.Listbox(root, width=60, height=10)
listbox.pack(pady=10)

tk.Button(root, text="Generate Invoice", command=generate_invoice, bg="#2196F3", fg="white").pack(pady=10)

root.mainloop()
