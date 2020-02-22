from flask import Flask, render_template, g
from flask import request
app = Flask(__name__,
            static_url_path='',
            static_folder='./static')

import sqlite3

import rules
from rules import run

import time

def connect_db():
    """Connects to the specific database."""
    conn = sqlite3.connect('./cards.sqlite')
    conn.execute("ATTACH DATABASE 'AllPrintings.sqlite' AS AllPrintings")
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """Opens a new database connection if there is none yet for the
     current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.route("/")
def main():
    #return "Welcome!"
    return render_template('index.html')

@app.route("/search", methods = ['GET', 'POST'])
def get_search():
    conn = get_db()
    cur = conn.cursor()

    sql = """SELECT * FROM cards AS c, cardlabels AS cl
             WHERE c.uuid = cl.uuid """
    params = []

    if request.method == 'POST':
        if 'cardname' in request.form and request.form['cardname'] != "":
            sql += "AND lower(c.name) like lower(?) "
            params.append('%' + request.form['cardname'] + '%')
        if 'trigger' in request.form and request.form['trigger'] != "":
            sql += "AND lower(cl.labels) like lower(?) "
            params.append('%' + request.form['trigger'] + '%')
        if 'effect' in request.form and request.form['effect'] != "":
            sql += "AND lower(cl.labels) like lower(?) "
            params.append('%' + request.form['effect'] + '%')

        if 'colormode' in request.form:
            colormode = request.form['colormode']
            colors = ['R', 'U', 'G', 'W', 'B']
            if colormode == 'any':
                anyfilter = False
                sql += "AND ( "
                if "color_NULL" in request.form:
                    sql += "( c.colors IS NULL ) OR "
                    anyfilter = True
                for c in colors:
                    if 'color_' + c in request.form:
                        sql += "(c.colors like '%" +c+ "%') OR "
                        anyfilter = True

                if anyfilter:
                    sql += "1=0"
                else:
                    sql += "1=1"
                sql += ")"

            elif colormode == 'all':
                anyfilter = False
                sql += "AND ( "
                if "color_NULL" in request.form:
                    sql += "( c.colors IS NULL ) AND "
                    anyfilter = True
                for c in colors:
                    if 'color_' + c in request.form:
                        sql += "(c.colors like '%" +c+ "%') AND "
                        anyfilter = True

                if anyfilter:
                    sql += "1=1"
                else:
                    sql += "1=0"
                sql += ")"

    app.logger.info("sql: [%s]", sql)
    app.logger.info("params: [%s]", params)
    cur.execute(sql, params)
    rows = cur.fetchall()

    data = {
        "labels": rules.get_labels(),
        "triggers": rules.get_trigger_labels(),
        "effects": rules.get_effect_labels()
    }

    return render_template('search.html', rows=rows, data=data)

@app.route("/runrules")
def run_rules():
    start_time = time.time()
    run()
    elapsed_time = time.time() - start_time
    return "OK "+ str(elapsed_time)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['TESTING'] = True
    app.run(debug=True)
