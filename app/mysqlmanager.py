# start includeing librarys that we need for work
import mysql.connector
import datetime
import time
import collect,config,main

def connect_to_database():
    '''this function make connection to mysql service'''

    db = mysql.connector.connect(
        host=config.host,
        user=config.user,
        passwd=config.passwd,
        db=config.db,
        charset=config.charset,
        auth_plugin=config.auth_plugin
    )

    return db

def reading_ledstatus_from_database():
    '''this function read ledstatuss from mysql database from past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM ledstatus;")
    db.close()
    return cur.fetchall()

def reading_relaystatus_from_database():
    '''this function read relaystatuss from mysql database from  past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM relaystatus;")
    db.close()
    return cur.fetchall()

def reading_servostatus_from_database():
    '''this function read servostatus from mysql database from  past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM servostatus;")
    db.close()
    return cur.fetchall()

def reading_pirstatus_from_database():
    '''this function read pirstatuss from mysql database from past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM pirstatus;")
    db.close()
    return cur.fetchall()

def reading_irstatus_from_database():
    '''this function read irstatuss from mysql database from past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM irstatus;")
    db.close()
    return cur.fetchall()

def reading_dhtstatus_from_database():
    '''this function read dhtstatuss from mysql database from past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM dhtstatus;")
    db.close()
    return cur.fetchall()            

def reading_alldatas_to_database():
    '''this function read alldatas statuss from mysql database from past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM alldatasstatus;")
    db.close()
    return cur.fetchall() 

def reading_alllatestdatas_to_database():
    '''this function read alllatestdatas statuss from mysql database from past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM alldatasstatus ORDER BY timestamp DESC LIMIT 1;")
    db.close()
    return cur.fetchall() 

def reading_writedatas_to_database():
    '''this function read allwritedatas statuss from mysql database from past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM allwritedatasstatus;")
    db.close()
    return cur.fetchall()         

def reading_latestwritedatas_to_database():
    '''this function read alllatestwritedatas statuss from mysql database from past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM allwritedatasstatus ORDER BY time DESC LIMIT 1;")
    db.close()
    return cur.fetchall()

def reading_latestdhtstatus_to_database():
    '''this function read latestdhtstatus statuss from mysql database from past to today and return them'''

    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM dhtstatus ORDER BY timestamp DESC LIMIT 1;")
    db.close()
    return cur.fetchall()

def writing_ledstatus_to_database(redled, yellowled, timestamp):
    '''this function write collected ledstatuss to mysql database with timestamp'''

    db = connect_to_database()    
    cur = db.cursor()
    qury = f'INSERT INTO ledstatus VALUES ("{redled}","{yellowled}","{timestamp}");'
    cur.execute(qury)
    db.commit()
    db.close()

def writing_relaystatus_to_database(light, fans, timestamp):
    '''this function write collected relaystatuss to mysql database with timestamp'''

    db = connect_to_database()    
    cur = db.cursor()
    qury = f'INSERT INTO relaystatus VALUES ("{light}","{fans}","{timestamp}");'
    cur.execute(qury)
    db.commit()
    db.close()

def writing_servostatus_to_database(servostatus,timestamp):
    '''this function write collected servostatus to mysql database with timestamp'''

    db = connect_to_database()    
    cur = db.cursor()
    qury = f'INSERT INTO servostatus VALUES ("{servostatus}","{timestamp}");'
    cur.execute(qury)
    db.commit()
    db.close()    

def writing_pirstatus_to_database(motion,timestamp):
    '''this function write collected pirstatuss to mysql database with timestamp'''

    db = connect_to_database()    
    cur = db.cursor()
    qury = f'INSERT INTO pirstatus VALUES ("{motion}","{timestamp}");'
    cur.execute(qury)
    db.commit()
    db.close()

def writing_irstatus_to_database(switch,timestamp):
    ''' this function write collected irstatuss to mysql databse with timestamp'''

    db = connect_to_database()    
    cur = db.cursor()
    qury = f'INSERT INTO irstatus VALUES ("{switch}","{timestamp}");'
    cur.execute(qury)
    db.commit()
    db.close()    

def writing_dhtstatus_to_database(hum, temp, timestamp):
    '''this function write collected dhtstatuss to mysql database with timestamp'''

    db = connect_to_database()    
    cur = db.cursor()
    qury = f'INSERT INTO dhtstatus VALUES ("{hum}","{temp}","{timestamp}");'
    cur.execute(qury)
    db.commit()
    db.close()    

def writing_alldatas_to_database(hum, temp, motion, switch, redled, yellowled, light, fans, servostatus, timestamp):
    '''this function write all collected datas to mysql database with timestamp'''

    db = connect_to_database()    
    cur = db.cursor()
    qury = f'INSERT INTO alldatasstatus VALUES ("{hum}","{temp}","{motion}","{switch}","{redled}","{yellowled}","{light}","{fans}","{servostatus}","{timestamp}");'
    cur.execute(qury)
    db.commit()
    db.close()

def writing_writedatas_to_database(title, name, weight, hight, temp, Score, discr, time):
    '''this function write all collected datas to mysql database with timestamp'''

    db = connect_to_database()    
    cur = db.cursor()
    qury = f'INSERT INTO allwritedatasstatus VALUES ("{title}","{name}","{weight}","{hight}","{temp}","{Score}","{discr}","{time}");'
    cur.execute(qury)
    db.commit()
    db.close()
