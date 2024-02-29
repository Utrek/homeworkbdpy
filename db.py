import psycopg2

def create_db (conn):
    with conn.cursor() as cur:
        cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS Clients(
                    id SERIAL PRIMARY KEY,
                    First_name VARCHAR NOT NULL,
                    Last_name VARCHAR NOT NULL,
                    Email VARCHAR NOT NULL);
                    """)
        cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS Phones(
                    id SERIAL PRIMARY KEY,
                    Client_id INTEGER not null REFERENCES Clients(id),
                    Number INTEGER UNIQUE);
                    """)
        
def add_client (conn, first_name, last_name, email, phones = None):
     with conn.cursor() as cur:
          cur.execute(""" 
                    INSERT INTO Clients(First_name,Last_name,Email) VALUES(%s, %s, %s) RETURNING id;;
                    """,(first_name,last_name,email))
          id = cur.fetchone()
          cur.execute(""" 
                    INSERT INTO Phones(Client_id,Number) VALUES(%s, %s) RETURNING id;
                    """,(id, phones))
          
def add_phone (conn,client_id,phone):
     with conn.cursor() as cur:
          cur.execute("""
                      INSERT INTO Phones(Client_id,Number) VALUES(%s, %s) RETURNING id;
                      """,(client_id, phone))
          
def add_phone2(conn, first_name, last_name, email,phone):
     with conn.cursor() as cur:
          cur.execute(""" 
                      SELECT id FROM Clients WHERE First_name=%s AND Last_name = %s AND Email=%s;
                      """, (first_name,last_name,email))
          id = cur.fetchone()[0]
          cur.execute("""
                      INSERT INTO Phones(Client_id,Number) VALUES(%s, %s) RETURNING id;
                      """,(id, phone))
          
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
      with conn.cursor() as cur:
        if first_name:
               cur.execute(""" 
                           UPDATE Clients SET First_name=%s WHERE id=%s;
                           """, (first_name,client_id))
        else:
             pass
        if last_name:
             cur.execute(""" 
                           UPDATE Clients SET Last_name=%s WHERE id=%s;
                           """, (last_name,client_id))
        else:
             pass 
        if email:
             cur.execute(""" 
                           UPDATE Clients SET Email=%s WHERE id=%s;
                           """, (email,client_id))
        else:
             pass 
        if phone:
             cur.execute("""
                      UPDATE Phones SET Number=%s WHERE id=%s;
                      """,(phone,client_id))
        else:
             pass
        
def delete_phone(conn, client_id, phone):
     with conn.cursor() as cur:
          cur.execute(""" 
                       DELETE FROM Phones WHERE client_id=%s and number=%s;
                      """,(client_id,phone))

def delete_client(conn, client_id):
    with conn.cursor() as cur:
          cur.execute(""" 
                       DELETE FROM Phones WHERE client_id=%s;
                      """,(client_id,))
          cur.execute(""" 
                       DELETE FROM Clients WHERE id=%s;
                      """,(client_id,))

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
     with conn.cursor() as cur:
        with conn.cursor() as cur:
            if phone:
               cur.execute(""" 
                      SELECT Client_id FROM Phones WHERE Number=%s;
                      """, (phone,))
               id = cur.fetchone()[0]
               cur.execute(""" 
                      SELECT First_name, Last_name,Email FROM Clients WHERE id=%s;
                      """, (id,))
               client = cur.fetchall()
               print ('Client:', client[0][0],client[0][1], 'Email:', client[0][2])
            elif email: 
                 cur.execute(""" 
                      SELECT id FROM Clients WHERE Email=%s;
                      """, (email,))
                 list_id = cur.fetchall()
                 for id_tuple in list_id:
                      id= id_tuple[0]
                      cur.execute(""" 
                                  SELECT First_name, Last_name, Email FROM Clients WHERE id=%s;
                                  """, (id,))
                      client = cur.fetchall()
                      print ('Client:', client[0][0],client[0][1], 'Email:', client[0][2])
            elif first_name and last_name:
                 cur.execute(""" 
                      SELECT id FROM Clients WHERE first_name=%s and last_name=%s;
                      """, (first_name,last_name))
                 list_id = cur.fetchall()
                 for id_tuple in list_id:
                      id= id_tuple[0]
                      cur.execute(""" 
                                  SELECT First_name, Last_name, Email FROM Clients WHERE id=%s;
                                  """, (id,))
                      client = cur.fetchall()
                      print ('Client:', client[0][0],client[0][1], 'Email:', client[0][2])
            elif first_name:
                 cur.execute(""" 
                      SELECT id FROM Clients WHERE first_name=%s;
                      """, (first_name,))
                 list_id = cur.fetchall()
                 for id_tuple in list_id:
                      id= id_tuple[0]
                      cur.execute(""" 
                                  SELECT First_name, Last_name, Email FROM Clients WHERE id=%s;
                                  """, (id,))
                      client = cur.fetchall()
                      print ('Client:', client[0][0],client[0][1], 'Email:', client[0][2])
            elif last_name:
                 cur.execute(""" 
                      SELECT id FROM Clients WHERE last_name=%s;
                      """, (last_name,))
                 list_id = cur.fetchall()
                 for id_tuple in list_id:
                      id= id_tuple[0]
                      cur.execute(""" 
                                  SELECT First_name, Last_name, Email FROM Clients WHERE id=%s;
                                  """, (id,))
                      client = cur.fetchall()
                      print ('Client:', client[0][0],client[0][1], 'Email:', client[0][2])
            else:
              pass  
         
