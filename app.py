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
import json

def get_stats(conn):
    cur = conn.cursor()
    cur.execute("""select count(*) as cards, sum(totalwords) as t, sum(labeledwords) as l, (sum(labeledwords)*1.0)/sum(totalwords) as pct from cardlabels""")
    stats = cur.fetchall()[0]
    return stats


@app.route("/")
def main():
    conn = database.get_db(g)
    database.save_history(request, conn, "INDEX", "")

    stats = get_stats(conn)

    conn.close()

    return render_template('index.html', stats=stats)

@app.route("/search", methods = ['GET'])
def get_search():
    conn = database.get_db(g)

    import json
    searchstr = json.dumps(request.args)
    app.logger.info("Search [%s]", searchstr)
    app.logger.info("Search2 [%s]", request)

    database.save_history(request, conn, "SEARCH", searchstr)

    sql = """SELECT * FROM cards AS c, cardlabels AS cl
             WHERE c.uuid = cl.uuid """
    params = []

    if request.method == 'GET':
        if 'cardname' in request.args and request.args['cardname'] != "":
            sql += "AND lower(c.name) like lower(?) "
            params.append('%' + request.args['cardname'] + '%')
        if 'text' in request.args and request.args['text'] != "":
            sql += "AND lower(c.text) like lower(?) "
            params.append('%' + request.args['text'] + '%')
        if 'trigger' in request.args:
            triggers = request.args.getlist("trigger")
            app.logger.info("trigger [%s]", triggers)
            for tr in triggers:
                sql += "AND lower(cl.labels) like lower(?) "
                params.append('%' + tr + '%')
        if 'effect' in request.args and request.args['effect'] != "":
            sql += "AND lower(cl.labels) like lower(?) "
            params.append('%' + request.args['effect'] + '%')

        if 'colormode' in request.args:
            colormode = request.args['colormode']
            colors = ['R', 'U', 'G', 'W', 'B']
            if colormode == 'any':
                anyfilter = False
                sql += "AND ( "
                if "color_C" in request.args:
                    sql += "( c.colors IS NULL ) OR "
                    anyfilter = True
                for c in colors:
                    if 'color_' + c in request.args:
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
                if "color_C" in request.args:
                    sql += "( c.colors IS NULL ) AND "
                    anyfilter = True
                for c in colors:
                    if 'color_' + c in request.args:
                        sql += "(c.colors like '%" +c+ "%') AND "
                        anyfilter = True

                if anyfilter:
                    sql += "1=1"
                else:
                    sql += "1=0"
                sql += ")"

    #sql += " ORDER BY name "
    # DEBUG
    sql += " ORDER BY labeledpct ASC "

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
    database.save_history(request, conn, "RUN_RULES", "")

    rules.run(app, conn)

    stats = get_stats(conn)
    statsObj = {}
    for k in stats.keys():
        statsObj[k] = stats[k]
    database.save_history(request, conn, "RUN_RULES_RESULT", json.dumps(statsObj))

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

@app.route("/analize/<name>")
def analize_uuid(name):
    conn = database.get_db(g)
    database.save_history(request, conn, "ANALYZE", name)

    analysis = rules.analize(app, conn, name)
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


class Node:
    def __init__(self, id, group):
        self.id = id
        self.group = group

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return '{{"id": "{}", "group": {}}}'.format(self.id, self.group)

@app.route("/graph")
def graph():
    conn = database.get_db(g)
    cur = conn.cursor()

    sql = """SELECT * FROM cards AS c, cardlabels AS cl
             WHERE c.uuid = cl.uuid 
             AND cl.labels LIKE "%DRAW%"
             AND colors = "R"
             """

    cur.execute(sql, [])
    rows = cur.fetchall()

    nodes = set()
    links = []
    for row in rows:
        cardname = row["name"]
        cardname = cardname.replace("'", "\'")
        nodes.add(Node(cardname, 1))

        labelsStr = row["labels"]
        if len(labelsStr) > 0:
            labels = labelsStr.split(',')

            for label in labels:
                label = label.strip()

                if label.startswith('ON_'):
                    fromLabel = label[3:]
                    nodes.add(Node(fromLabel, 3))
                    links.append({"source": fromLabel, "target": cardname})
                else:
                    nodes.add(Node(label, 2))
                    links.append({"source": cardname, "target": label})

    graphdata = {
        "nodes": list(nodes),
        "links": links
    }    
    
    return render_template('graph.html', graphdata=graphdata)


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['TESTING'] = True
    app.run(debug=True, host='0.0.0.0', port=5555)
