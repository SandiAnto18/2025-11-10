
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
    #AATENZIONE: (numero_TOTALE_oggetti_nei_due_ordini)
    # INTENDE quanti sono gli articoli(items) ordinati di un ordine,
    # quindi la quantità totale di articoli per coppia di ordini
    #K = NUMERO MAX DI GIORNI
    def getOrder1Order2(store_name,k):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT o1.order_id AS order1,
                   o2.order_id AS order2,

                   -- CALCOLO DIRETTAMENTE IL PESO DELL'ARCO
                   (SUM(oi.quantity) + SUM(oi2.quantity))
                   / DATEDIFF(o2.order_date, o1.order_date) AS weight

            FROM orders o1, orders o2, order_items oi, order_items oi2, stores s

            WHERE o1.store_id = o2.store_id

            -- COLLEGO GLI ARTICOLI AL PRIMO ORDINE
            AND oi.order_id = o1.order_id

            -- COLLEGO GLI ARTICOLI AL SECONDO ORDINE
            AND oi2.order_id = o2.order_id

            -- COLLEGO GLI ORDINI ALLO STORE
            AND s.store_id = o1.store_id

            -- o1 È L'ORDINE PRECEDENTE
            AND o1.order_date < o2.order_date

            -- CONSIDERO SOLO LO STORE SCELTO
            AND s.store_name = %s

            -- LA DISTANZA MASSIMA È K GIORNI
            AND DATEDIFF(o2.order_date, o1.order_date) <= %s

            GROUP BY o1.order_id, o2.order_id
            """

        cursor.execute(query, (store_name, k))

        for row in cursor:
            results.append((
                row["order1"],
                row["order2"],
                row["weight"]
            ))

        cursor.close()
        conn.close()

        return results


