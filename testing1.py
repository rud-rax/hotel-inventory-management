
import mysql.connector as myc
import inventoryConnect as ic


lhost = "localhost"
luser = "root"
lpasswd = "rudu101519"
database_name = "hotel_database"

hotelconn = myc.connect(
    host=lhost, user=luser, passwd=lpasswd, database=database_name
)


rc1 = ic.Recipe(hotelconn)

# rc1 = HDBConn(connection=hotelconn)
# rc1.displayInventory()


def testOrderItems():
    # ORDER ITEMS TESTING CODE
    ol = [
        ("ML1", "Cheese", 1, 20),
        ("ML2", "Paneer", 1, 25),
        ("VG1", "Potato", 3, 10),
        ("VG2", "Cucumber", 2, 15),
        ("VG3", "Tomato", 2, 10),
        ("VG4", "Onion", 1, 20),
        ("VG5", "Capsicum", 2, 15),
    ]

    sum = rc1.orderItems(ol)
    print("TOTAL --> ", sum)
    rc1.displayInventory()


def testDiscardItems():
    # DISCARD ITEMS TESTING CODE
    ol = [
        ("ML1", "Cheese", 1, 20),
        ("ML2", "Paneer", 1, 25),
        ("VG1", "Potato", 3, 10),
        ("VG2", "Cucumber", 2, 15),
        ("VG3", "Tomato", 2, 10),
        ("VG4", "Onion", 1, 20),
        ("VG5", "Capsicum", 2, 15),
    ]

    sum = rc1.discardItems(ol)
    print("TOTAL --> ", sum)
    rc1.displayInventory()


def testChangeItemNames():
    # CHANGING ITEMS TESTING CODE
    ol = [
        ("ML1", "Cheeeese", 1, 20),
        ("ML2", "Paneeeer", 1, 25),
        ("VG1", "Potatoooo", 3, 10),
        ("VG2", "Cucumber", 2, 15),
        ("VG3", "Tomatoooo", 2, 10),
        ("VG4", "Oniiion", 1, 20),
        ("VG5", "Capsiiicum", 2, 15),
    ]

    sum = rc1.changeItemName(ol)


def testDisplayInventory():
    rc1.displayInventory()

    ol = [
        ("ML1", "Cheese", 1, 30),
        ("ML2", "Paneer", 1, 15),
        ("VG1", "Potato", 3, 10),
        ("VG2", "Cucumber", 2, 25),
        ("VG3", "Tomato", 2, 20),
        ("VG4", "Onion", 1, 30),
        ("VG5", "Capsicum", 2, 15),
    ]

    rc1.changeItemPPQ(ol)
    rc1.displayInventory()


def testRecipe2Hash():
    print(rc1.displayInventory())
    print(rc1.details)
    print(rc1.getHash2Recipe())
    print(rc1.getRecipe2Hash())
    h1 = 'BD1*2+ML1*1+ML2*1+TP1*1+TP2*1+VG4*1+VG3*1'
    print(rl1 := rc1.getHash2Recipe(h1))

    rl1 = [('BD1', 2), ('ML1', 1), ('ML2', 1), ('TP1', 1),
           ('TP2', 1), ('VG4', 1), ('VG3', 1)]
    print(rc1.getRecipe2Hash(rl1))


def orderRecipe(id=1):

    rc1.getDetails(1)
    rc1.order(1)
    # rc1.displayInventory()


def testLowItems():
    print(rc1.checkLowItems())


def testgetNewRecipeId():
    print(rc1.getNewRecipeId())

# orderRecipe(1)

# testLowItems()


testgetNewRecipeId()


hotelconn.close()
