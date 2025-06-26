import random
import locale
from datetime import datetime, timedelta
import uuid


class Jugador:
    def __init__(self, nombre_jugador: str, apellidos_jugador: str):
        self.id_jugador = ""
        self.nombre = nombre_jugador
        self.apellidos = apellidos_jugador
        self.lista_id_jugadores = []

    def __str__(self):  # Representación del objeto jugador.
        return f"{self.nombre} {self.apellidos} con Id: {self.id_jugador}"

    # Genera un id automático para cada jugador que no esté repetido.
    # Posiblemente se cambie y utilizamos la librería uuid.
    def crear_id_jugador(self):
        self.id_jugador = random.randint(1, 1_000_000)
        while self.id_jugador in self.lista_id_jugadores:
            self.id_jugador = random.randint(1, 1_000_000)
        return self.id_jugador


class Boleto:
    def __init__(self, precio: int):
        # Con el método uuid4 generamos un código único por cada instancia.
        self.codigo = str(uuid.uuid4())
        # Atributo que almacena la fecha y hora actual al crear una instancia de boleto.
        self.fecha_sorteo = ""
        self.precio = precio
        self.lista_num = []  # Almacena 6 números del boleto.

    def __str__(self):  # Representación del objeto boleto.
        return f"\33[32mBoleto generado con éxito:\33[0m \nCódigo: {self.codigo} \nFecha: {self.fecha_sorteo} \nPrecio: {self.precio}€ \nJugada: {self.lista_num}"

    def generar_boleto_manual(self):
        while True:
            try:
                num = int(input("Dime número: "))
                while num < 1 or num > 49:
                    print("Solo se permiten números entre 1 y 49.")
                    num = int(input("Dime número: "))
                if num in self.lista_num:
                    print("El número ya existe, escoge otro por favor.")
                    continue
                self.lista_num.append(num)
            except ValueError:  # Si el user escribe un carácter que no sea un número, evitamos que falle el programa y mostramos mensaje informativo.
                print("Error!!! Solo se permiten números.")
            if len(self.lista_num) == 6:
                break
        if self.lista_num:  # Si la lista contiene algo, querrá decir que existen números, por lo que añadimos la fecha y hora actuales llamando a la función.
            self.fecha_sorteo = self.generar_fecha_y_hora_actual()
            return self.lista_num

    def generar_boleto_aleatorio(self, objeto_gestor):
        self.lista_num = objeto_gestor.generar_numeros_aleatorios()
        self.fecha_sorteo = self.generar_fecha_y_hora_actual()
        return self.lista_num

    def generar_fecha_y_hora_actual(self):
        # Formatear fechas con strftime()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y %H:%M")
        return fecha_formateada


class GestorLoteria:
    def __init__(self):
        self.n_aleatorios = []
        self.premios = {}
        self.boletos_emitidos = []  # Esta lista guarda OBJETOS Boleto
        # Almacena un conjunto de tuplas (6 números ordenados por cada tupla). Esto realiza un checkeo más rápido que si fueran listas
        self.jugadas_unicas_emitidas = set()

    def generar_numeros_aleatorios(self):
        # Genera 6 números aleatorios y distintos desde el 1 al 49. Considerar añadir constantes.
        self.n_aleatorios = list(random.sample(range(1, 49), 6))
        return self.n_aleatorios

    # Muestra por pantalla el boleto y los resultados y reparte premio si lo hay.
    def comprobar_boleto(self, resultado, objeto_boleto):
        n_acertados = []
        print(f"Id: {objeto_boleto.codigo}")
        print(f"Jugada: {objeto_boleto.lista_num}")
        print(f"Resultado: {resultado}")
        for numero in objeto_boleto.lista_num:
            if numero in resultado:
                n_acertados.append(numero)
        total = len(n_acertados)
        if total > 0:
            print(f"Los números acertados son: {n_acertados}")
            if total >= 3:
                print("Premio!!! Has ganado:")
                if total == 3:
                    print(f"{self.premios[3]}€")
                elif total == 4:
                    print(f"{self.premios[4]}€")
                elif total == 5:
                    print(f"{self.premios[5]}€")
                elif total == 6:
                    print(f"{self.premios[6]}€")
        else:
            print("No se ha acertado ningún número, lo siento")

    # Asignamos los premios recibiendo los datos como parámetro y asignamos los valores a la propiedad del objeto premios.
    def asignar_premios(self, primer_premio, segundo_premio, tercer_premio, cuarto_premio):
        self.premios[6] = primer_premio
        self.premios[5] = segundo_premio
        self.premios[4] = tercer_premio
        self.premios[3] = cuarto_premio

    def agregar_boleto(self, boleto_a_agregar):
        jugada_tupla = tuple(sorted(boleto_a_agregar.lista_num))

        if jugada_tupla in self.jugadas_unicas_emitidas:
            # Si la jugada (tupla ordenada) ya está en nuestro set de jugadas únicas.
            print("\n\33[31mEL BOLETO YA EXISTE. ESCOGE OTRO!!\33[0m")
            return  # Salimos de la función.

        # Si no está repetido, lo añadimos al set de jugadas únicas.
        self.jugadas_unicas_emitidas.add(jugada_tupla)

        # Y luego añadimos el objeto Boleto completo a nuestra lista de boletos emitidos.
        self.boletos_emitidos.append(boleto_a_agregar)
        print(boleto_a_agregar)

        ####################################### MENÚ PRINCIPAL###############################################
if __name__ == "__main__":
    gestor = GestorLoteria()
    gestor.asignar_premios(2_000_000, 600_000, 3_500, 350)

    # Solicitamos los datos al jugador, creamos una instancia del objeto jugador y un id único para dicho jugador.
    nombre = input("Dime tu nombre: ")
    apellidos = input("Dime tus apellidos: ")
    jugador = Jugador(nombre, apellidos)
    jugador.crear_id_jugador()
    print(f"\33[32mHola {jugador}\33[0m")

    # Bucle del Menú que gestiona el usuario por pantalla.
    while True:
        print("\n---- MENÚ DE LOTERÍA ----")
        print("1. Comprar boleto (Manual)")
        print("2. Comprar boleto (Automático)")
        print("3. Realizar sorteo")
        print("4. Comprobar mis boletos")
        print("5. Visualizar mis boletos")
        print("6. Salir")

        opcion = input("Escoge una opción: ")

        if opcion == "1":
            boleto = Boleto(2)
            boleto.generar_boleto_manual()
            gestor.agregar_boleto(boleto)

        elif opcion == "2":
            boleto = Boleto(2)
            boleto.generar_boleto_aleatorio(gestor)
            gestor.agregar_boleto(boleto)
        elif opcion == "3":
            combinacion_ganadora = gestor.generar_numeros_aleatorios()
            print(
                f"La combinación ganadora es: \33[32m{combinacion_ganadora}\33[0m")

        elif opcion == "4":
            try:
                for boleto in gestor.boletos_emitidos:
                    gestor.comprobar_boleto(combinacion_ganadora, boleto)
            except NameError:
                print("Todavía no ha salido el sorteo de hoy")

        elif opcion == "5":
            print("\n\33[31mTus boletos actuales son:\33[0m ")
            for boleto in gestor.boletos_emitidos:
                print(
                    f"Código: {boleto.codigo} Fecha: {boleto.fecha_sorteo} Precio: {boleto.precio} Número: {boleto.lista_num}")

        elif opcion == "6":
            print("\nGracias por jugar. Hasta pronto ;)")
            break

        else:
            print("Tienes que escribir un número válido")
