from flask import Flask, render_template, g
from flask import request

app = Flask(__name__,
            static_url_path='',
            static_folder='./static')

from flask_compress import Compress
Compress(app)

import database
import rules

import time


@app.route("/")
def main():
    conn = database.get_db(g)
    save_history(request, conn, "INDEX", "")

    cur = conn.cursor()
    cur.execute("""select count(*) as cards, sum(totalwords) as t, sum(labeledwords) as l, (sum(labeledwords)*1.0)/sum(totalwords) as pct from cardlabels""")
    stats = cur.fetchall()[0]

    conn.close()

    return render_template('index.html', stats=stats)

@app.route("/search", methods = ['GET', 'POST'])
def get_search():
    conn = database.get_db(g)

    import json
    searchstr = json.dumps(request.form)
    app.logger.info("Search [%s]", searchstr)

    save_history(request, conn, "SEARCH", searchstr)

    sql = """SELECT * FROM cards AS c, cardlabels AS cl
             WHERE c.uuid = cl.uuid """
    params = []

    if request.method == 'POST':
        if 'cardname' in request.form and request.form['cardname'] != "":
            sql += "AND lower(c.name) like lower(?) "
            params.append('%' + request.form['cardname'] + '%')
        if 'text' in request.form and request.form['text'] != "":
            sql += "AND lower(c.text) like lower(?) "
            params.append('%' + request.form['text'] + '%')
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
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()

    data = {
        "labels": rules.get_labels(),
        "triggers": rules.get_trigger_labels(),
        "effects": rules.get_effect_labels()
    }
    conn.close()

    return render_template('search.html', rows=rows, data=data)

@app.route("/runrules")
def run_rules():
    start_time = time.time()

    conn = database.get_db(g)
    save_history(request, conn, "RUN_RULES", "")

    rules.run(app, conn)
    conn.close()

    elapsed_time = time.time() - start_time
    return "OK "+ str(elapsed_time)

@app.route("/setup")
def setup():
    start_time = time.time()

    conn = database.get_db(g)
    conn.execute("""CREATE TABLE IF NOT EXISTS history (
        dt datetime default current_timestamp,
        data TEXT,
        type TEXT,
        remote_addr TEXT,
        url TEXT
    ) """)
    conn.close()


    elapsed_time = time.time() - start_time
    return "OK "+ str(elapsed_time)

@app.route("/analize/<uuid>")
def analize_uuid(uuid):
    conn = database.get_db(g)
    save_history(request, conn, "ANALYZE", uuid)

    analysis = rules.analize(app, conn, uuid)
    return render_template('analysis.html', analysis=analysis)

@app.route("/history")
def history():
    conn = database.get_db(g)
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM history ORDER BY dt DESC
    """, [])
    rows = cur.fetchall()
    return render_template('history.html', history=rows)



def save_history(request, conn, htype, data):

    ip = request.remote_addr
    if "X-Real-IP" in request.headers:
        ip = request.headers['X-Real-IP']
    
    conn.execute("""
        INSERT INTO history (data, type, remote_addr, url)
        VALUES (?, ?, ?, ?)
    """, [data, htype, ip, request.url])
    conn.commit()


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['TESTING'] = True
    app.run(debug=True, host='0.0.0.0')
