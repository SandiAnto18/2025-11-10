
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
    def getOrder1Order2(store_name,k):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
SELECT o1.order_id as order1, o2.order_id as order2

FROM orders o1, orders o2, stores s

-- I DUE ORDINI DEVONO APPARTENERE ALLO STESSO STORE
WHERE o1.store_id = o2.store_id

-- COLLEGO GLI ORDINI ALLO STORE
AND s.store_id = o1.store_id

-- o1 DEVE AVERE LA DATA PIÙ PICCOLA E QUINDI ESSERE L'ORDINE PRECEDENTE
-- o2 DEVE AVERE LA DATA PIÙ GRANDE E QUINDI ESSERE L'ORDINE SUCCESSIVO
AND o1.order_date < o2.order_date
and s.store_name=%s

-- CALCOLO LA DIFFERENZA TRA DATA PIÙ GRANDE E DATA PIÙ PICCOLA (in giorni)
-- LA DISTANZA TRA I DUE ORDINI DEVE ESSERE AL MASSIMO 5 GIORNI
AND DATEDIFF(o2.order_date, o1.order_date) <= %s
"""
        cursor.execute(query, (store_name,k))

        for row in cursor:
            #results.append(row["o1.order_id"], row["o2.order_id"]) #cosi non va bene

            # AGGIUNGO UNA COPPIA DI ORDINI COME UN SOLO ELEMENTO
            results.append((row["order1"], row["order2"],row["quantita1"],row["quantita2"]))
           #ogni tupla rapprensenta un arco, esempio: (10,15) = (10->15)

        cursor.close()
        conn.close()
        return results



