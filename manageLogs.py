from datetime import date
import logging
import mysql.connector as myc

# DATABASE VARIABLES
lhost = "localhost"
luser = "root"
lpasswd = ""
database_name = "hotel_database"


class HotelLog:

    report_file_path = 'reports/'
    report_file_name = 'REPORT_'

    inventoryTable = 'inventory'
    recipeTable = 'recipe'

    def __init__(self):

        self.reportFileName = HotelLog.report_file_path + \
            HotelLog.report_file_name+str(date.today())+'.log'

        # print(self.reportFileName)

        logging.basicConfig(
            filename=self.reportFileName, format='%(asctime)s %(message)s', filemode='a')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.conn = myc.connect(
            host=lhost, user=luser, passwd=lpasswd, database=database_name
        )

        self.cursor = self.conn.cursor()

        self.inventoryData = []
        self.recipeData = []

    def addOrderLog(self, orderList):
        idList = [row[0] for row in orderList]

        self.getInventoryData(idList)
        for id, q, ppq in orderList:
            for iid, iname in self.inventoryData:
                if iid == id:
                    message = f'ORDERED ITEM: {iname} QUANTITY: {q} COST: -{ppq*q}'

                    self.logger.info(message)

    def addRecipeLog(self, recipeList):

        self.getRecipeData(recipeList)

        for id, q in recipeList:
            for iid, name, ppq in self.recipeData:
                if iid == id:
                    message = f'RECIPE SOLD: {name} QUANTITY: {q} COST: +{ppq*q}'

                    self.logger.info(message)

    def getInventoryData(self, idList):

        idstr = '"'+('","'.join(idList))+'"'
        query = f'select id,name from {HotelLog.inventoryTable} where id in ({idstr});'
        print(query)
        self.cursor.execute(query)
        self.inventoryData = self.cursor.fetchall()

        print(self.inventoryData)

    def getRecipeData(self, recipeIDs):

        idstr = ','.join([str(row[0]) for row in recipeIDs])
        query = f'select id,name,total_price from {HotelLog.recipeTable} where id in ({idstr}) ;'
        self.cursor.execute(query)
        self.recipeData = self.cursor.fetchall()

        print(self.recipeData)

    def generateReport(self):
        with open(self.reportFileName) as reportFile:
            reportData = reportFile.readlines()

        moneySpent = 0
        profitEarned = 0
        print(reportData)

        for line in reportData:
            data = line.split()[-1]
            n = float(data)

            if n < 0:
                moneySpent += n

            else:
                profitEarned += n

        # print(f'PROFITS - {moneySpent}')
        # print(f'SPENT MONEY - {profitEarned}')

        # print(f'NET PROFIT - {profitEarned - moneySpent}')

        return moneySpent, profitEarned


if __name__ == '__main__':

    l = HotelLog()

    # idList = ['OT2', 'MP2', 'MP3', 'MP4', 'MP5', 'MP6', 'NV2']

    # l.getInventoryData(idList)
    l.generateReport()
