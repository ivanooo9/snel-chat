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

def handle_product_type(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    product_type = ""
    if '1' in norm_input or 'camara' in norm_input: product_type = "camara"
    elif '2' in norm_input or 'video' in norm_input: product_type = "videoportero"
    elif '3' in norm_input or 'alarma' in norm_input: product_type = "alarma"
    elif '4' in norm_input or 'cerradura' in norm_input: product_type = "cerradura"
    elif '5' in norm_input or 'respaldo' in norm_input or 'energia' in norm_input: product_type = "energia"
    
    if not product_type:
        return MSG_PROD_ERROR_TYPE, state
    
    state['prod_type'] = product_type
    state['step'] = 'prod_ask_sector' 
    return MSG_PROD_ASK_SECTOR, state

def handle_product_sector(text: str, state: dict) -> tuple[str, dict]:
    state['sector'] = text # Store original text input for sector
    product_type = state['prod_type']
    
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
    norm_input = normalize(text)
    val = ""
    if '1' in norm_input or 'casa' in norm_input: val = "Casa"
    elif '2' in norm_input or 'oficina' in norm_input: val = "Oficina"
    elif '3' in norm_input or 'empresa' in norm_input: val = "Empresa"
    
    if not val:
        return MSG_PROD_UPS_CONTEXT, state

    # Logic to map user selection to detailed product in Catalog
    # Casa -> ups_casa
    # Oficina/Empresa -> ups_negocio
    
    cat_key = 'ups_casa' if val == 'Casa' else 'ups_negocio'
    prod = PRODUCT_CATALOG.get(cat_key, PRODUCT_CATALOG['ups_casa'])
    
    # Store explicit detailed selection in 'adicional' to be appended to description later
    state['adicional'] = val 
    state['final_prod'] = prod
    state['step'] = 'prod_confirm'
    
    return format_product_confirmation(prod), state

def handle_product_additional(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    val = ""
    if '1' in norm_input or 'madera' in norm_input: val = "Madera"
    elif '2' in norm_input or 'metal' in norm_input: val = "Metal"
    elif '3' in norm_input or 'vidrio' in norm_input: val = "Vidrio"
    elif '4' in norm_input or 'blindada' in norm_input: val = "Blindada"
    
    if not val:
        return MSG_PROD_ERROR_DOOR, state
        
    state['adicional'] = val
    state['step'] = 'prod_other_context'
    return MSG_PROD_CONTEXT, state

def handle_cam_place(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    if '1' in norm_input or 'interior' in norm_input: state['cam_place'] = 'interior'
    elif '2' in norm_input or 'exterior' in norm_input: state['cam_place'] = 'exterior'
    else: return MSG_PROD_CAM_ERROR_PLACE, state
    
    state['step'] = 'prod_cam_conn'
    return MSG_PROD_CAM_CONN, state

def handle_cam_conn(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    if '1' in norm_input or 'wifi' in norm_input: conn = 'wifi'
    elif '2' in norm_input or 'cable' in norm_input: conn = 'cable'
    else: return MSG_PROD_CAM_ERROR_CONN, state

    place = state['cam_place']
    
    key = f"cam_{place}_{conn}"
    if place=='interior' and conn=='cable': key = 'cam_int_cable'
    elif place=='interior' and conn=='wifi': key = 'cam_int_wifi'
    elif place=='exterior' and conn=='cable': key = 'cam_ext_cable'
    elif place=='exterior' and conn=='wifi': key = 'cam_ext_wifi'
    
    prod = PRODUCT_CATALOG.get(key, PRODUCT_CATALOG['cam_int_wifi'])
    state['final_prod'] = prod
    state['step'] = 'prod_confirm'
    return format_product_confirmation(prod), state

def handle_other_context(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    context = ""
    
    # Logic: 1->Casa, 2->Casa (Department), 3->Negocio (Building)
    # Also word matching
    if '1' in norm_input or 'casa' in norm_input: context = 'casa'
    elif '2' in norm_input or 'departamento' in norm_input: context = 'casa'
    elif '3' in norm_input or 'edificio' in norm_input: context = 'negocio'
    elif 'negocio' in norm_input: context = 'negocio'
    
    if not context:
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
    
    state['final_prod'] = prod
    state['step'] = 'prod_confirm'
    return format_product_confirmation(prod), state

def handle_product_confirm(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    if '1' in norm_input or 'si' in norm_input or 'confirmar' in norm_input:
        p = state['final_prod']
        phone = state.get('phone', 'WEB')
        
        desc = p['desc']
        extra = state.get('adicional', '')
        final_adicional = f"{desc} - {extra}" if extra else desc

        payload = {
            "Fecha": datetime.datetime.utcnow().isoformat(),
            "Telefono": phone,
            "Categoria": p['cat'],
            "Sector": state.get('sector', ''),
            "Adicional": final_adicional,
            "ReferidoPor": state.get('referral', 'Desconocido')
        }
        
        send_to_appsheet("Solicitudes", payload)
        
        state = {'step': 'menu_start', 'phone': phone}
        return (MSG_PROD_SUCCESS + MSG_MENU_MAIN), state
    else:
        state = {'step': 'menu_start', 'phone': state.get('phone')}
        return (MSG_GLOBAL_CANCEL + MSG_MENU_MAIN), state
