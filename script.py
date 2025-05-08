import psycopg2
import time

# Configura tus datos de conexión
conn = psycopg2.connect(
    dbname="tarea_bdd",
    user="postgres",
    password="postgres",  # Cambia si tienes otro
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Cargar los RUTs
with open("50mil") as f:
    ruts = [line.strip() for line in f if line.strip()]

# --- Consulta individual ---
print("🔍 Consulta individual:")
rut_individual = ruts[0]

cur.execute("EXPLAIN ANALYZE SELECT nombre, direccion FROM personas2 WHERE rut = %s", (rut_individual,))
plan = cur.fetchall()
print("\n".join([row[0] for row in plan]))

start = time.time()
cur.execute("SELECT nombre, direccion FROM personas2 WHERE rut = %s", (rut_individual,))
print("Resultado:", cur.fetchone())
print("⏱️ Tiempo:", round(time.time() - start, 4), "segundos\n")

# --- Consulta masiva ---
print("🔍 Consulta masiva:")

start = time.time()
cur.execute("""
    EXPLAIN ANALYZE SELECT nombre, direccion
    FROM personas2
    WHERE rut = ANY(%s)
""", (ruts,))
plan = cur.fetchall()
plan_txt = "\n".join([row[0] for row in plan])
print(plan_txt)

# Consulta real
start_query = time.time()
cur.execute("""
    SELECT rut, nombre, direccion
    FROM personas2
    WHERE rut = ANY(%s)
""", (ruts,))
resultados = cur.fetchall()
tiempo_total = round(time.time() - start_query, 4)
print(f"✅ Se recuperaron {len(resultados)} filas en {tiempo_total} segundos.")

# Guardar resultados
with open("resultados_50mil.txt", "w") as f:
    for row in resultados:
        f.write(f"{row[0]}|{row[1]}|{row[2]}\n")

# Guardar explain
with open("explain_masiva.txt", "w") as f:
    f.write(plan_txt)

cur.close()
conn.close()
