from flask import Flask, jsonify, request
from connect import connect, init_tables

app = Flask(__name__)

@app.route('/api/projects', methods=['GET'])
def get_project():
    with app.app_context():
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM PROJECT')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        projects = [
            {'id': row[0], 'name': row[1], 'description': row[2], 'url': row[3]}
            for row in rows
        ]
        return jsonify(projects).json


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)