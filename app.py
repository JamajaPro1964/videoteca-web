from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def conexion():

    con = sqlite3.connect(
        "peliculas.db"
    )

    con.row_factory = sqlite3.Row

    return con

@app.route("/")
def inicio():

    buscar = request.args.get(
        "buscar",
        ""
    )

    con = conexion()

    cur = con.cursor()

    if buscar:

        cur.execute(
            """
            SELECT
                rowid,
                Titulo,
                Anio,
                RutaCaratula
            FROM peliculas
            WHERE Titulo LIKE ?
            ORDER BY Titulo
            """,
            (f"%{buscar}%",)
        )

    else:

        cur.execute(
            """
            SELECT
                rowid,
                Titulo,
                Anio,
                RutaCaratula
            FROM peliculas
            ORDER BY Titulo
            LIMIT 100
            """
        )

    peliculas = cur.fetchall()

    con.close()

    return render_template(
        "index.html",
        peliculas=peliculas,
        buscar=buscar
    )


@app.route("/pelicula/<int:id>")
def pelicula(id):

    con = conexion()

    cur = con.cursor()

    cur.execute(
        """
        SELECT *
        FROM peliculas
        WHERE rowid=?
        """,
        (id,)
    )

    pelicula = cur.fetchone()

    con.close()

    return render_template(
        "pelicula.html",
        pelicula=pelicula
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )




