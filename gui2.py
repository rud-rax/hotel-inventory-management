from os import name
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import manageLogs as mL
import mysql.connector as myc
import inventoryConnect as ic
import recipeConnect as ric

# DATABASE VARIABLES
lhost = "localhost"
luser = "root"
lpasswd = ''
database_name = "hotel_database"

# DATABASE CONNECTION
hotelconn = myc.connect(
    host=lhost, user=luser, passwd=lpasswd, database=database_name
)

# BACKEND CODE
rc = ic.Recipe(hotelconn)

# COLORS AND FONTS
# colorPalette2 = ['4F091D', 'DD4A48', 'F5EEDC']
# colorPalette1 = ['FF5C58', 'FE8F8F', '2D2424']
colorPalette3 = ['191919', '31112C', 'F2FFE9']
# colorPalette4 = ['31112C', '065C6F', 'FAF3DD']
# colorPalette5 = ['CEE5D0', 'F3F0D7', '5E454B']

colorPalette = colorPalette3
colorPalette = ['#'+col for col in colorPalette]
Ifont = 'Helvetica'
# bg=colorPalette[1], fg=colorPalette[2], font=Ifont

root = Tk()
root.geometry('1600x900+10+10')
root.title('HOTEL INVENTORY')
root.configure(bg=colorPalette[0])
root.iconbitmap(r"images/hotel4.ico")


lg = mL.HotelLog()

x_start = 20
y_start = 10

# STOCK FRAME STARTS -- >
stock_frame = LabelFrame(
    root, text='Stock', padx=10, pady=8)
