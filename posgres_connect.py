import psycopg2




contentelementtypeproperty_columns = {}
contentelementtypeproperty_columns["id"] = 0
contentelementtypeproperty_columns["key"] = 4
contentelementtypeproperty_columns["name"] = 6
contentelementtypeproperty_columns["value"] = 7



def get_connection():

    try:
        connection = psycopg2.connect(user = "zoeevelyn",
                                      password = "penzin1enzin",
                                      host = "192.168.0.23",
                                      port = "5432",
                                      database = "ikoda01")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
        return connection

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

def close_connection(connection):

            if(connection):
                connection.close()
                print("PostgreSQL connection is closed")





