from config import normalize, PRODUCT_CATALOG
from services.appsheet import send_to_appsheet
from utils.messages import (
    MSG_MENU_MAIN, MSG_GLOBAL_CANCEL, MSG_PROD_MENU_TYPE, MSG_PROD_ERROR_TYPE, MSG_PROD_ASK_SECTOR,
    MSG_PROD_DOOR_TYPE, MSG_PROD_CAM_PLACE, MSG_PROD_CAM_ERROR_PLACE, MSG_PROD_CAM_CONN, MSG_PROD_CAM_ERROR_CONN,
    MSG_PROD_UPS_CONTEXT, MSG_PROD_CONTEXT, MSG_PROD_ERROR_CONTEXT, MSG_PROD_ERROR_DOOR, 
    MSG_PROD_SUCCESS, MSG_PROD_SUCCESS_UPS, format_product_confirmation
)
from utils.logger import setup_logger
import datetime

logger = setup_logger(__name__)

def _finalize_product_request(state: dict, prod: dict) -> tuple[str, dict]:
    """ 
    Helper para finalizar el flujo de productos:
    1. Construye payload
    2. Envia a AppSheet
    3. Retorna mensaje de éxito y resetea estado
    """
    phone = state.get('phone', 'WEB')
    desc = prod['desc']
    extra = state.get('adicional', '')
    final_adicional = f"{desc} - {extra}" if extra else desc
    
    payload = {
        "Fecha": datetime.datetime.utcnow().isoformat(),
        "Telefono": phone,
        "Categoria": prod['cat'],
        "Sector": state.get('sector', ''),
        "Adicional": final_adicional,
        "ReferidoPor": state.get('referral', 'Desconocido')
    }
    
    # Debug logs (mantenemos los logs originales para trazabilidad)
    print("\n====== DEBUG PAYLOAD A APPSHEET ======")
    print("PRODUCTO:", prod)
    print("ADICIONAL RAW:", extra)
    print("FINAL ADICIONAL:", final_adicional)
    print("PAYLOAD:", payload)
    print("TIPOS:", {k: type(v) for k, v in payload.items()})
    print("====================================")
    
    send_to_appsheet("Solicitudes_Productos", payload)
    
    # Reseteo de estado según requerimiento
    state = {'step': 'menu_start', 'phone': phone}
    return (MSG_PROD_SUCCESS + MSG_MENU_MAIN), state

def handle_product_type(text: str, state: dict) -> tuple[str, dict]:
    print("\n=== handle_product_type ===")
    print("INPUT:", text)
    print("STATE IN:", state)

    norm_input = normalize(text)
    print("NORMALIZED:", norm_input)

    product_type = ""
    if '1' in norm_input or 'camara' in norm_input: product_type = "camara"
    elif '2' in norm_input or 'video' in norm_input: product_type = "videoportero"
    elif '3' in norm_input or 'alarma' in norm_input: product_type = "alarma"
    elif '4' in norm_input or 'cerradura' in norm_input: product_type = "cerradura"
    elif '5' in norm_input or 'respaldo' in norm_input or 'energia' in norm_input: product_type = "energia"
    
    print("PRODUCT TYPE DETECTED:", product_type)

    if not product_type:
        print("ERROR: product_type vacío")
        return MSG_PROD_ERROR_TYPE, state
    
    state['prod_type'] = product_type
    state['step'] = 'prod_ask_sector' 

    print("STATE OUT:", state)
    return MSG_PROD_ASK_SECTOR, state

def handle_product_sector(text: str, state: dict) -> tuple[str, dict]:
    print("\n=== handle_product_sector ===")
    print("INPUT:", text)
    print("STATE IN:", state)

    state['sector'] = text
    print("SECTOR GUARDADO:", state['sector'])

    product_type = state['prod_type']
    print("PRODUCT TYPE:", product_type)
    
    if product_type == 'cerradura':
        state['step'] = 'prod_ask_additional'
        return MSG_PROD_DOOR_TYPE, state
    elif product_type == 'camara':
        state['step'] = 'prod_cam_place'
        return MSG_PROD_CAM_PLACE, state
    elif product_type == 'energia':
        state['step'] = 'prod_ask_ups_context'
        return MSG_PROD_UPS_CONTEXT, state
    else:
        state['step'] = 'prod_other_context'
        return MSG_PROD_CONTEXT, state

def handle_ups_context(text: str, state: dict) -> tuple[str, dict]:
    print("\n=== handle_ups_context ===")
    print("INPUT:", text)
    print("STATE IN:", state)

    norm_input = normalize(text)
    print("NORMALIZED:", norm_input)

    val = ""
    if '1' in norm_input or 'casa' in norm_input: val = "Casa"
    elif '2' in norm_input or 'oficina' in norm_input: val = "Oficina"
    elif '3' in norm_input or 'empresa' in norm_input: val = "Empresa"
    
    print("VAL DETECTADO:", val)

    if not val:
        print("ERROR: UPS CONTEXT inválido")
        return MSG_PROD_UPS_CONTEXT, state

    cat_key = 'ups_casa' if val == 'Casa' else 'ups_negocio'
    prod = PRODUCT_CATALOG.get(cat_key, PRODUCT_CATALOG['ups_casa'])

    print("CAT KEY:", cat_key)
    print("PRODUCTO UPS:", prod)
    
    state['adicional'] = val 
    state['final_prod'] = prod
    # Finalizar flujo directamente
    return _finalize_product_request(state, prod)

