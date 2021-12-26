import mysql.connector as myc


class HDBConn:

    inventory_table = "inventory"
    recipe_table = "recipe"

    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()

    def displayInventory(self):

        query = f"select * from {HDBConn.inventory_table} ; "
        self.cursor.execute(query)
        inventory = self.cursor.fetchall()
        # for item in inventory:
        #     print(item)

        return inventory

    def orderItems(self, orderList):

        orderCost = 0
        for id, q, ppq in orderList:
            query = f"update {HDBConn.inventory_table} set quantity = quantity + {int(q)} where id = '{id}'"
            self.cursor.execute(query)
            orderCost += ppq * int(q)

        self.conn.commit()

        return orderCost

    def calculateOrderCost(self, orderList):
        orderCost = 0
        for id, q, ppq in orderList:
            query = f'select ppq from {HDBConn.inventory_table} where id = "{id}"'
            self.cursor.execute(query)
            ppq = self.cursor.fetchall()[0][0]
            orderCost += ppq*q

        print(orderCost)
        return orderCost

    def discardItems(self, discardList):

        # discardCost = 0
        print('discard list --> ', discardList)
        for id, q in discardList:
            query = f"update {HDBConn.inventory_table} set quantity = quantity - {int(q)} where id = '{id}'"
            self.cursor.execute(query)
            # discardCost += ppq * q

        self.conn.commit()
        # return discardCost

    def changeItemPPQ(self, id, ppq):

        query = f"update {HDBConn.inventory_table} set ppq = {ppq} where id = '{id}'"
        self.cursor.execute(query)

        self.conn.commit()
        return True

    def changeItemName(self, changeList):

        for id, name, q, ppq in changeList:
            query = f"update {HDBConn.inventory_table} set name = '{name}' where id = '{id}'"
            self.cursor.execute(query)

        self.conn.commit()
        return True

    def checkLowItems(self, margin_quantity=100):
        lowItems = []
        inventory = self.displayInventory()

        for id, name, quantity, _ in inventory:

            if quantity < margin_quantity:
                lowItems.append((id, name))

        return lowItems


class Recipe(HDBConn):

    recipe_table = 'recipe'
    inventory_table = 'inventory'

    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()

        self.details = {
            'id': 0,
            'name': '',
            'type': '',
            'recipe_hash': '',
            'price': 0
        }
        self.ingredients = []

    def getRecipe2Hash(self):
        hash = ""
        indList = []
        for id, q in self.ingredients:
            ind = id+"*"+str(q)
            indList.append(ind)

        hash = '+'.join(indList)
        return hash

    def getHash2Recipe(self):
        # print('recipe hash --. ', self.details['recipe_hash'])
        recipe_ingredients = self.details['recipe_hash'].split('+')
        for ind in recipe_ingredients:
            id, q = ind.split('*')
            self.ingredients.append((id, int(q)))
            #recipeList.append((id, int(q)))
        # return recipeList
        # print('Self ingredients --> ', self.ingredients)
        return self.ingredients

    def getDetails(self, id):
        query = f'select * from {Recipe.recipe_table} where id = {id}; '
        self.cursor.execute(query)
        recipe = self.cursor.fetchall()[0]

        self.parseDetails(recipe)
        # print(recipes)
        return recipe

    def parseDetails(self, details):
        self.details['id'] = details[0]
        self.details['name'] = details[1]
        self.details['type'] = details[2]
        self.details['recipe_hash'] = details[3]
        self.details['price'] = details[5]

        self.getHash2Recipe()

    def order(self, id):

        # self.getDetails(id)
        if self.checkRecipeIngredients():
            self.discardItems(self.ingredients)

            print(
                f'ORDER PLACED : {self.details["name"]} - {self.details["price"]}')

            return True

        else:
            return False

    def checkRecipeIngredients(self):

        for id, quantity in self.ingredients:

            query = f'select name,quantity from {Recipe.inventory_table} where id = "{id}" ;'
            self.cursor.execute(query)
            output = self.cursor.fetchall()[0]
            name, available_quantity = output[0], output[1]
            # print('AVAILABLE -- ', available_quantity)
            # print('NEEDED -- ', quantity)

            if available_quantity < quantity:
                print(
                    f'CANNOT PREPARE THE RECIPE ! ITEM {name} IS LOW IN QUANTITY ')
                print(
                    f'NEED MORE {quantity - available_quantity} TO PREPARE THE DISH !')
                return False

        return True

    def addRecipe(self, values):

        id = self.getNewRecipeId()

        # id ,name , type ,rc , mk , tp
        valstr = f"({id} ,'{values[0]}','{values[1]}','{values[2]}',{values[3]},{values[4]}) ;"
        query = f'insert into {Recipe.recipe_table} values {valstr}'
        # print(query)
        self.cursor.execute(query)
        self.conn.commit()

    def getNewRecipeId(self):

        query = f'select id from {Recipe.recipe_table} order by id desc limit 1'
        self.cursor.execute(query)
        lastid = self.cursor.fetchall()[0][0]
        # print(lastid)

        return lastid + 1


