import sqlite3
from datetime import datetime, timedelta

def connect_db():
    con = sqlite3.connect("data/otp.db")
    return con

def create_table():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS otp_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    otp TEXT NOT NULL UNIQUE,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    con.commit()
    con.close()
    print('Table create successfully!')

create_table()

def set_otp(letter):
   
    con = connect_db()
    cur = con.cursor()
        
    otp = letter
    expires_at = (datetime.now() + timedelta(minutes=15)).isoformat()
            
    cur.execute(""" insert into otp_data (otp, expires_at) values (?, ?) """, (otp, expires_at) )
        
    con.commit()
    con.close()
    # print("otp insert successfully")
  
    

# set_otp()

def verify(otp):
    con = connect_db()
    cur = con.cursor()

    cur.execute("""select id, expires_at from otp_data where otp = ?""", (otp,))
    row = cur.fetchone()
    con.close()
    if row is None:
        return {"success":False,"message":"Invalid OTP"}
    
    otp_id, expires_at  = row

    expires_at = datetime.fromisoformat(expires_at)

    if datetime.now() > expires_at:
        return {"valid":False, "message":"OTP has expired" }
    else:
        return {"valid":True, "message":"OTP verified successfully" }
    
