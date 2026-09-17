
from database.DB_connect import DBConnect




class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query="""select s.store_name  
from stores s """
        cursor.execute(query)
        for row in cursor:
            results.append(row["store_name"])

        cursor.close()
        conn.close()
        return results
    @staticmethod
    def getAllOrders(store_name):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select   o.*
from orders o,stores s
where store_name = %s
and s.store_id =o.store_id """
        cursor.execute(query, (store_name,))

        for row in cursor:
            results.append(row["order_id"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getOrderByOrder(k):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """query = """
SELECT o1.order_date, o2.order_date

FROM orders o1, orders o2, stores s

-- I DUE ORDINI DEVONO APPARTENERE ALLO STESSO STORE
WHER