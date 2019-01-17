import psycopg2 

try:
    conn = psycopg2.connect(database = 'rfenzo',
                          user = 'rfenzo',
                          host = 'localhost',
                          password = '12345')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Aux')
    cur.execute('CREATE TABLE Aux(value int primary key)')
    rCursor = conn.cursor()
    sCursor = conn.cursor()
    rCursor.execute('SELECT * FROM R')
    sCursor.execute('SELECT * FROM S')

    rRow = rCursor.fetchone()
    sRow = sCursor.fetchone()
    while rRow and sRow:
        if rRow[0] > sRow[0]:
            cur.execute('INSERT INTO Aux (value) VALUES(%s)', sRow)
            sRow = sCursor.fetchone()
        elif rRow[0] < sRow[0]:
            cur.execute('INSERT INTO Aux (value) VALUES(%s)', rRow)
            rRow = rCursor.fetchone()
        else:
            rRow = rCursor.fetchone()
            sRow = sCursor.fetchone()
    #GuardarlatablaAux
    conn.commit()
    conn.close()
    cur.close()
    rCursor.close()
    sCursor.close()
except Exception as e:
    print('Hubounproblema')
    print(e)