import psycopg2
import pandas as pd

fterospostgres = {
    "host": "ec2-35-171-66-64.compute-1.amazonaws.com",
    "user": "u9d5na024rb5gk",
    "pwd": "p6c7efd1c875b51bad733a9ee730243755fa16d8763f937ef5a9249a61051b8c7",
    "db": "dcrr3f58noacr2"
}

conn = psycopg2.connect(
    f"""host={fterospostgres["host"]} dbname={fterospostgres["db"]} user={fterospostgres["user"]} password={fterospostgres["pwd"]}""")