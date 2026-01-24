from flask import Flask, render_template, request, jsonify, session
from twilio.twiml.messaging_response import MessagingResponse
from calendar_service import crear_cita
import difflib
import json
import re
import datetime
import random
import requests
import uuid

app = Flask(__name__)
app.secret_key = 'super_secret_key_snel_unified'

# ========================
# CONFIG & CONSTANTS
# ========================
APPSHEET_APP_ID = "1b8d545e-28de-4ece-ab2e-44bfc7207211"
APPSHEET_KEY = "V2-NJZ9H-NhnsB-QC56V-uqYSl-idnwm-J6pbN-mESqf-C5Oc9"

COVERED_SECTORS = [
    "Epoca", "Operadores", "Chontacruz", "Colinas Lojanas", "Daniel Alvarez", "Zarzas I", "Zarzas II",
    "Sol de los Andes", "Esteban Godoy", "Ciudad Alegria", "Argelia", "Los Cipres", "San Isidro",
    "El Electricista", "Union Lojana", "Los Geranios", "La Pradera", "Pucara", "Los Cocos",
    "Tebaida", "San Pedro"
]

PRODUCT_CATALOG = {
    # Cameras
    "cam_ext_wifi": {"desc": "Cámara IP Exterior Wi-Fi Full HD con Visión Nocturna", "val": 45, "cat": "Cámaras"},
    "cam_ext_cable": {"desc": "Cámara Hikvision Turbo HD 4.0 Exterior (Cableada)", "val": 35, "cat": "Cámaras"},
    "cam_int_wifi": {"desc": "Cámara Robótica Interior 360° Wi-Fi", "val": 30, "cat": "Cámaras"},
    "cam_int_cable": {"desc": "Cámara Domo Interior HD 1080p", "val": 28, "cat": "Cámaras"},
    
    # Videoporteros
    "video_casa": {"desc": "Videoportero Analógico Kit Hogar", "val": 120, "cat": "Videoporteros"},
    "video_negocio": {"desc": "Videoportero IP Multi-usuario para Edificios", "val": 250, "cat": "Videoporteros"},
    
    # Alarmas
    "alarma_casa": {"desc": "Kit Alarma Inalámbrica Básica (Sensor Puerta + Movimiento)", "val": 85, "cat": "Alarmas"},
    "alarma_negocio": {"desc": "Central de Alarma Híbrida 8 Zonas Profesional", "val": 180, "cat": "Alarmas"},
    
    # Cerraduras
    "cerradura_casa": {"desc": "Cerradura Inteligente Huella/Clave para Puerta Principal", "val": 150, "cat": "Cerraduras"},
    "cerradura_negocio": {"desc": "Control de Acceso Biométrico para Personal", "val": 200, "cat": "Cerraduras"},
    
    # Energia
    "ups_casa": {"desc": "UPS 500VA para Router y PC Básico", "val": 45, "cat": "Respaldo Energía"},
    "ups_negocio": {"desc": "UPS Online 1KVA Doble Conversión", "val": 300, "cat": "Respaldo Energía"},
}

