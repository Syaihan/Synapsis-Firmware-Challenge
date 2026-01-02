import mysql.connector
from flask import Flask, request, jsonify
from datetime import datetime
from function.helper import generateNodeId, formatResponse


class NodeController:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "ProjectDB"
        }


    def getConnection(self):
        return mysql.connector.connect(**self.db_config)


    def getAllNodes(self):
        conn = self.getConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id AS node_id, name, updated_at FROM nodeDB")
        nodes = cursor.fetchall()
        
        for node in nodes:
            node["updated_at"] = node["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
            node["total_sensor"] = "0" 
            
        cursor.close()
        conn.close()
        return nodes


    def createNode(self, name):
        node_id = generateNodeId()
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = self.getConnection()
        cursor = conn.cursor()
        query = "INSERT INTO nodeDB (id, name, updated_at) VALUES (%s, %s, %s)"
        cursor.execute(query, (node_id, name, updated_at))
        conn.commit()
        cursor.close()
        conn.close()
        return self.getAllNodes()


    def updateNode(self, node_id, name):
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = self.getConnection()
        cursor = conn.cursor()
        query = "UPDATE nodeDB SET name = %s, updated_at = %s WHERE id = %s"
        cursor.execute(query, (name, updated_at, node_id))
        conn.commit()
        cursor.close()
        conn.close()
        return self.getAllNodes()


    def deleteNode(self, node_id):
        conn = self.getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM nodeDB WHERE id = %s", (node_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return self.getAllNodes()


app = Flask(__name__)
node_controller = NodeController()


@app.route("/api/read/node", methods=["GET"])
def readNode():
    try:
        data = node_controller.getAllNodes()
        return jsonify(formatResponse("Success", "Data berhasil diambil", data)), 200
    except Exception as e:
        return jsonify(formatResponse("Failed", str(e))), 500


@app.route("/api/create/node", methods=["POST"])
def createNode():
    try:
        name = request.json.get("name")
        data = node_controller.createNode(name)
        return jsonify(formatResponse("Success", "Data berhasil ditambahkan", data)), 201
    except Exception as e:
        return jsonify(formatResponse("Failed", str(e))), 500


@app.route("/api/update/node", methods=["PUT"])
def updateNode():
    try:
        node_id = request.json.get("node_id")
        name = request.json.get("name")
        data = node_controller.updateNode(node_id, name)
        return jsonify(formatResponse("Success", "Data berhasil diupdate", data)), 200
    except Exception as e:
        return jsonify(formatResponse("Failed", str(e))), 500


@app.route("/api/delete/node", methods=["DELETE"])
def deleteNode():
    try:
        node_id = request.json.get("id")
        data = node_controller.deleteNode(node_id)
        return jsonify(formatResponse("Success", "Data berhasil dihapus", data)), 200
    except Exception as e:
        return jsonify(formatResponse("Failed", str(e))), 500


if __name__ == "__main__":
    app.run(port=8080, debug=True)