if __name__ == "__main__":

    lhost = "localhost"
    luser = "root"
    lpasswd = "rudu101519"
    database_name = "hotel_database"

    hotelconn = myc.connect(
        host=lhost, user=luser, passwd=lpasswd, database=database_name
    )

    # hc1 = HDBConn(connection=hotelconn)
    # hc1.displayInventory()

    # ORDER ITEMS TESTING CODE
    # ol = [
    #     ("ML1", "Cheese", 1, 20),
    #     ("ML2", "Paneer", 1, 25),
    #     ("VG1", "Potato", 3, 10),
    #     ("VG2", "Cucumber", 2, 15),
    #     ("VG3", "Tomato", 2, 10),
    #     ("VG4", "Onion", 1, 20),
    #     ("VG5", "Capsicum", 2, 15),
    # ]

    # sum = hc1.orderItems(ol)
    # print("TOTAL --> ", sum)
    # hc1.displayInventory()

    # DISCARD ITEMS TESTING CODE
    # ol = [
    #     ("ML1", "Cheese", 1, 20),
    #     ("ML2", "Paneer", 1, 25),
    #     ("VG1", "Potato", 3, 10),
    #     ("VG2", "Cucumber", 2, 15),
    #     ("VG3", "Tomato", 2, 10),
    #     ("VG4", "Onion", 1, 20),
    #     ("VG5", "Capsicum", 2, 15),
    # ]

    # sum = hc1.discardItems(ol)
    # print("TOTAL --> ", sum)
    # hc1.displayInventory()

    # CHANGING ITEMS TESTING CODE
    # ol = [
    #     ("ML1", "Cheeeese", 1, 20),
    #     ("ML2", "Paneeeer", 1, 25),
    #     ("VG1", "Potatoooo", 3, 10),
    #     ("VG2", "Cucumber", 2, 15),
    #     ("VG3", "Tomatoooo", 2, 10),
    #     ("VG4", "Oniiion", 1, 20),
    #     ("VG5", "Capsiiicum", 2, 15),
    # ]

    # sum = hc1.changeItemName(ol)

    # hc1.displayInventory()

    # ol = [
    #     ("ML1", "Cheese", 1, 30),
    #     ("ML2", "Paneer", 1, 15),
    #     ("VG1", "Potato", 3, 10),
    #     ("VG2", "Cucumber", 2, 25),
    #     ("VG3", "Tomato", 2, 20),
    #     ("VG4", "Onion", 1, 30),
    #     ("VG5", "Capsicum", 2, 15),
    # ]

    # hc1.changeItemPPQ(ol)
    # hc1.displayInventory()

    rc1 = Recipe(hotelconn)

    rc1.getDetails(1)
    rc1.order()

    # print(rc1.displayInventory())
    # print(rc1.details)
    # print(rc1.getHash2Recipe())
    # print(rc1.getRecipe2Hash())
    # h1 = 'BD1*2+ML1*1+ML2*1+TP1*1+TP2*1+VG4*1+VG3*1'
    # print(rl1 := rc1.getHash2Recipe(h1))

    # rl1 = [('BD1', 2), ('ML1', 1), ('ML2', 1), ('TP1', 1),
    #        ('TP2', 1), ('VG4', 1), ('VG3', 1)]
    # print(rc1.getRecipe2Hash(rl1))

    hotelconn.close()
