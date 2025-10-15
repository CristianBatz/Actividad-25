import sqlite3

DB_NAME = "estudiantes.db"

class Estudiante:
    def __init__(self, nombre, carrera, promedio):
        self.nombre = nombre
        self.carrera = carrera
        self.promedio = promedio

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                carrera TEXT NOT NULL,
                promedio REAL
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO estudiantes (nombre, carrera, promedio) VALUES (?, ?, ?)",
                (self.nombre, self.carrera, self.promedio)
            )
        print(f"Estudiante '{self.nombre}' guardado con éxito.")

    @staticmethod
    def listar():
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT * FROM estudiantes")
            filas = cur.fetchall()
            if not filas:
                print("No hay estudiantes registrados.")
                return
            print("\n--- LISTADO DE ESTUDIANTES ---")
            for f in filas:
                print(f"ID: {f['id_estudiante']} | Nombre: {f['nombre']} | Carrera: {f['carrera']} | Promedio: {f['promedio']}")

    @staticmethod
    def modificar():
        ide = input("Ingrese ID del estudiante a modificar: ")
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT * FROM estudiantes WHERE id_estudiante = ?", (ide,))
            fila = cur.fetchone()
            if not fila:
                print("No se encontró el estudiante.")
                return
            nombre = input(f"Nuevo nombre [{fila['nombre']}]: ") or fila['nombre']
            carrera = input(f"Nueva carrera [{fila['carrera']}]: ") or fila['carrera']
            promedio = input(f"Nuevo promedio [{fila['promedio']}]: ") or fila['promedio']
            conn.execute("UPDATE estudiantes SET nombre=?, carrera=?, promedio=? WHERE id_estudiante=?",
                         (nombre, carrera, promedio, ide))
        print("Estudiante actualizado con éxito.")

    @staticmethod
    def eliminar():
        ide = input("Ingrese ID del estudiante a eliminar: ")
        with Estudiante._conn() as conn:
            cur = conn.execute("DELETE FROM estudiantes WHERE id_estudiante = ?", (ide,))
            if cur.rowcount == 0:
                print("No se encontró el estudiante.")
            else:
                print("Estudiante eliminado con éxito.")

    @staticmethod
    def promedio_general():
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT AVG(promedio) AS prom FROM estudiantes")
            prom = cur.fetchone()["prom"]
            if prom:
                print(f"\nPromedio general: {prom:.2f}")
            else:
                print("No hay datos para calcular el promedio.")

class Curso:
    def __init__(self, nombre, punteo):
        self.nombre = nombre
        self.punteo = punteo

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                punteo INTEGER NOT NULL
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO cursos (nombre, punteo) VALUES (?, ?)",
                (self.nombre, self.punteo)
            )
        print(f"Curso '{self.nombre}' guardado con éxito.")

    @staticmethod
    def listar():
        with Curso._conn() as conn:
            cur = conn.execute("SELECT * FROM cursos")
            filas = cur.fetchall()
            if not filas:
                print("No hay cursos registrados.")
                return
            print("\n--- LISTADO DE CURSOS ---")
            for f in filas:
                print(f"ID: {f['id_curso']} | Nombre: {f['nombre']} | Créditos: {f['creditos']}")

    @staticmethod
    def buscar():
        ide = input("Ingrese ID del curso a buscar: ")
        with Curso._conn() as conn:
            cur = conn.execute("SELECT * FROM cursos WHERE id_curso = ?", (ide,))
            fila = cur.fetchone()
            if not fila:
                print("No se encontró el curso.")
                return
            print("\n--- Informacion del curso ---")
            print(f"ID: {fila['id_docente']} | Nombre: {fila['nombre']} | Especialidad: {fila['especialidad']}")

class Docente:
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS docentes (
                id_docente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especialidad TEXT NOT NULL
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO docentes (nombre, especialidad) VALUES (?, ?)",
                (self.nombre, self.especialidad)
            )
        print(f"Docente '{self.nombre}' guardado con éxito.")

    @staticmethod
    def listar():
        with Docente._conn() as conn:
            cur = conn.execute("SELECT * FROM docentes")
            filas = cur.fetchall()
            if not filas:
                print("No hay docentes registrados.")
                return
            print("\n--- LISTADO DE DOCENTES ---")
            for f in filas:
                print(f"ID: {f['id_docente']} | Nombre: {f['nombre']} | Especialidad: {f['especialidad']}")



# --- MENÚ PRINCIPAL ---
def menu():
    while True:
        print("\n===== MENÚ DE ESTUDIANTES =====")
        print("1. Ingresar estudiante")
        print("2. Listar estudiantes")
        print("3. Modificar estudiante")
        print("4. Eliminar estudiante")
        print("5. Promedio general")
        print("6. Ingresar curso")
        print("7. Listar cursos")
        print("8. Ingresar docente")
        print("9. Listar docente")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            carrera = input("Carrera: ")
            promedio = float(input("Promedio: "))
            e = Estudiante(nombre, carrera, promedio)
            e.guardar()
        elif opcion == "2":
            Estudiante.listar()
        elif opcion == "3":
            Estudiante.modificar()
        elif opcion == "4":
            Estudiante.eliminar()
        elif opcion == "5":
            Estudiante.promedio_general()
        elif opcion == "6":
            nombre = input("Nombre del curso: ")
            punteo = int(input("punteo: "))
            c = Curso(nombre, punteo)
            c.guardar()
        elif opcion == "7":
            Curso.listar()
        elif opcion == "8":
            nombre = input("Nombre del docente: ")
            especialidad = input("Especialidad: ")
            d = Docente(nombre, especialidad)
            d.guardar()
        elif opcion == "9":
            Docente.listar()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu()