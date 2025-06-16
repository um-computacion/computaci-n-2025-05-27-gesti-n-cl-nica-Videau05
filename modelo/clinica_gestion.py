# === MODELO ===
from datetime import datetime

class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        if not nombre or not dni or not fecha_nacimiento:
            raise ValueError("Todos los campos del paciente son obligatorios")
        self.__nombre = nombre
        self.__dni = dni
        self.__fecha_nacimiento = fecha_nacimiento

    def obtener_dni(self):
        return self.__dni

    def __str__(self):
        return f"{self.__nombre}, {self.__dni}, {self.__fecha_nacimiento}"


class Especialidad:
    def __init__(self, tipo: str, dias: list[str]):
        if not tipo or not dias:
            raise ValueError("Especialidad y días son obligatorios")
        self.__tipo = tipo
        self.__dias = [dia.lower() for dia in dias]

    def obtener_especialidad(self):
        return self.__tipo

    def verificar_dia(self, dia: str):
        return dia.lower() in self.__dias

    def __str__(self):
        return f"{self.__tipo} (Días: {', '.join(self.__dias)})"


class Medico:
    def __init__(self, nombre: str, matricula: str, especialidades: list[Especialidad] = None):
        if not nombre or not matricula:
            raise ValueError("Nombre y matrícula son obligatorios")
        self.__nombre = nombre
        self.__matricula = matricula
        self.__especialidades = especialidades or []

    def agregar_especialidad(self, especialidad: Especialidad):
        self.__especialidades.append(especialidad)

    def obtener_matricula(self):
        return self.__matricula

    def obtener_especialidad_para_dia(self, dia: str):
        for esp in self.__especialidades:
            if esp.verificar_dia(dia):
                return esp.obtener_especialidad()
        return None

    def __str__(self):
        especialidades_str = ", ".join(str(e) for e in self.__especialidades)
        return f"{self.__nombre}, {self.__matricula}, [{especialidades_str}]"


class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str):
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad

    def obtener_medico(self):
        return self.__medico

    def obtener_fecha_hora(self):
        return self.__fecha_hora

    def __str__(self):
        return f"Turno({self.__paciente}, {self.__medico}, {self.__fecha_hora}, {self.__especialidad})"


class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str]):
        if not medicamentos:
            raise ValueError("La receta debe contener al menos un medicamento")
        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = medicamentos
        self.__fecha = datetime.now()

    def __str__(self):
        meds = ", ".join(self.__medicamentos)
        return f"Receta({self.__paciente}, {self.__medico}, [{meds}], {self.__fecha})"


class HistoriaClinica:
    def __init__(self, paciente: Paciente):
        self.__paciente = paciente
        self.__turnos = []
        self.__recetas = []

    def agregar_turno(self, turno: Turno):
        self.__turnos.append(turno)

    def agregar_receta(self, receta: Receta):
        self.__recetas.append(receta)

    def obtener_turnos(self):
        return list(self.__turnos)

    def obtener_recetas(self):
        return list(self.__recetas)

    def __str__(self):
        turnos = '\n'.join(str(t) for t in self.__turnos)
        recetas = '\n'.join(str(r) for r in self.__recetas)
        return f"HistoriaClinica({self.__paciente},\nTurnos:\n{turnos}\nRecetas:\n{recetas})"


# Excepciones personalizadas
class PacienteNoEncontradoException(Exception): pass
class MedicoNoDisponibleException(Exception): pass
class TurnoOcupadoException(Exception): pass
class RecetaInvalidaException(Exception): pass


class Clinica:
    def __init__(self):
        self.__pacientes = {}
        self.__medicos = {}
        self.__turnos = []
        self.__historias_clinicas = {}

    def agregar_paciente(self, paciente: Paciente):
        if paciente.obtener_dni() in self.__pacientes:
            raise ValueError("Paciente ya registrado")
        self.__pacientes[paciente.obtener_dni()] = paciente
        self.__historias_clinicas[paciente.obtener_dni()] = HistoriaClinica(paciente)

    def agregar_medico(self, medico: Medico):
        if medico.obtener_matricula() in self.__medicos:
            raise ValueError("Médico ya registrado")
        self.__medicos[medico.obtener_matricula()] = medico

    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
        if dni not in self.__pacientes:
            raise PacienteNoEncontradoException()
        if matricula not in self.__medicos:
            raise MedicoNoDisponibleException()

        medico = self.__medicos[matricula]
        if any(t.obtener_medico() == medico and t.obtener_fecha_hora() == fecha_hora for t in self.__turnos):
            raise TurnoOcupadoException()

        dia = self.obtener_dia_semana_en_espanol(fecha_hora)
        if not medico.obtener_especialidad_para_dia(dia):
            raise MedicoNoDisponibleException()

        if medico.obtener_especialidad_para_dia(dia).lower() != especialidad.lower():
            raise MedicoNoDisponibleException()

        turno = Turno(self.__pacientes[dni], medico, fecha_hora, especialidad)
        self.__turnos.append(turno)
        self.__historias_clinicas[dni].agregar_turno(turno)

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        if dni not in self.__pacientes or matricula not in self.__medicos:
            raise RecetaInvalidaException()
        receta = Receta(self.__pacientes[dni], self.__medicos[matricula], medicamentos)
        self.__historias_clinicas[dni].agregar_receta(receta)

    def obtener_dia_semana_en_espanol(self, fecha: datetime):
        dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        return dias[fecha.weekday()]

    def obtener_pacientes(self):
        return list(self.__pacientes.values())

    def obtener_medicos(self):
        return list(self.__medicos.values())

    def obtener_turnos(self):
        return list(self.__turnos)

    def obtener_historia_clinica_por_dni(self, dni: str):
        if dni not in self.__historias_clinicas:
            raise PacienteNoEncontradoException()
        return self.__historias_clinicas[dni]
