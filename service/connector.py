import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            dbname="postgres",  
            user="postgres",      
            password="040612", 
            host="localhost",
            port="5432"           
        )
        conn.autocommit = False 
        
        print("Connected successfully")
        return conn
    except psycopg2.Error as e:
        print(f"Failed to connected PostGres: {e}")
        return
    
def disconnect(conn, cursor=None):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        