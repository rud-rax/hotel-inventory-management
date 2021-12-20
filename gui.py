from tkinter import *
from tkinter import messagebox
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
root.geometry('900x900+10+10')
root.title('HOTEL INVENTORY')
root.iconbitmap(r"images/hotel4.ico")


# def plusClick(n): print('+', n)
# def minusClick(n): print('-', n)


# def rn(x): return x


x_start = 20
y_start = 10

# STOCK FRAME STARTS -- >
stock_frame = LabelFrame(
    root, text='Stock', padx=10, pady=8)
stock_frame.place(x=x_start, y=y_start)

label_pad = (10, 6)
stock_unit_pad = (10, 2)
button_w = 5

stock_namelabels = []
stock_quantityboxes = []
stock_ppqs = []

plus_buttons = []
minus_buttons = []
input_entries = []

item_dict = {}


def getItems():
    item = clicked.get()
    # print(item_dict[item][0])
    item_dict[item][1] = quantity_entry.get()
    # make corrections
    # print(item_dict.values())


def orderItems():
    print('ORDER FUNCTION ---- ')

    orderlist = list(item_dict.values())
    print(orderlist)

    totalCost = rc.orderItems(orderlist)
    inventory = rc.displayInventory()
    updateInventory(inventory)

    ans = messagebox.askyesno(
        'TOTAL EXPENSE', f"The total order cost is {totalCost} \n Are you sure you want to place the order ?")

    if not ans:
        rc.discardItems(orderlist)
        inventory = rc.displayInventory()
        updateInventory(inventory)


def changePPQ():

    new_ppq = ppq_entry.get()
    id = item_dict[clicked1.get()][0]

    rc.changeItemPPQ(id, new_ppq)

    inventory = rc.displayInventory()
    updateInventory(inventory)


def changeName(): pass


# GET VALUES FROM DATABASE
inventory = rc.displayInventory()

NAME_label = Label(stock_frame, text='NAME').grid(
    row=0, column=0, padx=label_pad[0], pady=label_pad[1])
QUANTITY_label = Label(stock_frame, text='QUANTITY').grid(
    row=0, column=1, padx=label_pad[0], pady=label_pad[1])
PPQ_label = Label(stock_frame, text='PRICE PER QUANTITY').grid(
    row=0, column=2, padx=label_pad[0], pady=label_pad[1])

# PLUS_label = Label(stock_frame, text='Increase').grid(
#     row=0, column=3, padx=label_pad[0], pady=label_pad[1])
# OQ_label = Label(stock_frame, text='ORDER QUANTITY').grid(
#     row=0, column=4, padx=label_pad[0], pady=label_pad[1])
# MINUS_label = Label(stock_frame, text='Decrease').grid(
#     row=0, column=5, padx=label_pad[0], pady=label_pad[1])


