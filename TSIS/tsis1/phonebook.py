import csv
import json
from connect import connect


def run_sql_file(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, "r") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()


def setup_database():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")
    print("Database is ready.")


def get_group_id(cur, group_name):
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT(name) DO NOTHING",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
    return cur.fetchone()[0]


def add_contact(name, phone, phone_type, email, birthday, group_name):
    conn = connect()
    cur = conn.cursor()

    group_id = get_group_id(cur, group_name)

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT(name) DO UPDATE
        SET email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        RETURNING id
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()


def insert_from_console():
    name = input("Name: ")
    phone = input("Phone: ")
    phone_type = input("Phone type (home/work/mobile): ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")

    add_contact(name, phone, phone_type, email, birthday, group_name)
    print("Contact added.")


def import_from_csv(filename):
    with open(filename, newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            name, phone, phone_type, email, birthday, group_name = row
            add_contact(name, phone, phone_type, email, birthday, group_name)

    print("CSV imported.")


def show_all(sort_by="name"):
    allowed = {
        "name": "c.name",
        "birthday": "c.birthday",
        "date": "c.created_at"
    }

    sort_column = allowed.get(sort_by, "c.name")

    conn = connect()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY {sort_column}
    """)

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def filter_by_group(group_name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name ILIKE %s
    """, (group_name,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def search_by_email(email_part):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, email, birthday
        FROM contacts
        WHERE email ILIKE %s
    """, ("%" + email_part + "%",))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def advanced_search(query):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def add_phone_to_contact():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type (home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added.")


def move_contact_to_group():
    name = input("Contact name: ")
    group_name = input("New group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved to group.")


def export_to_json(filename):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    contacts = []

    for contact_id, name, email, birthday, group_name in cur.fetchall():
        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id=%s
        """, (contact_id,))

        phones = []
        for phone, phone_type in cur.fetchall():
            phones.append({
                "phone": phone,
                "type": phone_type
            })

        contacts.append({
            "name": name,
            "email": email,
            "birthday": str(birthday),
            "group": group_name,
            "phones": phones
        })

    with open(filename, "w") as file:
        json.dump(contacts, file, indent=4)

    cur.close()
    conn.close()

    print("Exported to JSON.")


def import_from_json(filename):
    with open(filename, "r") as file:
        contacts = json.load(file)

    for contact in contacts:
        name = contact["name"]

        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} already exists. skip/overwrite? ")

            if choice == "skip":
                cur.close()
                conn.close()
                continue

            elif choice == "overwrite":
                contact_id = exists[0]

                # Delete old phone numbers before inserting new ones
                cur.execute("DELETE FROM phones WHERE contact_id=%s", (contact_id,))
                conn.commit()

            else:
                print("Invalid choice. Skipping contact.")
                cur.close()
                conn.close()
                continue

        cur.close()
        conn.close()

        for phone_data in contact["phones"]:
            add_contact(
                contact["name"],
                phone_data["phone"],
                phone_data["type"],
                contact["email"],
                contact["birthday"],
                contact["group"]
            )

    print("JSON imported.")


def paginated_view():
    page = 0
    limit = 3

    while True:
        offset = page * limit

        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.name
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        print(f"\nPage {page + 1}")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

        command = input("next / prev / quit: ")

        if command == "next":
            page += 1
        elif command == "prev" and page > 0:
            page -= 1
        elif command == "quit":
            break


def main():
    while True:
        print("""
1. Setup database
2. Add contact
3. Import CSV
4. Show all
5. Filter by group
6. Search by email
7. Advanced search
8. Add phone
9. Move to group
10. Export JSON
11. Import JSON
12. Paginated view
0. Exit
""")

        choice = input("> ")

        if choice == "1":
            setup_database()

        elif choice == "2":
            insert_from_console()

        elif choice == "3":
            import_from_csv("contacts.csv")

        elif choice == "4":
            sort_by = input("Sort by name / birthday / date: ")
            show_all(sort_by)

        elif choice == "5":
            filter_by_group(input("Group name: "))

        elif choice == "6":
            search_by_email(input("Email search: "))

        elif choice == "7":
            advanced_search(input("Search query: "))

        elif choice == "8":
            add_phone_to_contact()

        elif choice == "9":
            move_contact_to_group()

        elif choice == "10":
            export_to_json("contacts.json")

        elif choice == "11":
            import_from_json("contacts.json")

        elif choice == "12":
            paginated_view()

        elif choice == "0":
            break


if __name__ == "__main__":
    main()