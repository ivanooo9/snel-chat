from calendar_service import crear_cita
from datetime import datetime
import sys

# Fecha dinámica para evitar líos si corremos esto mañana
# Usamos un día fijo futuro para prueba
TEST_DATE = "2026-02-15" 
TEST_TIME = "10:00"

print(f"--- TEST DE CHOQUE DE HORARIOS ---")
print(f"Intentando crear cita 1 en {TEST_DATE} {TEST_TIME}...")
res1 = crear_cita("Test Cita 1", "Prueba autom", TEST_DATE, TEST_TIME)
print(f"Resultado 1: {res1}")

print(f"\nIntentando crear cita 2 (DUPLICADA) en {TEST_DATE} {TEST_TIME}...")
res2 = crear_cita("Test Cita 2", "Prueba choque", TEST_DATE, TEST_TIME)
print(f"Resultado 2 (Esperado error): {res2}")

if "⛔" in str(res2):
    print("\n✅ ÉXITO: El choque fue detectado correctamente.")
    sys.exit(0)
else:
    print("\n❌ FALLO: Se permitió crear la cita duplicada.")
    sys.exit(1)
