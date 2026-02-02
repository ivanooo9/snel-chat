# General
MSG_MENU_MAIN = (
    "Hola. Sistema de Gestión SNEL.\n"
    "Selecciona una opción para continuar:\n\n"
    "1️⃣ Registro de Solicitud Internet\n"
    "2️⃣ Registro de Solicitud Seguridad\n"
    "3️⃣ Agendar Cita\n"
)

MSG_MENU_ERROR_SELECTION = "⚠️ Opción no válida. Responde 1, 2 o 3."

MSG_GLOBAL_CANCEL = "Operación cancelada.\n\n"
MSG_GLOBAL_ERROR = "⚠️ Error del sistema. Escribe 'Menu' para reiniciar."
MSG_FALLBACK_DEFAULT = "Sistema SNEL. Escribe 'Menu' para iniciar."

# Referral
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

# Internet Coverage
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

# Products
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

# Product Explanations REMOVED (No recommendation policy)

def format_product_confirmation(prod):
    # Minimalist Confirmation
    desc = prod['desc']
    cat = prod.get('cat', 'General')
    
    return (f"Confirmar registro de solicitud:\n\n"
            f"📋 Item: {desc}\n"
            f"📂 Categoría: {cat}\n\n"
            f"1️⃣ Confirmar\n"
            f"2️⃣ Cancelar")

# Calendar
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

MSG_MENU_ERROR_SELECTION = "\n\n⚠️ Por favor, selecciona 1, 2 o 3."

MSG_GLOBAL_CANCEL = "Operación cancelada. Volviendo al inicio...\n\n"
MSG_GLOBAL_ERROR = "⚠️ Ocurrió un error interno. Escribe 'Menu' para reiniciar."
MSG_FALLBACK_DEFAULT = "Hola, soy el asistente de SNEL. Escribe 'Menu' para comenzar."

# Referral
MSG_REFERRAL_QUESTION = (
    "Antes de continuar, una pregunta rápida: \n\n"
    "**¿Cómo se enteró de SNEL?**\n\n"
    "1️⃣ Redes Sociales\n"
    "2️⃣ Volantes / Flyers\n"
    "3️⃣ Google\n"
    "4️⃣ ChatGPT\n"
    "5️⃣ Pantalla Publicitaria\n"
    "6️⃣ Eventos"
)
MSG_REFERRAL_ERROR = "⚠️ Por favor selecciona una opción válida (1-6):\n\n"

# Internet Coverage
MSG_COV_ASK_SECTOR = "¿Para qué sector de la ciudad de Loja necesitas el internet?"
MSG_COV_FUZZY_CONFIRM = (
    "¿Te refieres al sector {sector}?\n\n"
    "1️⃣ Sí, confirmar\n"
    "2️⃣ No, cancelar"
)
MSG_COV_NO_COVERAGE = (
    "❌ Lo siento, no tenemos cobertura de internet en ese sector.\n\n"
    "Igual te informamos que contamos con productos de seguridad 🔐\n\n"
    "1️⃣ Ver productos de seguridad\n"
    "2️⃣ Volver al menú"
)
MSG_COV_INVALID_OPTION = (
    "❌ Opción no válida.\n\n"
    "1️⃣ Ver productos de seguridad\n"
    "2️⃣ Volver al menú"
)
MSG_COV_SUCCESS = (
    "✅ Listo! Hemos registrado tu interés para el sector {sector}.\n"
    "📞 Un asesor te contactará al {phone} en breve.\n\n"
)
MSG_COV_ERROR_APPSHEET = (
    "⚠️ Hubo un error registrando tu solicitud en el sistema.\n"
    "Por favor intenta más tarde o comunícate con soporte.\n\n"
)

# Products
MSG_PROD_MENU_TYPE = (
    "Soy tu amiga y estoy para ayudarte en tu inversión de productos de seguridad.\n"
    "¿Qué tipo de producto buscas?\n\n"
    "1️⃣ Cámaras\n"
    "2️⃣ Videoporteros\n"
    "3️⃣ Alarmas\n"
    "4️⃣ Cerraduras Inteligentes\n"
    "5️⃣ Respaldo de Energía (UPS)"
)
MSG_PROD_ERROR_TYPE = (
    "⚠️ Opción no válida.\n\n"
    "1️⃣ Cámaras\n"
    "2️⃣ Videoporteros\n"
    "3️⃣ Alarmas\n"
    "4️⃣ Cerraduras Inteligentes\n"
    "5️⃣ Respaldo de Energía"
)

MSG_PROD_ASK_SECTOR = "¿En qué sector de Loja te encuentras?"

