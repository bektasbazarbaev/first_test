from connect import connec
def creat_table():
    conn=connec()
    cur=conn.cursor()
    cur.execute("""
          CREATE TABLE IF NOT EXISTS bd20(
                id serial primary key,
                name varchar(255),
                soname varchar(255),
                phone varchar(255)

                )  
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_person(name,soname,phone):
    
    conn=connec()
    cur=conn.cursor()
    cur.execute(
        "INSERT INTO bd20(name,soname,phone) VALUES(%s,%s,%s)",
        (name,soname,phone)
    )
    conn.commit()
    cur.close()
    conn.close()


add_person("Ali", "Nazarov", "87771234567")
add_person("Aisha", "Kuzbayeva", "87779876543")

def show():
    conn=connec()
    cur=conn.cursor()
    cur.execute("SELECT * FROM bd20")
    row=cur.fetchall()
    for i in row:
        print(i)
    conn.commit()
    cur.close()
    conn.close()

