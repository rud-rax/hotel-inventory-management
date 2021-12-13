
# import xlrd
import pandas as pd
import mysql.connector as myc

path = f"data/databaseValues.xlsx"

# wb = xlrd.open_workbook(path)
# sheet = wb.sheet_by_index(1)

# print(sheet.row_values(3))

data1 = pd.read_excel(path, sheet_name='Sheet2')

# print(df.head())

# for id in data:
#     print(id)


lhost = "localhost"
luser = "root"
lpasswd = "rudu101519"
database_name = "hotel_database"

hotelconn = myc.connect(
    host=lhost, user=luser, passwd=lpasswd, database=database_name
)

cursor = hotelconn.cursor()

table = 'inventory'


def generateInventoryInsertQuery(data):

    ids = data['Unnamed: 0'][2:]
    names = data['Unnamed: 1'][2:]
    quantities = data['Unnamed: 2'][2:]
    ppqs = data['Unnamed: 3'][2:]

    print('PARSING DATA')
    data = []
    for id, name, q, ppq in zip(ids, names, quantities, ppqs):
        # print(f"ID {id} NAME {name} QUANTITY {q} PPQ {ppq}")
        tempstr = f"('{id}','{name}',{q},{ppq})"
        # print(tempstr)
        data.append(tempstr)

    print(data)
    print('GENERATING QUERY .. ')

    query = f'insert into {table} values ' + ','.join(data)

    return query + ";"


data2 = pd.read_excel(path, sheet_name='Sheet3')
print(data2)

recipe_table = "recipe"


def generateRecipeInsertQuery(data):

    ids = data['ID']
    names = data['Name']
    types = data['Type']
    recipes = data['Recipe_hash']
    prices = data['Price']
    tps = data['Total Price']

    # print(recipes)
    data = []

    for id, name, type, recipe_hash, p, tp in zip(ids, names, types, recipes, prices, tps):
        tempstr = f"({id},'{name}','{type}','{recipe_hash}',{p},{round(tp)})"
        data.append(tempstr)

    query = f'insert into {recipe_table} values ' + ','.join(data)
    return query


def runQuery(query):

    cursor.execute(query)
    hotelconn.commit()


print(query := generateInventoryInsertQuery(data1))

runQuery(query)


# # print(generateRecipeInsertQuery(data2))
# runQuery(generateRecipeInsertQuery(data2))
# print('SUCCESS !')
