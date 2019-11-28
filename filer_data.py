import mysql.connector


def filerYear(year):
    year = (year,)

    connection = mysql.connector.connect(host='localhost',
                                         database='ibm',
                                         user='root',
                                         password='paz1c')

    cursor = connection.cursor()
    sql = "SELECT * FROM photos WHERE YEAR(Created) = %s;"
    cursor.execute(sql, year)
    result = cursor.fetchall()

    for x in result:
        print(x)


def filerYearIsFixed(year, fixed):
    data = (year, fixed,)

    connection = mysql.connector.connect(host='localhost',
                                         database='ibm',
                                         user='root',
                                         password='paz1c')

    cursor = connection.cursor()
    sql = "SELECT * FROM photos WHERE YEAR(Created) = %s AND Solve = %s;"
    cursor.execute(sql, data)
    result = cursor.fetchall()

    for x in result:
        print(x)


def filerYearMonth(year, month):
    date = (year, month,)
    connection = mysql.connector.connect(host='localhost',
                                         database='ibm',
                                         user='root',
                                         password='paz1c')

    cursor = connection.cursor()
    sql = "SELECT * FROM photos WHERE YEAR(Created) = %s AND MONTH(Created) = %s;"
    cursor.execute(sql, date)
    result = cursor.fetchall()

    for x in result:
        print(x)


def filerYearMonthIsFixed(year, month, fixed):
    data = (year, month, fixed,)
    connection = mysql.connector.connect(host='localhost',
                                         database='ibm',
                                         user='root',
                                         password='paz1c')

    cursor = connection.cursor()
    sql = "SELECT * FROM photos WHERE YEAR(Created) = %s AND MONTH(Created) = %s AND Solve = %s;"
    cursor.execute(sql, data)
    result = cursor.fetchall()

    for x in result:
        print(x)


filerYearMonthIsFixed(input("Year: "), input("Month: "), input("Fixed: "))
