
import mysql.connector as myc


class Recipes:

    table = 'recipe'

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def getRecipes(self):

        query = f'select * from {Recipes.table} ;'
        self.cursor.execute(query)
        recipes = self.cursor.fetchall()

        return recipes


if __name__ == "__main__":

    lhost = "localhost"
    luser = "root"
    lpasswd = ""
    database_name = "hotel_database"

    hotelconn = myc.connect(
        host=lhost, user=luser, passwd=lpasswd, database=database_name
    )

    r = Recipes(hotelconn)

    for recipe in r.getRecipes():
        print(recipe)
