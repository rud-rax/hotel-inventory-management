from tkinter import *
from PIL import ImageTk, Image
import mysql.connector as myc
import inventoryConnect as ic

# DATABASE VARIABLES
lhost = "localhost"
luser = "root"
lpasswd = "rudu101519"
database_name = "hotel_database"

# DATABASE CONNECTION
hotelconn = myc.connect(
    host=lhost, user=luser, passwd=lpasswd, database=database_name
)

rc = ic.Recipe(hotelconn)

root = Tk()
root.geometry('1600x900+10+10')
root.title('HOTEL INVENTORY')
root.iconbitmap(
    r"images/hotel4.ico")


def plusClick(n): print('+', n)
def minusClick(n): print('-', n)


def rn(x): return x


# STOCK FRAME STARTS -- >
stock_frame = LabelFrame(
    root, text='Stock', padx=10, pady=8)
stock_frame.grid(row=0, column=0, padx=10, pady=5)

label_pad = (10, 6)
stock_unit_pad = (10, 2)
button_w = 5

stock_namelabels = []
stock_quantityboxes = []
stock_ppqs = []

plus_buttons = []
minus_buttons = []
input_entries = []

# GET VALUES FROM DATABASE
inventory = rc.displayInventory()

NAME_label = Label(stock_frame, text='NAME').grid(
    row=0, column=0, padx=label_pad[0], pady=label_pad[1])
QUANTITY_label = Label(stock_frame, text='QUANTITY').grid(
    row=0, column=1, padx=label_pad[0], pady=label_pad[1])
PPQ_label = Label(stock_frame, text='PRICE PER QUANTITY').grid(
    row=0, column=2, padx=label_pad[0], pady=label_pad[1])

PLUS_label = Label(stock_frame, text='Increase').grid(
    row=0, column=3, padx=label_pad[0], pady=label_pad[1])
OQ_label = Label(stock_frame, text='ORDER QUANTITY').grid(
    row=0, column=4, padx=label_pad[0], pady=label_pad[1])
MINUS_label = Label(stock_frame, text='Decrease').grid(
    row=0, column=5, padx=label_pad[0], pady=label_pad[1])

i = 1
for id, name, quantity, ppq in inventory:

    stock_namelabels.append(Label(stock_frame, text=name).grid(
        row=i, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

    stock_quantityboxes.append(
        Label(stock_frame, text=quantity).grid(row=i, column=1, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

    stock_ppqs.append(Label(stock_frame, text=ppq).grid(
        row=i, column=2, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

    plus_buttons.append(Button(stock_frame, text="+", command=lambda: plusClick(id), width=button_w).grid(
        row=i, column=3, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

    input_entries.append(
        Entry(stock_frame).grid(row=i, column=4, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

    minus_buttons.append(Button(stock_frame, text='-', command=lambda: minusClick(id), width=button_w).grid(
        row=i, column=5, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

    i += 1


root.mainloop()