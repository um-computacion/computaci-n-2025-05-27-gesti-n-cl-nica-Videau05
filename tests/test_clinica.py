import unittest
from datetime import datetime
from modelo.clinica_gestion import (
    Clinica, Paciente, Medico, Especialidad, Receta,
    PacienteNoEncontradoException, MedicoNoDisponibleException,
    RecetaInvalidaException
)

class TestClinica(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Ana García", "111", "01/01/1990")
        self.medico = Medico("Dr. House", "MED123")
        self.especialidad = Especialidad("Clínica", ["lunes"])
        self.medico.agregar_especialidad(self.especialidad)
        self.fecha = datetime(2025, 6, 16, 10, 0)  # lunes

        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)

    def test_agregar_paciente_duplicado(self):
        with self.assertRaises(ValueError):
            self.clinica.agregar_paciente(self.paciente)

    def test_agendar_turno_correcto(self):
        self.clinica.agendar_turno("111", "MED123", "Clínica", self.fecha)
        self.assertEqual(len(self.clinica.obtener_turnos()), 1)

    def test_agendar_turno_paciente_inexistente(self):
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("999", "MED123", "Clínica", self.fecha)

    def test_agendar_turno_medico_inexistente(self):
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("111", "MED999", "Clínica", self.fecha)

    def test_emision_receta_valida(self):
        self.clinica.emitir_receta("111", "MED123", ["Paracetamol"])
        historia = self.clinica.obtener_historia_clinica_por_dni("111")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_receta_medicamento_vacio(self):
        with self.assertRaises(ValueError):
            Receta(self.paciente, self.medico, [])

    def test_receta_paciente_inexistente(self):
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("999", "MED123", ["Paracetamol"])

if __name__ == "__main__":
    unittest.main()
