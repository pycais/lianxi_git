
def fetchall_to_dict(cursor):
    description = [i[0] for i in cursor.description]
    data = [dict(zip(description, i)) for i in cursor.fetchall()]
    return data