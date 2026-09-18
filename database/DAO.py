
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
               q1.quantita AS quantita1,
               q2.quantita AS quantita2,
               DATEDIFF(o2.order_date, o1.order_date) AS giorni_tra_ordini

        FROM orders o1, orders o2, stores s,

             -- CALCOLO PRIMA IL TOTALE DEGLI ARTICOLI DEL PRIMO ORDINE
             (SELECT order_id, SUM(quantity) AS quantita
              FROM order_items
              GROUP BY order_id) q1,

             -- CALCOLO PRIMA IL TOTALE DEGLI ARTICOLI DEL SECONDO ORDINE
             (SELECT order_id, SUM(quantity) AS quantita
              FROM order_items
              GROUP BY order_id) q2

        -- I DUE ORDINI DEVONO APPARTENERE ALLO STESSO STORE
        WHERE o1.store_id = o2.store_id

        -- COLLEGO IL TOTALE DEGLI ARTICOLI DEL PRIMO ORDINE AL PRIMO ORDINE
        AND q1.order_id = o1.order_id

        -- COLLEGO IL TOTALE DEGLI ARTICOLI DEL SECONDO ORDINE AL SECONDO ORDINE
        AND q2.order_id = o2.order_id

        -- COLLEGO GLI ORDINI ALLO STORE
        AND s.store_id = o1.store_id

        -- o1 DEVE AVERE LA DATA PIÙ PICCOLA E QUINDI ESSERE L'ORDINE PRECEDENTE
        -- o2 DEVE AVERE LA DATA PIÙ GRANDE E QUINDI ESSERE L'ORDINE SUCCESSIVO
        AND o1.order_date < o2.order_date

        -- CONSIDERO SOLO LO STORE SELEZIONATO DALL'UTENTE
        AND s.store_name = %s

        -- CALCOLO LA DIFFERENZA TRA DATA PIÙ GRANDE E DATA PIÙ PICCOLA (in giorni)
        -- LA DISTANZA TRA I DUE ORDINI DEVE ESSERE AL MASSIMO K GIORNI
        AND DATEDIFF(o2.order_date, o1.order_date) <= %s
        """
        cursor.close()
        conn.close()
        return results



