from datetime import datetime
from modelo.clinica_gestion import *

class CLI:
    def __init__(self):
        self.clinica = Clinica()

    def mostrar_menu(self):
        while True:
            print("""
--- Menú Clínica ---
1) Agregar paciente
2) Agregar médico
3) Agendar turno
4) Agregar especialidad a médico
5) Emitir receta
6) Ver historia clínica
7) Ver todos los turnos
8) Ver todos los pacientes
9) Ver todos los médicos
0) Salir
""")
            opcion = input("Seleccione una opción: ")
            try:
                if opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.agregar_especialidad()
                elif opcion == "5":
                    self.emitir_receta()
                elif opcion == "6":
                    self.ver_historia_clinica()
                elif opcion == "7":
                    self.ver_turnos()
                elif opcion == "8":
                    self.ver_pacientes()
                elif opcion == "9":
                    self.ver_medicos()
                elif opcion == "0":
                    print("Saliendo...")
                    break
                else:
                    print("Opción inválida")
            except Exception as e:
                print(f"Error: {e}")

    def agregar_paciente(self):
        nombre = input("Nombre completo: ")
        dni = input("DNI: ")
        fecha_nac = input("Fecha de nacimiento (dd/mm/aaaa): ")
        self.clinica.agregar_paciente(Paciente(nombre, dni, fecha_nac))
        print("Paciente agregado con éxito.")

    def agregar_medico(self):
        nombre = input("Nombre completo: ")
        matricula = input("Matrícula: ")
        medico = Medico(nombre, matricula)
        self.clinica.agregar_medico(medico)
        print("Médico agregado con éxito.")

    def agregar_especialidad(self):
        matricula = input("Matrícula del médico: ")
        tipo = input("Nombre de la especialidad: ")
        dias = input("Días de atención (separados por coma): ").split(',')
        medico = self.clinica.obtener_medico_por_matricula(matricula)
        medico.agregar_especialidad(Especialidad(tipo, dias))
        print("Especialidad agregada.")

    def agendar_turno(self):
        dni = input("DNI del paciente: ")
        matricula = input("Matrícula del médico: ")
        especialidad = input("Especialidad: ")
        fecha_str = input("Fecha y hora (dd/mm/aaaa HH:MM): ")
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
        self.clinica.agendar_turno(dni, matricula, especialidad, fecha)
        print("Turno agendado.")

    def emitir_receta(self):
        dni = input("DNI del paciente: ")
        matricula = input("Matrícula del médico: ")
        medicamentos = input("Medicamentos (separados por coma): ").split(',')
        self.clinica.emitir_receta(dni, matricula, medicamentos)
        print("Receta emitida.")

    def ver_historia_clinica(self):
        dni = input("DNI del paciente: ")
        historia = self.clinica.obtener_historia_clinica_por_dni(dni)
        print(historia)

    def ver_turnos(self):
        for turno in self.clinica.obtener_turnos():
            print(turno)

    def ver_pacientes(self):
        for p in self.clinica.obtener_pacientes():
            print(p)

    def ver_medicos(self):
        for m in self.clinica.obtener_medicos():
            print(m)

if __name__ == "__main__":
    CLI().mostrar_menu()
