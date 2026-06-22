import os
import mysql.connector
from mysql.connector import pooling
from flask import Flask, jsonify

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "employeesdb"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "password")
}

connection_pool = None

def get_connection():
    global connection_pool

    if connection_pool is None:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="home_pool",
            pool_size=5,
            **db_config
        )

    return connection_pool.get_connection()

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({
        "status": "healthy",
        "service": "home-api"
    })

@app.route("/health")
def health_check():
    return jsonify({
        "status": "UP"
    }), 200

@app.route("/employees")
def employees():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name, department
            FROM employees
        """)

        employees = cursor.fetchall()

        return jsonify({
            "count": len(employees),
            "employees": employees
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)