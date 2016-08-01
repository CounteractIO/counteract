import rethinkdb as r

conn = r.connect('localhost', 28015)

r.db_create('athena').run(conn)
r.db('athena').table_create('users').run(conn)