stock_frame.configure(bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
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
    # print(orderlist)

    totalCost = rc.orderItems(orderlist)
    inventory = rc.displayInventory()
    updateInventory(inventory)

    ans = messagebox.askyesno(
        'TOTAL EXPENSE', f"The total order cost is {totalCost} \n Are you sure you want to place the order ?")

    if not ans:
        rc.discardItems(orderlist)
        inventory = rc.displayInventory()
        updateInventory(inventory)

    else:

        neworderList = [[id, int(q), float(ppq)]
                        for id, q, ppq in orderlist if int(q) > 0]
        print(neworderList)
        lg.addOrderLog(neworderList)

        # ADD REPORT CODE HERE
        pass


def changePPQ():

    new_ppq = ppq_entry.get()
    id = item_dict[clicked1.get()][0]

    rc.changeItemPPQ(id, new_ppq)

    inventory = rc.displayInventory()
    updateInventory(inventory)


def changeName(): pass


# GET VALUES FROM DATABASE
inventory = rc.displayInventory()

NAME_label = Label(stock_frame, text='NAME', bg=colorPalette[0], fg=colorPalette[2], font=Ifont).grid(
    row=0, column=0, padx=label_pad[0], pady=label_pad[1])
QUANTITY_label = Label(stock_frame, text='QUANTITY', bg=colorPalette[0], fg=colorPalette[2], font=Ifont).grid(
    row=0, column=1, padx=label_pad[0], pady=label_pad[1])
PPQ_label = Label(stock_frame, text='PRICE PER QUANTITY', bg=colorPalette[0], fg=colorPalette[2], font=Ifont).grid(
    row=0, column=2, padx=label_pad[0], pady=label_pad[1])


def updateInventory(inventory):

    i = 1
    for id, name, quantity, ppq in inventory:

        stock_namelabels.append(Label(stock_frame, text=name, bg=colorPalette[0], fg=colorPalette[2], font=Ifont).grid(
            row=i, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1], sticky=W))

        stock_quantityboxes.append(
            Label(stock_frame, text=quantity, bg=colorPalette[0], fg=colorPalette[2], font=Ifont).grid(row=i, column=1, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

        stock_ppqs.append(Label(stock_frame, text=ppq, bg=colorPalette[0], fg=colorPalette[2], font=Ifont).grid(
            row=i, column=2, padx=stock_unit_pad[0], pady=stock_unit_pad[1]))

        item_dict[name] = [id, 0, ppq]

        i += 1


updateInventory(inventory)


x_start += 520

order_unitpad = (14, 2)

order_frame = LabelFrame(
    root, text='Order', padx=10, pady=8)
order_frame.configure(bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
order_frame.place(x=x_start, y=y_start)

iv = list(item_dict.keys())

clicked = StringVar()
clicked.set(iv[0])

orderSelect = OptionMenu(order_frame, clicked, *iv)
orderSelect['menu'].config(
    bg=colorPalette[1], fg=colorPalette[2], font='Helvetica')
orderSelect.configure(bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
orderSelect.grid(row=0, column=0, padx=order_unitpad[0], pady=order_unitpad[1])

quantity_entry = Entry(order_frame, width=13,
                       bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
quantity_entry.grid(
    row=0, column=1, padx=order_unitpad[0], pady=order_unitpad[1])

quantity_entry.insert(0, item_dict[clicked.get()][1])

getq_button = Button(order_frame, text="GET",
                     width=5, command=getItems, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
getq_button.grid(row=0, column=2, padx=order_unitpad[0], pady=order_unitpad[1])


orderButton = Button(order_frame, text="ORDER ITEMS",
                     width=35, command=orderItems, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
orderButton.grid(row=1, column=0, columnspan=3,
                 padx=order_unitpad[0], pady=order_unitpad[1])


# MANAGE PPQ FRAME

y_start += 120
manage_frame = LabelFrame(
    root, text='Manage Price Per Quantity', padx=10, pady=8)
manage_frame.configure(bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
manage_frame.place(x=x_start, y=y_start)

clicked1 = StringVar()
clicked1.set(iv[0])


ppqSelect = OptionMenu(manage_frame, clicked1, *iv)
ppqSelect['menu'].config(
    bg=colorPalette[1], fg=colorPalette[2], font='Helvetica')
ppqSelect.configure(bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
ppqSelect.grid(row=0, column=0, padx=order_unitpad[0], pady=order_unitpad[1])

ppq_entry = Entry(manage_frame, width=24,
                  bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
ppq_entry.grid(
    row=0, column=1, padx=order_unitpad[0], pady=order_unitpad[1])

ppq_entry.insert(0, item_dict[clicked.get()][1])

ppq_button = Button(manage_frame, text="CHANGE",
                    width=35, command=changePPQ, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
ppq_button.grid(row=1, column=0, columnspan=2,
                padx=order_unitpad[0], pady=order_unitpad[1])


y_start += 120
# x_start += 330


# NEW WINDOW FOR RECIPE


class Ingredient():
    def __init__(self, frame, row, column, id, name, ppq):
        self.id = id
        self.name = name
        self.ppq = ppq

        self.q = 0

        self.row = row
        self.column = column

        self.label = Label(frame, text=self.name,
                           bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
        self.label.grid(row=self.row, column=self.column,
                        padx=order_unitpad[0], pady=order_unitpad[1], sticky=W)

        self.qEntry = Entry(
            frame, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
        self.qEntry.grid(row=self.row, column=self.column + 1,
                         padx=order_unitpad[0], pady=order_unitpad[1])
        self.qEntry.insert(0, self.q)


class NewRecipe():

    def __init__(self):
        self.name = ''
        self.type = ''
        self.recipe_hash = ''
        self.mk = 0
        self.tp = 0


def openRecipeWindow():

    recipeWindow = Toplevel(bg=colorPalette[0])
    recipeWindow.title('RECIPE WINDOW')
    recipeWindow.geometry('900x400+450+350')

    # RECIPE FRAME

    recipeOrderList = []

    recipe_frame = LabelFrame(recipeWindow, text='Recipes', bg=colorPalette[0], fg=colorPalette[2], font=Ifont,
                              padx=label_pad[0], pady=label_pad[1])
    recipe_frame.place(x=10, y=10)
    # recipe_frame.place(x=x_start, y=y_start)

    x_start = 10
    y_start = 10

    r = ric.Recipes(hotelconn)

    i = 0
    recipeAllList = []

    recipeDDM = StringVar()

    options = []
    recipe_dict = {}
    for recipe in r.getRecipes():

        id, name, type, rh, mk, tp = recipe
        recipe_dict[name] = id
        options.append(name)
        # re1 = RecipeItem(id, name, i)
        # recipeAllList.append(re1)
        i += 1

    def addToOrder():
        name = recipeDDM.get()

        id = recipe_dict[name]
        q = orderQuantityEntry.get()
        try:
            recipeOrderList.append((id, int(q)))

        except ValueError:
            messagebox.showerror('Error', 'Invalid Quantity Entered !')

        print(recipeOrderList)

    recipeDDM.set(options[0])
    recipeDrop = OptionMenu(recipe_frame, recipeDDM, *options)
    recipeDrop['menu'].config(
        bg=colorPalette[1], fg=colorPalette[2], font='Helvetica')
    recipeDrop.configure(bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
    recipeDrop.grid(row=0, column=0,
                    padx=stock_unit_pad[0], pady=stock_unit_pad[1])

    orderQuantityEntry = Entry(
        recipe_frame, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
    orderQuantityEntry.grid(
        row=0, column=1, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

    availableRecipeLabel = Label(
        recipe_frame, text="-", bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
    availableRecipeLabel.grid(
        row=0, column=2, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

    getRecipeButton = Button(recipe_frame, text='GET', command=addToOrder,
                             bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
    getRecipeButton.grid(
        row=0, column=3, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

    def generateRecipeOrder(orderRecipeList):

        inventory = rc.displayInventory()

        s = True
        total_cost = 0
        for id, q in orderRecipeList:
            q = int(q)
            print(f'{id} - {q}')
            for n in range(1, q+1):

                r1 = ic.Recipe(hotelconn)
                r1.getDetails(id)
                total_cost += r1.details['price']

                if r1.checkRecipeIngredients():
                    r1.order(id)
                    print(f"ORDERED {n} time")
                else:
                    messagebox.showerror('Error !', 'Not enough Ingredients !')

                    s = False
                    break

        if s == True:
            messagebox.showinfo('Bill', f'Order Total --> {total_cost}')
            print(orderRecipeList)

            lg.addRecipeLog(orderRecipeList)
            # ADD REPORT CODE HERE

        inventory = rc.displayInventory()
        updateInventory(inventory)

    def refreshList():
        global recipeOrderList
        recipeOrderList = []
        updateInventory(rc.displayInventory())

        recipe_name = recipeDDM.get()
        recipe_id = recipe_dict[recipe_name]

        rc1 = ic.Recipe(hotelconn)
        rc1.getDetails(recipe_id)
        recipeNeedQuantity = rc1.ingredients

        availableQuantity = rc.displayInventory()

        maxRecipeLimit = 99999999

        breakflag = False
        for id, q in recipeNeedQuantity:
            for aid, _1, aq, _2 in availableQuantity:
                if aid == id:
                    if aq > q:

                        # print('id - ', id)
                        # print('aq =', aq)
                        # print('q = ', q)
                        ning = aq // q
                        # print('max ing - ', ning)
                        if ning < maxRecipeLimit:
                            maxRecipeLimit = ning

                        # print(maxRecipeLimit)
                    else:
                        maxRecipeLimit = 0
                        breakflag = True
                        break

            if breakflag:
                break

        availableRecipeLabel = Label(
            recipe_frame, text=maxRecipeLimit, bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
        availableRecipeLabel.grid(
            row=0, column=2, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

        # print('---- recipe need')
        # print(recipeNeedQuantity)
        # print(' ---- available')
        # print(availableQuantity)

        recipeNeedQuantity = []
        availableQuantity = []

        for re in recipeAllList:
            re.refresh_recipe()

    orderRecipe = Button(recipe_frame, text='ORDER RECIPES',
                         command=lambda: generateRecipeOrder(recipeOrderList), width=56, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
    orderRecipe.grid(row=i, column=0, columnspan=4,
                     padx=stock_unit_pad[0], pady=stock_unit_pad[1])
    i += 1
    refreshButton = Button(recipe_frame, text='REFRESH',
                           command=refreshList, width=56, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
    refreshButton.grid(row=i, column=0, columnspan=4,
                       padx=stock_unit_pad[0], pady=stock_unit_pad[1])

    y_start += 160

    backToInventoryButton = Button(
        recipeWindow, text='BACK', command=recipeWindow.destroy, height=4, width=62, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
    backToInventoryButton.place(x=x_start, y=y_start)

    y_start -= 135
    y_start += stock_unit_pad[1]
    x_start += 470

    # ADD RECIPE WINDOW
    recipe_hash = ''
    recipe_make_price = 0

    # return hash

    def openAddRecipeWindow():

        nre = NewRecipe()

        recipe_hash = ''

        addrecipeWindow = Toplevel(
            bg=colorPalette[0])
        addrecipeWindow.title('ADD RECIPE')

        addrecipeWindow.geometry('900x900+750+10')

        newRecipeDetails = LabelFrame(addrecipeWindow, text='Details')
        newRecipeDetails.configure(
            bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
        newRecipeDetails.place(x=10, y=10)

        newRecipeIngredients = LabelFrame(addrecipeWindow, text='Ingredients')
        newRecipeIngredients.configure(
            bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
        newRecipeIngredients.place(x=380, y=10)

        def destoryaddRecipeWindow():

            nre.recipe_hash = ''
            nre.mk = 0

            addrecipeWindow.destroy()

        def createRecipe():

            try:
                nre.name = str(newRecipeNameEntry.get())
                nre.tp = int(tpEntry.get())
                nre.type = str(recipeType.get())
                nre.mk = int(nre.mk)

                newRecipeDetails = [nre.name, nre.type,
                                    nre.recipe_hash, nre.mk, nre.tp]
                print(f'{nre.name} {nre.type} {nre.recipe_hash} {nre.mk} {nre.tp}')

                rc.addRecipe(newRecipeDetails)

            except ValueError:
                messagebox.showerror('ERROR', 'Invalid Values ! Try Again.')
                destoryaddRecipeWindow()

        backToRecipeButton = Button(
            addrecipeWindow, text='BACK', command=destoryaddRecipeWindow, width=38, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
        backToRecipeButton.place(x=10, y=180)

        createRecipeButton = Button(
            addrecipeWindow, text='ADD TO MENU', width=38, command=createRecipe, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)  # add command
        createRecipeButton.place(x=10, y=140)

        allIngredients = []

        row = 0
        column = 0

        tempInventory = rc.displayInventory()
        for idI, nameI, _, ppqI in tempInventory:
            new_ing = Ingredient(newRecipeIngredients, row,
                                 column, idI, nameI, ppqI)
            allIngredients.append(new_ing)

            row += 1

        def confirmIngredients(allIngredients):

            # global recipe_hash
            # recipe_make_price = 0
            ingList = []

            for ing in allIngredients:
                id = ing.id
                q = int(ing.qEntry.get())
                ppq = float(ing.ppq)
                if q:
                    nre.mk += (float(ppq)*q)
                    ingList.append(id+"*"+str(q))

            nre.recipe_hash = '+'.join(ingList)
            print(nre.recipe_hash)

            mkLabel = Label(newRecipeDetails, text=nre.mk,
                            bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
            mkLabel.grid(row=2, column=2,
                         padx=stock_unit_pad[0], pady=stock_unit_pad[1])

            # messagebox.showinfo(
            #     'Make Price', f'Total Make Price = {recipe_make_price}')

        recipeConfirmButton = Button(
            newRecipeIngredients, text='CONFIRM', width=37, command=lambda: confirmIngredients(allIngredients), bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
        recipeConfirmButton.grid(
            row=row, column=0, columnspan=2, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

        # DETAILS FRAME

        newRecipeNameLabel = Label(
            newRecipeDetails, text='Name : ', bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
        newRecipeNameLabel.grid(
            row=0, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1], sticky=W)

        i = 0
        recipeType = StringVar()

        for option in ['Veg', 'Non-veg']:
            newRecipeType = Radiobutton(
                newRecipeDetails, text=option, variable=recipeType, value=option, bg=colorPalette[0], fg=colorPalette[2], font=Ifont, selectcolor=colorPalette[0])
            newRecipeType.grid(
                row=1, column=i, padx=stock_unit_pad[0], pady=stock_unit_pad[1], sticky=W)
            i += 1

        newRecipeNameEntry = Entry(
            newRecipeDetails, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
        newRecipeNameEntry.grid(
            row=0, column=1, padx=stock_unit_pad[0], pady=stock_unit_pad[1])

        totalPriceLabel = Label(newRecipeDetails, text='Total Price : ',
                                bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
        totalPriceLabel.grid(
            row=2, column=0, padx=stock_unit_pad[0], pady=stock_unit_pad[1], sticky=W)
        tpEntry = Entry(newRecipeDetails,
                        bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
        tpEntry.grid(row=2, column=1,
                     padx=stock_unit_pad[0], pady=stock_unit_pad[1])

        mkLabel = Label(newRecipeDetails, text='-',
                        bg=colorPalette[0], fg=colorPalette[2], font=Ifont)
        mkLabel.grid(row=2, column=2,
                     padx=stock_unit_pad[0], pady=stock_unit_pad[1])

    newRecipeButton = Button(
        recipeWindow, text='ADD RECIPE', height=7, width=12, command=openAddRecipeWindow, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
    newRecipeButton.place(x=x_start + 130, y=y_start - 24)


y_start += 10
recipeWindowButton = Button(root, text='OPEN MENU',
                            command=openRecipeWindow, width=41, height=4, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
recipeWindowButton.place(x=x_start, y=y_start)


def generateRep():
    moneySpent, moneyEarned = lg.generateReport()

    profit = moneyEarned + moneySpent

    messagebox.showinfo(
        "TODAY'S REPORT", f'Money Spent = {abs(moneySpent)} \nMoneyEarned = {moneyEarned} \nProfit = {profit}')


y_start += 100
generateReportButton = Button(
    root, text='GENERATE REPORT', width=41, height=4, command=generateRep, bg=colorPalette[1], fg=colorPalette[2], font=Ifont)
generateReportButton.place(x=x_start, y=y_start)

root.mainloop()
