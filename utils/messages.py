# =========================
# General
# =========================
print("LOADING:", __file__)
print("EXPORTS:", dir())

MSG_MENU_MAIN = (
    "¡Hola! 👋 Gracias por comunicarte con SNEL.\n"
    "Somos especialistas en servicios de internet y cámaras de seguridad residencial.\n\n"
    "¿Qué deseas hacer hoy?\n\n"
    "1️⃣ Planes de Internet\n"
    "2️⃣ Productos de Seguridad SNEL\n"
    "3️⃣ Agendar Cita\n\n"
    "👉 Responde SOLO con el número de la opción.\n"
    "📝 En cualquier momento puedes escribir 'Menu' para volver al inicio."
)

MSG_MENU_ERROR_SELECTION = "⚠️ Opción no válida. Responde 1, 2 o 3."

MSG_GLOBAL_CANCEL = "Operación cancelada.\n\n"
MSG_GLOBAL_ERROR = "⚠️ Error del sistema. Escribe 'Menu' para reiniciar."
MSG_FALLBACK_DEFAULT = "Sistema SNEL. Escribe 'Menu' para iniciar."


# =========================
# Referral
# =========================

MSG_REFERRAL_QUESTION = (
    "¿Fuente de referencia?\n\n"
    "1️⃣ Redes Sociales\n"
    "2️⃣ Volantes / Flyers\n"
    "3️⃣ Google\n"
    "4️⃣ ChatGPT\n"
    "5️⃣ Pantalla Publicitaria\n"
    "6️⃣ Eventos"
)

MSG_REFERRAL_ERROR = "⚠️ Selecciona una opción válida (1-6)."


# =========================
# Internet Coverage
# =========================

MSG_COV_ASK_SECTOR = "¿Sector de residencia?"

MSG_COV_FUZZY_CONFIRM = (
    "¿Confirmas el sector {sector}?\n\n"
    "1️⃣ Sí\n"
    "2️⃣ No"
)

MSG_COV_NO_COVERAGE = (
    "❌ Sector sin cobertura.\n\n"
    "1️⃣ Ver productos de seguridad\n"
    "2️⃣ Volver al menú"
)

MSG_COV_INVALID_OPTION = (
    "❌ Opción no válida.\n\n"
    "1️⃣ Ver productos de seguridad\n"
    "2️⃣ Volver al menú"
)

MSG_COV_SUCCESS = (
    "✅ Solicitud registrada: {sector}.\n"
    "Un asesor procesará la información.\n\n"
)

MSG_COV_ERROR_APPSHEET = (
    "⚠️ Error de registro.\n"
    "Intente más tarde.\n\n"
)


# =========================
# Products
# =========================

MSG_PROD_MENU_TYPE = (
    "Selecciona el tipo de producto:\n\n"
    "1️⃣ Cámaras\n"
    "2️⃣ Videoporteros\n"
    "3️⃣ Alarmas\n"
    "4️⃣ Cerraduras Inteligentes\n"
    "5️⃣ Respaldo de Energía (UPS)"
)

MSG_PROD_ERROR_TYPE = "⚠️ Opción no válida. Selecciona del 1 al 5."

MSG_PROD_ASK_SECTOR = "¿Sector de instalación?"

MSG_PROD_DOOR_TYPE = (
    "Tipo de puerta:\n\n"
    "1️⃣ Madera\n"
    "2️⃣ Metal\n"
    "3️⃣ Vidrio\n"
    "4️⃣ Blindada"
)

MSG_PROD_CAM_PLACE = (
    "Ubicación de la cámara:\n\n"
    "1️⃣ Interior\n"
    "2️⃣ Exterior"
)

MSG_PROD_CAM_ERROR_PLACE = "⚠️ Responde: 1 (Interior) o 2 (Exterior)."

MSG_PROD_CAM_CONN = (
    "Tipo de conexión:\n\n"
    "1️⃣ Inalámbrica (Wi-Fi)\n"
    "2️⃣ Cableada"
)

MSG_PROD_CAM_ERROR_CONN = "⚠️ Responde: 1 (Wi-Fi) o 2 (Cable)."

MSG_PROD_UPS_CONTEXT = (
    "Uso del equipo:\n\n"
    "1️⃣ Casa\n"
    "2️⃣ Oficina\n"
    "3️⃣ Empresa"
)

MSG_PROD_CONTEXT = (
    "Tipo de inmueble:\n\n"
    "1️⃣ Casa Unifamiliar\n"
    "2️⃣ Departamento\n"
    "3️⃣ Edificio de Departamentos"
)

MSG_PROD_ERROR_CONTEXT = "⚠️ Selecciona una opción válida."
MSG_PROD_ERROR_DOOR = "⚠️ Selecciona una opción válida (1-4)."

MSG_PROD_SUCCESS = (
    "✅ Registro completado.\n"
    "Datos guardados en sistema.\n\n"
)

MSG_PROD_SUCCESS_UPS = (
    "✅ Registro completado (UPS: {val}).\n"
    "Datos guardados en sistema.\n\n"
)


# =========================
# Calendar
# =========================

MSG_CAL_ASK_DATE = "📅 Fecha de la cita (YYYY-MM-DD):"
MSG_CAL_ASK_TIME = "⏰ Hora (HH:MM):"

MSG_CAL_CONFIRM = (
    "Confirmar cita:\n"
    "📅 {date}\n"
    "⏰ {time}\n\n"
    "1️⃣ Confirmar\n"
    "2️⃣ Cancelar"
)

MSG_CAL_SUCCESS = (
    "✅ Cita registrada.\n"
    "Link: {link}\n\n"
)

MSG_CAL_ERROR_CREATE = "Error al registrar cita."
MSG_CAL_ERROR_COLLISION = "⛔ Horario ocupado. Elige otro."
MSG_CAL_ERROR_FORMAT = "Formato incorrecto."


# =========================
# Helpers (LO QUE FALTABA)
# =========================

def format_product_confirmation(prod: dict) -> str:
    """
    Formatea un mensaje de confirmación de producto.
    Evita errores de import en flows/products.py
    """
    return f"""
✅ Producto registrado correctamente

📦 Producto: {prod.get('desc', 'N/A')}
📂 Categoría: {prod.get('cat', 'N/A')}

📞 Un asesor de SNEL se contactará contigo.
"""