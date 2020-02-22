from flask import Flask, render_template, g
from flask import request
app = Flask(__name__,
            static_url_path='',
            static_folder='./static')

import database
import rules

import time


@app.route("/")
def main():
    #return "Welcome!"
    return render_template('index.html')

@app.route("/search", methods = ['GET', 'POST'])
def get_search():
    conn = database.get_db(g)
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

    conn = database.get_db(g)
    rules.run(conn)

    elapsed_time = time.time() - start_time
    return "OK "+ str(elapsed_time)

@app.route("/analize/<uuid>")
def analize_uuid(uuid):
    conn = database.get_db(g)
    analysis = rules.analize(conn, uuid)
    return render_template('analysis.html', analysis=analysis)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['TESTING'] = True
    app.run(debug=True)
