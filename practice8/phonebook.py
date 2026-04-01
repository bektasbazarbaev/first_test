from connect import connec

def create_table():
    conn = connec()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def insert_or_update():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connec()
    cur = conn.cursor()
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()


def insert_many():
    n = int(input("How many contacts to insert? "))
    names = []
    phones = []
    for i in range(n):
        names.append(input(f"Name {i+1}: "))
        phones.append(input(f"Phone {i+1}: "))

    conn = connec()
    cur = conn.cursor()
    cur.execute("CALL insert_many_users(%s, %s, %s)", (names, phones, None))
    conn.commit()
    cur.close()
    conn.close()


def query_contacts():
    print("1 - All contacts")
    print("2 - Search by name")
    print("3 - Search by phone prefix")
    choice = input("Choose option: ")

    conn = connec()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook ORDER BY id")
    elif choice == "2":
        name = input("Enter name pattern: ")
        cur.execute("SELECT * FROM search_contacts(%s)", (name,))
    elif choice == "3":
        prefix = input("Enter phone prefix: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + '%',))

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = connec()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_user():
    value = input("Enter name or phone to delete: ")

    conn = connec()
    cur = conn.cursor()
    cur.execute("CALL delete_user(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()


def main():
    create_table()

    while True:
        print("\nPhoneBook Menu:")
        print("1 - Insert or update contact")
        print("2 - Insert many contacts")
        print("3 - Query contacts")
        print("4 - Pagination")
        print("5 - Delete contact")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_or_update()
        elif choice == "2":
            insert_many()
        elif choice == "3":
            query_contacts()
        elif choice == "4":
            pagination()
        elif choice == "5":
            delete_user()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()