MSG_PROD_DOOR_TYPE = (
    "¿El tipo de puerta es?\n\n"
    "1️⃣ Madera\n"
    "2️⃣ Metal\n"
    "3️⃣ Vidrio\n"
    "4️⃣ Blindada"
)

MSG_PROD_CAM_PLACE = (
    "¿La cámara será para uso interior o exterior?\n\n"
    "1️⃣ Interior\n"
    "2️⃣ Exterior"
)
MSG_PROD_CAM_ERROR_PLACE = "⚠️ Por favor responde:\n1️⃣ Interior\n2️⃣ Exterior"

MSG_PROD_CAM_CONN = (
    "¿Qué tipo de conexión prefieres?\n\n"
    "1️⃣ Inalámbrica (Wi-Fi)\n"
    "2️⃣ Cableada (Más estable)"
)
MSG_PROD_CAM_ERROR_CONN = "⚠️ Por favor responde:\n1️⃣ Wi-Fi\n2️⃣ Cable"

MSG_PROD_UPS_CONTEXT = (
    "¿Para qué tipo de lugar necesitas el UPS?\n\n"
    "1️⃣ Casa\n"
    "2️⃣ Oficina\n"
    "3️⃣ Empresa"
)

MSG_PROD_CONTEXT = (
    "Necesitas para:\n\n"
    "1️⃣ Casa Unifamiliar\n"
    "2️⃣ Departamento\n"
    "3️⃣ Edificio de Departamentos\n"
)

MSG_PROD_ERROR_CONTEXT = "⚠️ Por favor selecciona una opción válida."
MSG_PROD_ERROR_DOOR = "⚠️ Por favor selecciona el tipo de puerta (1-4)."

MSG_PROD_SUCCESS = (
    "✅ Tu solicitud fue registrada correctamente.\n"
    "📞 Un asesor de SNEL se contactará contigo.\n\n"
)
MSG_PROD_SUCCESS_UPS = (
    "✅ Listo! Hemos registrado tu interés por un UPS para {val}.\n"
    "📞 Un asesor te contactará pronto.\n\n"
)

# Product Explanations
PROD_DESC_CAM = "✔ Monitoreo 24/7 desde tu celular\n✔ Visión nocturna"
PROD_DESC_VIDEO = "✔ Mira quién toca tu puerta\n✔ Apertura remota"
PROD_DESC_ALARM = "✔ Alerta inmediata de intrusos\n✔ Sirena potente"
PROD_DESC_LOCK = "✔ Olvídate de las llaves\n✔ Acceso con huella"
PROD_DESC_UPS = "✔ Protege tus equipos\n✔ Mantén internet activo"
PROD_DESC_DEFAULT = "✔ Calidad garantizada SNEL"

def format_product_confirmation(prod):
    cat = prod.get('cat', 'General')
    expl_map = {
        "Cámaras": PROD_DESC_CAM,
        "Videoporteros": PROD_DESC_VIDEO,
        "Alarmas": PROD_DESC_ALARM,
        "Cerraduras": PROD_DESC_LOCK,
        "Respaldo Energía": PROD_DESC_UPS
    }
    expl = expl_map.get(cat, PROD_DESC_DEFAULT)
    val = prod['val']
    
    return (f"Te recomiendo: {prod['desc']}\n"
            f"{expl}\n\n"
            f"💰 Valor: ${val}\n"
            f"📋 Categoría: {cat}\n\n"
            f"1️⃣ Confirmar Registro\n"
            f"2️⃣ Cancelar")

# Calendar
MSG_CAL_ASK_DATE = "📅 Claro, agendemos una cita.\n¿Para qué fecha deseas? (Formato: YYYY-MM-DD, ej: 2026-01-20)"
MSG_CAL_ASK_TIME = "⏰ ¿A qué hora? (Formato: HH:MM, ej: 15:00)"
MSG_CAL_CONFIRM = (
    "🗓️ Confirmas la cita:\n"
    "📅 Fecha: {date}\n"
    "⏰ Hora: {time}\n\n"
    "1️⃣ Sí, agendar\n"
    "2️⃣ Cancelar"
)
MSG_CAL_SUCCESS = (
    "✅ Tu cita fue agendada con éxito.\n"
    "🔗 Link del evento: {link}\n\n"
)
MSG_CAL_ERROR_CREATE = "Error desconocido al agendar."
MSG_CAL_ERROR_COLLISION = "⛔ Ese horario ya está ocupado. Por favor elige otro."
MSG_CAL_ERROR_FORMAT = "Formato de fecha u hora incorrecto."
