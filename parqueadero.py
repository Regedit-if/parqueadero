import time
from datetime import datetime, timedelta

class Parqueadero:
    def __init__(self):
        self.vehiculos = ['v' + str(i) for i in range(1, 51)]
        self.motos = ['m' + str(i) for i in range(1, 26)]
        self.estado = [['.' for _ in range(10)] for _ in range(5)]  # 50 espacios para vehículos
        self.estado_motos = [['.' for _ in range(5)] for _ in range(5)]  # 25 espacios para motos
        self.tarifas = {'vehiculo': 2000, 'moto': 1000}  # Tarifa por hora
        self.registros = {}  # Registro de entrada y salida

    def mostrar_matriz(self):
        print("***************************************")
        for fila in self.estado:
            print('-'.join(fila))
        print("***************************************")
        for fila in self.estado_motos:
            print('-'.join(fila))
        print("***************************************")

    def alquiler(self, tipo):
        if tipo == 'vehiculo':
            espacios = self.vehiculos
            estado = self.estado
        else:
            espacios = self.motos
            estado = self.estado_motos

        for i, espacio in enumerate(espacios):
            if estado[i // 10][i % 10] == '.':
                estado[i // 10][i % 10] = 'A'
                print(f"Espacio {espacio} alquilado.")
                return
        print("No hay espacios disponibles para alquiler.")

    def registrar_entrada(self, placa, tipo):
        espacios = self.vehiculos if tipo == 'vehiculo' else self.motos
        estado = self.estado if tipo == 'vehiculo' else self.estado_motos

        # Solicitar hora de entrada
        hora_entrada_str = input("Ingrese la hora de entrada (HH:MM): ")
        try:
            hora_entrada = datetime.strptime(hora_entrada_str, "%H:%M")
            hora_actual = datetime.now()
            # Establecer la fecha actual con la hora de entrada proporcionada
            hora_entrada = hora_entrada.replace(year=hora_actual.year, month=hora_actual.month, day=hora_actual.day)

            # Verificar si la hora de entrada es futura
            if hora_entrada > hora_actual:
                print("La hora de entrada no puede ser en el futuro.")
                return
        except ValueError:
            print("Formato de hora inválido. Por favor use HH:MM.")
            return

        for i, espacio in enumerate(espacios):
            if estado[i // 10][i % 10] == '.':
                estado[i // 10][i % 10] = 'O'
                self.registros[placa] = {'tipo': tipo, 'hora_entrada': hora_entrada}
                print(f"Vehículo {placa} registrado en {espacio} a las {hora_entrada.strftime('%H:%M:%S')}.")
                return
        print("No hay espacios disponibles para registro.")

    def registrar_salida(self, placa):
        if placa in self.registros:
            tipo = self.registros[placa]['tipo']
            espacios = self.vehiculos if tipo == 'vehiculo' else self.motos
            estado = self.estado if tipo == 'vehiculo' else self.estado_motos

            for i, espacio in enumerate(espacios):
                if estado[i // 10][i % 10] == 'O':
                    estado[i // 10][i % 10] = '.'
                    
                    # Solicitar hora de salida
                    hora_salida_str = input("Ingrese la hora de salida (HH:MM): ")
                    try:
                        hora_salida = datetime.strptime(hora_salida_str, "%H:%M")
                        hora_actual = datetime.now()
                        # Establecer la fecha actual con la hora de salida proporcionada
                        hora_salida = hora_salida.replace(year=hora_actual.year, month=hora_actual.month, day=hora_actual.day)

                        # Verificar si la hora de salida es futura
                        if hora_salida > hora_actual:
                            print("La hora de salida no puede ser en el futuro.")
                            return
                    except ValueError:
                        print("Formato de hora inválido. Por favor use HH:MM.")
                        return

                    self.registros[placa]['hora_salida'] = hora_salida
                    print(f"Vehículo {placa} registrado como salido a las {hora_salida.strftime('%H:%M:%S')}.")
                    return
        print("Vehículo no encontrado.")

    def facturar(self, placa):
        if placa in self.registros:
            tipo = self.registros[placa]['tipo']
            hora_entrada = self.registros[placa]['hora_entrada']

            # Solicitar hora de salida para facturar
            hora_salida_str = input("Ingrese la hora de salida para facturar (HH:MM): ")
            try:
                hora_salida = datetime.strptime(hora_salida_str, "%H:%M")
                hora_actual = datetime.now()
                # Establecer la fecha actual con la hora de salida proporcionada
                hora_salida = hora_salida.replace(year=hora_actual.year, month=hora_actual.month, day=hora_actual.day)

                # Verificar si la hora de salida es futura
                if hora_salida > hora_actual:
                    print("La hora de salida no puede ser en el futuro.")
                    return
            except ValueError:
                print("Formato de hora inválido. Por favor use HH:MM.")
                return

            tiempo_ocupacion = hora_salida - hora_entrada
            horas = int(tiempo_ocupacion.total_seconds() / 3600) + (1 if tiempo_ocupacion.total_seconds() % 3600 > 0 else 0)
            tarifa = self.tarifas[tipo] * horas

            # Aplicar descuento si corresponde
            if horas >= 5:  # Si ocupó el 70% del tiempo de jornada (6 horas)
                tarifa *= 0.85

            print(f"Factura para {placa}: {tarifa} (Tiempo: {horas} horas).")
        else:
            print("Vehículo no encontrado.")

def main():
    parqueadero = Parqueadero()
    while True:
        print("\nMenu de Opciones:")
        print("1. Mostrar matriz del parqueadero")
        print("2. Alquiler")
        print("3. Registrar entrada")
        print("4. Registrar salida")
        print("5. Facturar")
        print("6. Salir ")

        opcion = input("Ingrese una opción: ")

        if opcion == '1':
            parqueadero.mostrar_matriz()
        elif opcion == '2':
            tipo = input("Ingrese tipo (vehiculo/moto): ")
            parqueadero.alquiler(tipo)
        elif opcion == '3':
            placa = input("Ingrese placa: ")
            tipo = input("Ingrese tipo (vehiculo/moto): ")
            parqueadero.registrar_entrada(placa, tipo)
        elif opcion == '4':
            placa = input("Ingrese placa: ")
            parqueadero.registrar_salida(placa)
        elif opcion == '5':
            placa = input("Ingrese placa: ")
            parqueadero.facturar(placa)
        elif opcion == '6':
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
