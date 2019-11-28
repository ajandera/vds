import mysql.connector
from GPSPhoto import gpsphoto


def insertVariablesIntoTable(cesta, latitude, longitude):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='ibm',
                                             user='root',
                                             password='paz1c')
        cursor = connection.cursor()
        mysql_insert_query = """INSERT INTO photos (Path, Latitude, Longitude) 
                                VALUES (%s, %s, %s) """

        recordTuple = (cesta, latitude, longitude)
        cursor.execute(mysql_insert_query, recordTuple)
        connection.commit()
        print("Record inserted successfully into photos table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


path = input()
data = gpsphoto.getGPSData(path)
insertVariablesIntoTable(path, data['Latitude'], data['Longitude'])
