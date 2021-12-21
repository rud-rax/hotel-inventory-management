from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector as myc
import inventoryConnect as ic
import recipeConnect as ric

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

recipeOrderList = []


class RecipeItem():
    def __init__(self, id, name, row):
        self.id = id
        self.name = name

        self.recipeLabel = Label(recipe_frame, text=self.name)
        self.recipeLabel.grid(row=row, column=0)

        # self.increaseButton = Button(recipe_frame, text=" + ",
        #                              width=3, command=self.increaseQ)
        # self.increaseButton.grid(row=row, column=1,
        #                          padx=stock_unit_pad[0], pady=stock_unit_pad[1])

        # self.decreaseButton = Button(recipe_frame, text=" - ",
        #                              width=3, command=self.decreseQ)
        # self.decreaseButton.grid(row=row, column=2,
        #                          padx=stock_unit_pad[0], pady=stock_unit_pad[1])

        self.quantityEntry = Entry(recipe_frame)
        self.quantityEntry.grid(row=row, column=1,
                                padx=stock_unit_pad[0], pady=stock_unit_pad[1])

        self.addButton = Button(
            recipe_frame, text='ADD', command=self.print_id)
        self.addButton.grid(row=row, column=2,
                            padx=stock_unit_pad[0], pady=stock_unit_pad[1])

        self.refresh_recipe()

    def refresh_recipe(self):
        self.q = 0
        self.quantityEntry.delete(0, last=len(self.quantityEntry.get()))
        self.quantityEntry.insert(0, 0)

    def print_id(self):
        self.q = self.quantityEntry.get()
        print(f"{self.id} -  {self.name} --> {self.q}")
        recipeOrderList.append((self.id, self.q))

    # def increaseQ(self):
    #     self.q = int(self.quantityEntry.get())
    #     self.q += 1
    #     self.quantityEntry.delete(0)
    #     self.quantityEntry.insert(0, self.q)

    # def decreseQ(self):
    #     self.q = int(self.quantityEntry.get())
    #     self.q -= 1
    #     self.quantityEntry.delete(0)
    #     self.quantityEntry.insert(0, self.q)


y_start -= 120
x_start += 330


recipe_frame = LabelFrame(root, text='Recipes',
                          padx=label_pad[0], pady=label_pad[1])
recipe_frame.place(x=x_start, y=y_start)

r = ric.Recipes(hotelconn)

i = 0
recipeAllList = []
for recipe in r.getRecipes():

    id, name, type, rh, mk, tp = recipe

    re1 = RecipeItem(id, name, i)
    recipeAllList.append(re1)
    i += 1


def generateRecipeOrder(orderRecipeList):

    inventory = rc.displayInventory()

    s = True
    total_cost = 0
    for id, q in orderRecipeList:
        q = int(q)
        print(f'{id} - {q}')
        r1 = ic.Recipe(hotelconn)
        r1.getDetails(id)
        total_cost += r1.details['price']*q
        for n in range(1, q+1):
            if r1.checkRecipeIngredients():
                r1.order(id)
                print(f"ORDERED {n} time")
            else:
                messagebox.showerror('Error !', 'Not enough Ingredients !')

                s = False
                break

    if s == True:
        messagebox.showinfo('Bill', f'Order Total --> {total_cost}')
        inventory = rc.displayInventory()
        updateInventory(inventory)


def refreshList():
    recipeOrderList = []
    updateInventory(rc.displayInventory())
    for re in recipeAllList:
        re.refresh_recipe()


orderRecipe = Button(recipe_frame, text='ORDER RECIPES',
                     command=lambda: generateRecipeOrder(recipeOrderList), width=45)
orderRecipe.grid(row=i, column=0, columnspan=3,
                 padx=stock_unit_pad[0], pady=stock_unit_pad[1])
i += 1
refreshButton = Button(recipe_frame, text='REFRESH',
                       command=refreshList, width=45)
refreshButton.grid(row=i, column=0, columnspan=3,
                   padx=stock_unit_pad[0], pady=stock_unit_pad[1])


root.mainloop()