def normalize(text):
    if not text: return ""
    text = re.sub(r'[^\w\s]', '', text) 
    replacements = (
        ("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
        ("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U")
    )
    for a, b in replacements:
        text = text.replace(a, b)
    return text.lower().strip()

NORMALIZED_SECTORS = {normalize(s): s for s in COVERED_SECTORS}

# Memory for WhatsApp users
whatsapp_users = {}

# ========================
# APPSHEET HELPERS
# ========================
def generar_id(prefijo):
    # Generates ID like INT-ABCD1234
    return f"{prefijo}-{uuid.uuid4().hex[:8].upper()}"

def fecha_actual():
    return datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
    

def enviar_a_appsheet(nombre_tabla, fila):
    url = f"https://api.appsheet.com/api/v2/apps/{APPSHEET_APP_ID}/tables/{nombre_tabla}/Action"

    payload = {
        "Action": "Add",
        "Properties": {
            "Locale": "es-EC"
        },
        "Rows": [fila]
    }

    headers = {
        "ApplicationAccessKey": APPSHEET_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Log for debugging
        print("===================================")
        print("Tabla:", nombre_tabla)
        print("Status:", response.status_code)
        print("Respuesta:", response.text)
        print("===================================")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error CRITICO enviando a AppSheet: {e}")
        return False

# ========================
# LOGIC CORE
# ========================

def get_menu_text():
    return (
        "¡Hola! 👋 Gracias por comunicarte con SNEL.\n"
        "Somos especialistas en servicios de internet y cámaras de seguridad residencial.\n\n"
        "¿Qué deseas hacer hoy?\n\n"
        "1️⃣ Planes de Internet\n"
        "2️⃣ Productos de Seguridad SNEL\n"
        "3️⃣ Agendar Cita\n\n"
        "👉 Responde SOLO con el número de la opción.\n"
        "📝 En cualquier momento puedes escribir 'Menu' para volver al inicio."
    )

def check_global_commands(norm_input, state):
    global_commands = ['menu', 'inicio', 'volver', 'empezar', 'cancelar']
    if any(cmd == norm_input or cmd in norm_input.split() for cmd in global_commands):
        return True
    return False

def check_confirmation(norm_input):
    valid_confirms = ['1', 'si', 'sí', 'ok', 'dale', 'confirmo', 'de acuerdo', 'confirmar']
    for v in valid_confirms:
        if v in norm_input: 
            return True
    return False

def process_message(user_input, state, phone_number=None):
    norm_input = normalize(user_input)
    
    if phone_number and 'phone' not in state:
        state['phone'] = phone_number
    
    if check_global_commands(norm_input, state):
        return get_menu_text(), {'step': 'menu_start', 'phone': state.get('phone')}

    if not state or 'step' not in state:
        state = {'step': 'menu_start', 'phone': state.get('phone')}
        return get_menu_text(), state

    step = state['step']
    reply = ""

    # ====================================================
    # MENÚ PRINCIPAL
    # ====================================================
    if step == 'menu_start':
        if '1' in norm_input or 'internet' in norm_input or 'planes' in norm_input:
            state['step'] = 'cov_ask_sector'
            reply = "Hola, puedo ayudarte a verificar tu cobertura. ¿En qué sector te encuentras?"
        elif '2' in norm_input or 'producto' in norm_input or 'seguridad' in norm_input:
            state['step'] = 'prod_ask_type'
            reply = ("¡Hola! 😊 Soy tu asistente de seguridad.\n"
                     "¿Qué tipo de producto buscas?\n\n"
                     "1️⃣ Cámaras\n"
                     "2️⃣ Videoporteros\n"
                     "3️⃣ Alarmas\n"
             "4️⃣ Cerraduras Inteligentes\n"
             "5️⃣ Respaldo de Energía (UPS)")

        elif '3' in norm_input or 'agendar' in norm_input or 'cita' in norm_input:
            state['step'] = 'cal_ask_date'
            reply = "📅 Claro, agendemos una cita.\n¿Para qué fecha deseas? (Formato: YYYY-MM-DD, ej: 2026-01-20)"
        else:
            reply = get_menu_text() + "\n\n⚠️ Por favor, selecciona 1, 2 o 3."
        return reply, state

    # ====================================================
    # FLUJO 1: INTERNET (COBERTURA)
    # ====================================================
    if step.startswith('cov_'):
        return process_coverage_flow(norm_input, user_input, state)

    # ====================================================
    # FLUJO 2: PRODUCTOS
    # ====================================================
    if step.startswith('prod_'):
        return process_products_flow(norm_input, user_input, state)

    # ====================================================
    # FLUJO 3: CALENDARIO (CITAS)
    # ====================================================
    if step.startswith('cal_'):
        return process_calendar_flow(norm_input, user_input, state)

    return get_menu_text(), {'step': 'menu_start'}


def process_coverage_flow(norm_input, user_input, state):
    step = state['step']
    
    if step == 'cov_ask_sector':
        found_sector = None
        sorted_keys = sorted(NORMALIZED_SECTORS.keys(), key=len, reverse=True)
        for k in sorted_keys:
            if k in norm_input:
                found_sector = NORMALIZED_SECTORS[k]
                break
        
        if found_sector:
            state['sector'] = found_sector
            state['step'] = 'cov_ask_usage'
            return (f"Perfecto, sí tenemos cobertura en {found_sector}.\n"
                    f"¿Para qué lo usarás?\n\n"
                    f"1️⃣ Hogar\n"
                    f"2️⃣ Gaming\n"
                    f"3️⃣ Trabajo"), state
        
        matches = difflib.get_close_matches(norm_input, NORMALIZED_SECTORS.keys(), n=1, cutoff=0.6)
        if matches:
            real_name = NORMALIZED_SECTORS[matches[0]]
            state['temp_sector'] = real_name
            state['step'] = 'cov_confirm_fuzzy'
            return (f"¿Te refieres al sector {real_name}?\n\n"
                    f"1️⃣ Sí, confirmar\n"
                    f"2️⃣ No, cancelar"), state
        
        return (f"Lo siento, no identifiqué el sector '{user_input}' o no tenemos cobertura.\n"
                f"Prueba escribiendo solo el nombre (ej: 'Epoca').\n"
                f"O escribe 'Menú' para salir."), state

    if step == 'cov_confirm_fuzzy':
        if check_confirmation(norm_input):
            real_name = state.pop('temp_sector')
            state['sector'] = real_name
            state['step'] = 'cov_ask_usage'
            return (f"Perfecto, sí tenemos cobertura en {real_name}.\n"
                    f"¿Para qué lo usarás?\n\n"
                    f"1️⃣ Hogar\n"
                    f"2️⃣ Gaming\n"
                    f"3️⃣ Trabajo"), state
        else:
            state = {'step': 'menu_start'}
            return get_menu_text(), state

    if step == 'cov_ask_usage':
        usage = None
        if '1' in norm_input or 'hogar' in norm_input or 'casa' in norm_input:
            usage = 'Hogar'
        elif '2' in norm_input or 'gaming' in norm_input or 'jugar' in norm_input:
            usage = 'Gaming'
        elif '3' in norm_input or 'trabajo' in norm_input or 'oficina' in norm_input:
            usage = 'Trabajo'

        if usage:
            state['usage'] = usage
            state['step'] = 'cov_ask_persons'
            return "Entendido. ¿Cuántas personas usarían el internet? (Escribe el número)", state
        else:
            return "⚠️ Por favor selecciona una opción válida (1, 2 o 3).", state

    if step == 'cov_ask_persons':
        nums = re.findall(r'\d+', user_input)
        if nums:
            p = int(nums[0])
            state['persons'] = p
            u = state['usage'].lower()
            plan = "Hogar 50 Mbps"
            desc_expl = ""
            
            if "hogar" in u:
                plan = "Hogar 50 Mbps" if p <= 2 else "Hogar 100 Mbps" if p <= 4 else "Hogar 200 Mbps"
                desc_expl = "✔ Ideal para streaming y redes sociales"
            elif "gaming" in u:
                plan = "Gaming 150 Mbps" if p <= 2 else "Gaming 300 Mbps" if p <= 4 else "Gaming PRO 500 Mbps"
                desc_expl = "✔ Latencia ultra baja para jugar online"
            elif "trabajo" in u:
                plan = "Trabajo 100 Mbps" if p <= 2 else "Trabajo 200 Mbps" if p <= 4 else "Empresa 300 Mbps"
                desc_expl = "✔ Alta estabilidad y velocidad simétrica"

            state['plan'] = plan
            state['plan_expl'] = desc_expl
            state['step'] = 'cov_confirm_final'
            return (f"Perfecto, aquí tienes el resumen:\n"
                    f"📍 Sector: {state['sector']}\n"
                    f"🏠 Uso: {state['usage']}\n"
                    f"👥 Personas: {p}\n"
                    f"🚀 Plan recomendado: {plan}\n"
                    f"{desc_expl}\n\n"
                    f"1️⃣ Confirmar consulta\n"
                    f"2️⃣ Cancelar"), state
        else:
            return "Por favor, escribe un número válido de personas.", state

    if step == 'cov_confirm_final':
        if check_confirmation(norm_input):
            # GENERATE FINAL JSON DYNAMICALLY
            uid = generar_id("INT")
            ts = fecha_actual()
            phone = state.get('phone', 'WEB') 
            
            Solicitud_Internet = {
                "ID": uid,
                "Fecha": ts,
                "Telefono": phone,
                "Sector": state['sector'],
                "TipoInternet": state['usage'],
                "Personas": state['persons'],
                "PlanRecomendado": state['plan']
            }
            
            # SEND TO APPSHEET: Solicitudes_Internet
            enviar_a_appsheet("Solicitudes_Internet", Solicitud_Internet)
            
            state = {'step': 'menu_start', 'phone': phone}
            return (f"✅ Tu solicitud fue registrada correctamente.\n"
                    f"📞 Un asesor de SNEL se contactará contigo al {phone}.\n\n" + get_menu_text()), state
        else:
            state = {'step': 'menu_start'}
            return "Operación cancelada. Volviendo al inicio...", state

    return "Error en flujo internet.", state


def process_products_flow(norm_input, user_input, state):
    step = state['step']

    if step == 'prod_ask_type':
        product_type = ""
        if '1' in norm_input or 'camara' in norm_input: product_type = "camara"
        elif '2' in norm_input or 'video' in norm_input: product_type = "videoportero"
        elif '3' in norm_input or 'alarma' in norm_input: product_type = "alarma"
        elif '4' in norm_input or 'cerradura' in norm_input: product_type = "cerradura"
        elif '5' in norm_input or 'respaldo' in norm_input or 'energia' in norm_input: product_type = "energia"
        
        if not product_type:
             return ("⚠️ Opción no válida.\n\n"
                     "1️⃣ Cámaras\n"
                     "2️⃣ Videoporteros\n"
                     "3️⃣ Alarmas\n"
                     "4️⃣ Cerraduras Inteligentes\n"
                     "5️⃣ Respaldo de Energía"), state
        
        state['prod_type'] = product_type
        
        if product_type == 'camara':
            state['step'] = 'prod_cam_place'
            return ("¿La cámara será para uso interior o exterior?\n\n"
                    "1️⃣ Interior\n"
                    "2️⃣ Exterior"), state
        else:
            state['step'] = 'prod_other_place'
            return "Por favor, escribe en qué ciudad o sector se instalará:", state

    if step == 'prod_cam_place':
        if '1' in norm_input or 'interior' in norm_input: state['cam_place'] = 'interior'
        elif '2' in norm_input or 'exterior' in norm_input: state['cam_place'] = 'exterior'
        else: return "⚠️ Por favor responde:\n1️⃣ Interior\n2️⃣ Exterior", state
        
        state['step'] = 'prod_cam_conn'
        return ("¿Qué tipo de conexión prefieres?\n\n"
                "1️⃣ Inalámbrica (Wi-Fi)\n"
                "2️⃣ Cableada (Más estable)"), state

    if step == 'prod_cam_conn':
        if '1' in norm_input or 'wifi' in norm_input: conn = 'wifi'
        elif '2' in norm_input or 'cable' in norm_input: conn = 'cable'
        else: return "⚠️ Por favor responde:\n1️⃣ Wi-Fi\n2️⃣ Cable", state

        place = state['cam_place']
        
        key = f"cam_{place}_{conn}"
        if place=='interior' and conn=='cable': key = 'cam_int_cable'
        elif place=='interior' and conn=='wifi': key = 'cam_int_wifi'
        elif place=='exterior' and conn=='cable': key = 'cam_ext_cable'
        elif place=='exterior' and conn=='wifi': key = 'cam_ext_wifi'
        
        prod = PRODUCT_CATALOG.get(key, PRODUCT_CATALOG['cam_int_wifi'])
        state['final_prod'] = prod
        
        state['step'] = 'prod_confirm'
        return format_products_confirmation(prod, state), state

    if step == 'prod_other_place':
        state['location'] = user_input 
        state['step'] = 'prod_other_context'
        return ("¿Será para casa o negocio?\n\n"
                "1️⃣ Casa\n"
                "2️⃣ Negocio"), state

    if step == 'prod_other_context':
        context = ""
        if '1' in norm_input or 'casa' in norm_input: context = 'casa'
        elif '2' in norm_input or 'negocio' in norm_input: context = 'negocio'
        
        if not context:
             return "⚠️ Por favor responde:\n1️⃣ Casa\n2️⃣ Negocio", state

        ptype = state['prod_type'] 
        key_map = {
            'videoportero': f"video_{context}",
            'alarma': f"alarma_{context}",
            'cerradura': f"cerradura_{context}",
            'energia': f"ups_{context}"
        }
        
        key = key_map.get(ptype, f"video_{context}")
        prod = PRODUCT_CATALOG.get(key, PRODUCT_CATALOG['video_casa'])
        state['final_prod'] = prod
        
        state['step'] = 'prod_confirm'
        return format_products_confirmation(prod, state), state

    if step == 'prod_confirm':
        if check_confirmation(norm_input):
            p = state['final_prod']
            uid = generar_id("PROD")
            ts = fecha_actual()
            phone = state.get('phone', 'WEB')

            Solicitud_Producto = {
                "ID": uid,
                "Fecha": ts,
                "Telefono": phone,
                "Categoria": p['cat'],
                "Descripcion": p['desc'],
                "Valor": p['val'],
                "Proveedor": "SNEL"
            }
            
            # SEND TO APPSHEET: Solicitudes_Productos
            enviar_a_appsheet("Solicitudes_Productos", Solicitud_Producto)
            
            state = {'step': 'menu_start', 'phone': phone}
            return (f"✅ Tu solicitud fue registrada correctamente.\n"
                    f"📞 Un asesor de SNEL se contactará contigo.\n\n" + get_menu_text()), state
        else:
            state = {'step': 'menu_start'}
            return "Operación cancelada. Volviendo al inicio...", state

    return "Error en flujo productos.", state

def process_calendar_flow(norm_input, user_input, state):
    step = state['step']

    if step == 'cal_ask_date':
        # Simple validation could go here, for now just accept whatever or check format
        state['cal_date'] = user_input.strip()
        state['step'] = 'cal_ask_time'
        return "⏰ ¿A qué hora? (Formato: HH:MM, ej: 15:00)", state

    if step == 'cal_ask_time':
        state['cal_time'] = user_input.strip()
        
        # Tentative confirmation
        d = state['cal_date']
        t = state['cal_time']
        state['step'] = 'cal_confirm'
        return (f"🗓️ Confirmas la cita:\n"
                f"📅 Fecha: {d}\n"
                f"⏰ Hora: {t}\n\n"
                f"1️⃣ Sí, agendar\n"
                f"2️⃣ Cancelar"), state

    if step == 'cal_confirm':
        if check_confirmation(norm_input):
            try:
                d = state['cal_date']
                t = state['cal_time']
                phone = state.get('phone', 'Desconocido')
                
                link = crear_cita(f"Cita SNEL - {phone}", f"Cliente: {phone}", d, t)
                
                # Manejo de choque de horarios (Nuevo)
                if link and link.startswith("⛔"):
                     return link, state

                state = {'step': 'menu_start', 'phone': phone}
                return (f"✅ Tu cita fue agendada con éxito.\n"
                        f"🔗 Link del evento: {link}\n\n" + get_menu_text()), state
            except Exception as e:
                print(f"Error calendar: {e}")
                return "❌ Hubo un error reservando la cita (Revisa formato de fecha YYYY-MM-DD y hora HH:MM). Intenta de nuevo.", state
        else:
            state = {'step': 'menu_start'}
            return "Operación cancelada. Volviendo al inicio...", state

    return "Error en flujo calendario.", state

def format_products_confirmation(prod, state):
    expl_map = {
        "Cámaras": "✔ Monitoreo 24/7 desde tu celular\n✔ Visión nocturna",
        "Videoporteros": "✔ Mira quién toca tu puerta\n✔ Apertura remota",
        "Alarmas": "✔ Alerta inmediata de intrusos\n✔ Sirena potente",
        "Cerraduras": "✔ Olvídate de las llaves\n✔ Acceso con huella",
        "Respaldo Energía": "✔ Protege tus equipos\n✔ Mantén internet activo"
    }
    cat = prod.get('cat', 'General')
    expl = expl_map.get(cat, "✔ Calidad garantizada SNEL")
    val = prod['val']
    
    return (f"Te recomiendo: {prod['desc']}\n"
            f"{expl}\n\n"
            f"💰 Valor: ${val}\n"
            f"📋 Categoría: {cat}\n\n"
            f"1️⃣ Confirmar Registro\n"
            f"2️⃣ Cancelar")

# ========================
# FLASK ROUTES
# ========================

@app.route('/')
def index():
    session.clear() 
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Detect Source: Web vs WhatsApp (Twilio)
    # Twilio sends 'From' in form data
    # Web sends 'message' in form data (we just changed script.js to send form data)
    
    sender_phone = None
    user_input = ""
    is_whatsapp = False
    
    # 1. Check for Twilio/WhatsApp
    if 'From' in request.form:
        sender_phone = request.form.get('From', '').replace('whatsapp:', '')
        user_input = request.form.get('Body', '').strip()
        is_whatsapp = True
    
    # 2. Check for Web Client
    elif 'message' in request.form:
        user_input = request.form.get('message', '').strip()
        sender_phone = session.get('phone', 'WEB') # Use session if available
        # Web special init
        if user_input == "MENU_INIT":
            session.clear()
            session['step'] = 'menu_start'
            session['phone'] = 'WEB'
            return jsonify({'reply': get_menu_text()})
    
    else:
        # Fallback or error
        return "Unsupported Media Type", 415

    # --- CORE LOGIC ---
    # Load state
    state = {}
    if is_whatsapp:
        state = whatsapp_users.get(sender_phone, {'step': 'menu_start'})
    else:
        state = dict(session)
        state.setdefault('step', 'menu_start')

    # Process Message
    norm = normalize(user_input)
    # If starting fresh or global command (except for 'menu' which is handled in process_message too, but we catch generic starts here for whatsapp)
    if is_whatsapp and (not user_input or any(w in norm for w in ['hola', 'menu', 'inicio', 'join'])):
        if not user_state_exists(sender_phone):
            state = {'step': 'menu_start'}
            new_state = state
            response_text = get_menu_text()
        else:
            response_text, new_state = process_message(user_input, state, phone_number=sender_phone)
    else:
        response_text, new_state = process_message(user_input, state, phone_number=sender_phone)
    
    # Save State
    if is_whatsapp:
        whatsapp_users[sender_phone] = new_state
    else:
        session.clear()
        for k, v in new_state.items():
            session[k] = v
            
    # --- RESPONSE ---
    if is_whatsapp:
        resp = MessagingResponse()
        resp.message(response_text)
        return str(resp)
    else:
        return jsonify({'reply': response_text})

def user_state_exists(phone):
    return phone in whatsapp_users

if __name__ == '__main__':
    print("Asistente SNEL Professional (AppSheet Integrated) Iniciado...")
    app.run(debug=True, port=5000)
