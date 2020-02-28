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


def save_history(request, conn, htype, data):

    ip = request.remote_addr
    if "X-Real-IP" in request.headers:
        ip = request.headers['X-Real-IP']
    
    conn.execute("""
        INSERT INTO history (data, type, remote_addr, url)
        VALUES (?, ?, ?, ?)
    """, [data, htype, ip, request.url])
    conn.commit()