def updateInventory(inventory):

    i = 1
    for id, name, quantity, ppq in inventory:

        stock_namelabels.append(Label(stock_frame, text=name).grid(
            row=i, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

        stock_quantityboxes.append(
            Label(stock_frame, text=quantity).grid(row=i, column=1, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

        stock_ppqs.append(Label(stock_frame, text=ppq).grid(
            row=i, column=2, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

        # plus_buttons.append(Button(stock_frame, text="+", command=lambda: plusClick(id), width=button_w).grid(
        #     row=i, column=3, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

        # input_entries.append(
        #     Entry(stock_frame).grid(row=i, column=4, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

        # minus_buttons.append(Button(stock_frame, text='-', command=lambda: minusClick(id), width=button_w).grid(
        #     row=i, column=5, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

        item_dict[name] = [id, 0, ppq]

        i += 1


updateInventory(inventory)


x_start += 420

order_unitpad = (10, 4)

order_frame = LabelFrame(
    root, text='Order', padx=10, pady=8)
order_frame.place(x=x_start, y=y_start)

iv = list(item_dict.keys())

clicked = StringVar()
clicked.set(iv[0])

orderSelect = OptionMenu(order_frame, clicked, *iv)
orderSelect.grid(row=0, column=0, padx=order_unitpad[0], pady=order_unitpad[1])

quantity_entry = Entry(order_frame, width=13)
quantity_entry.grid(
    row=0, column=1, padx=order_unitpad[0], pady=order_unitpad[1])

quantity_entry.insert(0, item_dict[clicked.get()][1])

getq_button = Button(order_frame, text="GET",
                     width=5, command=getItems)
getq_button.grid(row=0, column=2, padx=order_unitpad[0], pady=order_unitpad[1])


orderButton = Button(order_frame, text="ORDER ITEMS",
                     width=35, command=orderItems)
orderButton.grid(row=1, column=0, columnspan=3,
                 padx=order_unitpad[0], pady=order_unitpad[1])


# MANAGE PPQ FRAME

y_start += 120
manage_frame = LabelFrame(
    root, text='Manage Price Per Quantity', padx=10, pady=8)
manage_frame.place(x=x_start, y=y_start)

clicked1 = StringVar()
clicked1.set(iv[0])


ppqSelect = OptionMenu(manage_frame, clicked1, *iv)
ppqSelect.grid(row=0, column=0, padx=order_unitpad[0], pady=order_unitpad[1])

ppq_entry = Entry(manage_frame, width=24)
ppq_entry.grid(
    row=0, column=1, padx=order_unitpad[0], pady=order_unitpad[1])

ppq_entry.insert(0, item_dict[clicked.get()][1])

ppq_button = Button(manage_frame, text="CHANGE",
                    width=35, command=changePPQ)
ppq_button.grid(row=1, column=0, columnspan=2,
                padx=order_unitpad[0], pady=order_unitpad[1])

# CHANGE NAME FRAME


# y_start += 120
# name_frame = LabelFrame(
#     root, text='Change Name', padx=10, pady=8)
# manage_frame.place(x=x_start, y=y_start)

# clicked2 = StringVar()
# clicked2.set(iv[0])


# nameSelect = OptionMenu(name_frame, clicked2, *iv)
# nameSelect.grid(row=0, column=0, padx=order_unitpad[0], pady=order_unitpad[1])

# name_entry = Entry(name_frame, width=24)
# name_entry.grid(
#     row=0, column=1, padx=order_unitpad[0], pady=order_unitpad[1])

# name_entry.insert(0, item_dict[clicked.get()][1])

# name_button = Button(name_frame, text="CHANGE",
#                     width=35, command=changeName)
# name_button.grid(row=1, column=0, columnspan=2,
#                 padx=order_unitpad[0], pady=order_unitpad[1])


# RECIPE FRAME
# y_start -= 120
# x_start += 330


# recipe_frame = LabelFrame(root, text='Recipes',
#                           padx=label_pad[0], pady=label_pad[1])
# recipe_frame.place(x=x_start, y=y_start)

# rl1 = Label(recipe_frame, text='Mashroom Masala Curry')
# rl1.grid(row=1, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])
# rl1i = Button(recipe_frame, text=" + ", width=3)
# rl1i.grid(row=1, column=1, padx=stock_unit_pad[0], pady=stock_unit_pad[1])
# rl1d = Button(recipe_frame, text=" - ", width=3)
# rl1d.grid(row=1, column=2, padx=stock_unit_pad[0], pady=stock_unit_pad[1])
# rl1e = Entry(recipe_frame)
# rl1e.grid(row=1, column=3, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl2 = Label(recipe_frame, text='Aloo Matar')
# rl2.grid(row=2, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl3 = Label(recipe_frame, text='Palak Paneer')
# rl3.grid(row=3, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl4 = Label(recipe_frame, text='Fish Fry')
# rl4.grid(row=4, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl5 = Label(recipe_frame, text='Tandoori Chicken')
# rl5.grid(row=5, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])


# rl6 = Label(recipe_frame, text='Fish Curry')
# rl6.grid(row=6, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl7 = Label(recipe_frame, text='Chicken Masala')
# rl7.grid(row=7, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl8 = Label(recipe_frame, text='Egg Masala Curry')
# rl8.grid(row=8, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl9 = Label(recipe_frame, text='Chicken Chilli')
# rl9.grid(row=9, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl10 = Label(recipe_frame, text='Chicken Tikka')
# rl10.grid(row=10, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])


# rl11 = Label(recipe_frame, text='Chicken Dum Biryani')
# rl11.grid(row=11, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl12 = Label(recipe_frame, text='Kadhai Paneer')
# rl12.grid(row=12, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl13 = Label(recipe_frame, text='Shahi Paneer')
# rl13.grid(row=13, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl14 = Label(recipe_frame, text='Veg Pulao')
# rl14.grid(row=14, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl15 = Label(recipe_frame, text='Mix Veg')
# rl15.grid(row=15, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])


# rl16 = Label(recipe_frame, text='Dal Tadka')
# rl16.grid(row=16, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl17 = Label(recipe_frame, text='Veg Kolhapuri')
# rl17.grid(row=17, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl18 = Label(recipe_frame, text='Paneer Do Pyaza')
# rl18.grid(row=18, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl19 = Label(recipe_frame, text='Paneer Bhurji')
# rl19.grid(row=19, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl20 = Label(recipe_frame, text='Matar Paneer')
# rl20.grid(row=20, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])


# rl21 = Label(recipe_frame, text='Garlic Naan')
# rl21.grid(row=21, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl22 = Label(recipe_frame, text='Pyaaz Paratha')
# rl22.grid(row=22, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

# rl23 = Label(recipe_frame, text='Bhindi Masala')
# rl23.grid(row=23, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1])


# recipe_button = Button(recipe_frame, text='Make', width=55)
# recipe_button.grid(
#     row=0, column=0, columnspan=4, padx=label_pad[0], pady=label_pad[1])

root.mainloop()
