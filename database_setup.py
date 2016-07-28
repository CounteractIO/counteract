import rethinkdb as r

conn = r.connect('localhost', 28015)

r.db_create('luma').run(conn)
r.db('luma').table_create('users').run(conn)