from flask import Flask, render_template
from flask import request
app = Flask(__name__)

import sqlite3

from rules import run

@app.route("/")
def main():
    #return "Welcome!"
    return render_template('index.html')

@app.route("/search", methods = ['GET', 'POST'])
def get_search():
    conn = sqlite3.connect('./cards.sqlite')
    conn.execute("ATTACH DATABASE 'AllPrintings.sqlite' AS AllPrintings")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cardname = "%"
    label = "%"
    if request.method == 'POST':
        cardname = "%" + request.form['cardname'] + "%"
        label = "%" + request.form['label'] + "%"

    cur.execute("""SELECT * FROM cards AS c, cardlabels AS cl
        WHERE c.uuid = cl.uuid
        AND lower(c.name) like lower(?)
        AND lower(cl.labels) like lower(?)
    """, [cardname, label])
    rows = cur.fetchall()
    return render_template('search.html', rows=rows)

@app.route("/runrules")
def run_rules():
    run(5)
    return "OK"

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['TESTING'] = True
    app.run(debug=True)
