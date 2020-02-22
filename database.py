import sqlite3

def connect_db():
    """Connects to the specific database."""
    conn = sqlite3.connect('./cards.sqlite')
    conn.execute("ATTACH DATABASE 'AllPrintings.sqlite' AS AllPrintings")
    conn.row_factory = sqlite3.Row
    return conn


def get_db(g):
    """Opens a new database connection if there is none yet for the
     current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
