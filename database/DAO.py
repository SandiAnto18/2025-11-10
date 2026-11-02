from database.DB_connect import DBConnect
from model.order import Order


class DAO():

    @staticmethod
    def getStores():
        # RECUPERO TUTTI GLI ANNI DISPONIBILI
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
              select store_name
from stores s
            """

        cursor.execute(query)
        results = []

        for row in cursor:
            results.append(row["store_name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getOrders(store_name):
        # RECUPERO TUTTI GLI ANNI DISPONIBILI
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
                  select o.*
from stores s,orders o
where s.store_id =o.store_id 
and s.store_name = %s
                """

        cursor.execute(query, (store_name,))
        results = []

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(store_name,k):
        # RECUPERO TUTTI GLI ANNI DISPONIBILI
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
                   select distinct o.order_id as ord1, o2.order_id as ord2,
sum(oi.quantity + oi2.quantity)/DATEDIFF(o2.order_date,o.order_date) as peso
from stores s,orders o,orders o2, order_items oi , order_items oi2
where s.store_id =o.store_id 
and s.store_name = %s
and s.store_id =o2.store_id 
and oi.order_id =o.order_id 
and oi2.order_id =o2.order_id 
and o.order_date < o2.order_date 
and o.order_id < o2.order_id 
and DATEDIFF(o2.order_date,o.order_date)<= %s
group by o.order_id, o2.order_id

                    """

        cursor.execute(query, (store_name,k))
        results = []

        for row in cursor:
            results.append((row["ord1"], row["ord2"], row["peso"]))

        cursor.close()
        conn.close()
        return results