def handle_product_additional(text: str, state: dict) -> tuple[str, dict]:
    print("\n=== handle_product_additional ===")
    print("INPUT:", text)
    print("STATE IN:", state)

    norm_input = normalize(text)
    print("NORMALIZED:", norm_input)

    val = ""
    if '1' in norm_input or 'madera' in norm_input: val = "Madera"
    elif '2' in norm_input or 'metal' in norm_input: val = "Metal"
    elif '3' in norm_input or 'vidrio' in norm_input: val = "Vidrio"
    elif '4' in norm_input or 'blindada' in norm_input: val = "Blindada"
    
    print("VAL DETECTADO:", val)

    if not val:
        print("ERROR: DOOR TYPE inválido")
        return MSG_PROD_ERROR_DOOR, state
        
    state['adicional'] = val
    state['step'] = 'prod_other_context'
    print("STATE OUT:", state)
    return MSG_PROD_CONTEXT, state

def handle_cam_place(text: str, state: dict) -> tuple[str, dict]:
    print("\n=== handle_cam_place ===")
    print("INPUT:", text)
    print("STATE IN:", state)

    norm_input = normalize(text)
    print("NORMALIZED:", norm_input)

    if '1' in norm_input or 'interior' in norm_input: 
        state['cam_place'] = 'interior'
    elif '2' in norm_input or 'exterior' in norm_input: 
        state['cam_place'] = 'exterior'
    else: 
        print("ERROR: CAM PLACE inválido")
        return MSG_PROD_CAM_ERROR_PLACE, state
    
    print("CAM PLACE:", state['cam_place'])

    state['step'] = 'prod_cam_conn'
    return MSG_PROD_CAM_CONN, state

def handle_cam_conn(text: str, state: dict) -> tuple[str, dict]:
    print("\n=== handle_cam_conn ===")
    print("INPUT:", text)
    print("STATE IN:", state)

    norm_input = normalize(text)
    print("NORMALIZED:", norm_input)

    if '1' in norm_input or 'wifi' in norm_input: conn = 'wifi'
    elif '2' in norm_input or 'cable' in norm_input: conn = 'cable'
    else: 
        print("ERROR: CAM CONN inválido")
        return MSG_PROD_CAM_ERROR_CONN, state

    place = state['cam_place']
    
    key = f"cam_{place}_{conn}"
    if place=='interior' and conn=='cable': key = 'cam_int_cable'
    elif place=='interior' and conn=='wifi': key = 'cam_int_wifi'
    elif place=='exterior' and conn=='cable': key = 'cam_ext_cable'
    elif place=='exterior' and conn=='wifi': key = 'cam_ext_wifi'
    
    prod = PRODUCT_CATALOG.get(key, PRODUCT_CATALOG['cam_int_wifi'])

    print("CAM KEY:", key)
    print("PRODUCTO CAMARA:", prod)

    state['final_prod'] = prod
    # Finalizar flujo directamente
    return _finalize_product_request(state, prod)

def handle_other_context(text: str, state: dict) -> tuple[str, dict]:
    print("\n=== handle_other_context ===")
    print("INPUT:", text)
    print("STATE IN:", state)

    norm_input = normalize(text)
    print("NORMALIZED:", norm_input)

    context = ""
    if '1' in norm_input or 'casa' in norm_input: context = 'casa'
    elif '2' in norm_input or 'departamento' in norm_input: context = 'casa'
    elif '3' in norm_input or 'edificio' in norm_input: context = 'negocio'
    elif 'negocio' in norm_input: context = 'negocio'
    
    print("CONTEXT:", context)

    if not context:
         print("ERROR: CONTEXT inválido")
         return MSG_PROD_ERROR_CONTEXT, state

    ptype = state['prod_type'] 
    key_map = {
        'videoportero': f"video_{context}",
        'alarma': f"alarma_{context}",
        'cerradura': f"cerradura_{context}",
        'energia': f"ups_{context}"
    }
    
    key = key_map.get(ptype, f"video_{context}")
    prod = PRODUCT_CATALOG.get(key, PRODUCT_CATALOG.get('video_casa')) 
    if not prod: prod = PRODUCT_CATALOG['video_casa'] 

    print("KEY FINAL:", key)
    print("PRODUCTO FINAL:", prod)

    state['final_prod'] = prod
    # Finalizar flujo directamente
    return _finalize_product_request(state, prod)