def find_client_phones(conn, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
         if email: 
                 cur.execute(""" 
                      SELECT id FROM Clients WHERE Email=%s;
                      """, (email,))
                 list_id = cur.fetchall()
                 for id_tuple in list_id:
                      id= id_tuple[0]
                      cur.execute(""" 
                                  SELECT First_name, Last_name FROM Clients WHERE id=%s;
                                  """, (id,))
                      client = cur.fetchall()
                      cur.execute(""" 
                      SELECT number FROM Phones WHERE Client_id=%s;
                      """, (id,))
                      number_list = cur.fetchall()
                      print ('Client:', client[0][0],client[0][1])
                      for number_tuple in number_list:
                           number = number_tuple[0]
                           print('Phone:', number) 
         elif first_name: 
                 cur.execute(""" 
                      SELECT id FROM Clients WHERE First_name=%s;
                      """, (first_name,))
                 list_id = cur.fetchall()
                 for id_tuple in list_id:
                      id= id_tuple[0]
                      cur.execute(""" 
                                  SELECT First_name, Last_name FROM Clients WHERE id=%s;
                                  """, (id,))
                      client = cur.fetchall()
                      cur.execute(""" 
                      SELECT number FROM Phones WHERE Client_id=%s;
                      """, (id,))
                      number_list = cur.fetchall()
                      print ('Client:', client[0][0],client[0][1])
                      for number_tuple in number_list:
                           number = number_tuple[0]
                           print('Phone:', number)
         elif last_name: 
                 cur.execute(""" 
                      SELECT id FROM Clients WHERE Last_name=%s;
                      """, (last_name,))
                 list_id = cur.fetchall()
                 for id_tuple in list_id:
                      id= id_tuple[0]
                      cur.execute(""" 
                                  SELECT First_name, Last_name FROM Clients WHERE id=%s;
                                  """, (id,))
                      client = cur.fetchall()
                      cur.execute(""" 
                      SELECT number FROM Phones WHERE Client_id=%s;
                      """, (id,))
                      number_list = cur.fetchall()
                      print ('Client:', client[0][0],client[0][1])
                      for number_tuple in number_list:
                           number = number_tuple[0]
                           print('Phone:', number)  
    
     

with psycopg2.connect(database="Client_base", user="postgres", password="0956") as conn:
       with conn.cursor() as cur:
            cur.execute("""
                        DROP TABLE Phones;
                        DROP TABLE Clients;
                        """)
       create_db(conn)
       add_client(conn, 'Joe', 'Black', '1@mail.ru', 555555)
       add_client(conn, 'Yorik', 'Scull', '4@mail.ru', 585555)
       add_client(conn, 'Bart', 'Grey', '4@mail.ru', 585585)
       add_client(conn, 'Gomer', 'Simpson','4@yandex.ru', 333333)
       add_phone(conn,1,666545)
       add_phone2(conn, 'Joe', 'Black', '1@mail.ru', 777777)
       change_client(conn,1,'Lisa','Simpson','2@yandex.ru',222222)
       change_client(conn,1,'Bart',None,'4@yandex.ru',None)
       delete_phone(conn,1, 666545)
       delete_client(conn, 2)
       find_client(conn, None,None,'4@yandex.ru', None)
       find_client_phones(conn,None,'Simpson',None)








    