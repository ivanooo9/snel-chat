import difflib
import datetime
from config import normalize, NORMALIZED_SECTORS
from services.appsheet import send_to_appsheet
from utils.messages import (
    MSG_MENU_MAIN, MSG_COV_ASK_SECTOR, MSG_COV_FUZZY_CONFIRM, 
    MSG_COV_NO_COVERAGE, MSG_COV_INVALID_OPTION, MSG_COV_SUCCESS, 
    MSG_COV_ERROR_APPSHEET, MSG_GLOBAL_CANCEL, MSG_PROD_MENU_TYPE
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

def handle_coverage_sector(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    found_sector = None
    
    # Direct match logic
    sorted_keys = sorted(NORMALIZED_SECTORS.keys(), key=len, reverse=True)
    for k in sorted_keys:
        if k in norm_input:
            found_sector = NORMALIZED_SECTORS[k]
            break
    
    if found_sector:
        return _register_internet_request(found_sector, state)
    
    # Fuzzy match
    matches = difflib.get_close_matches(norm_input, NORMALIZED_SECTORS.keys(), n=1, cutoff=0.6)
    if matches:
        real_name = NORMALIZED_SECTORS[matches[0]]
        state['temp_sector'] = real_name
        state['step'] = 'cov_confirm_fuzzy'
        return MSG_COV_FUZZY_CONFIRM.format(sector=real_name), state
    
    # No coverage
    state['step'] = 'cov_no_coverage'
    return MSG_COV_NO_COVERAGE, state

def handle_coverage_fuzzy(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    if 'sí' in norm_input or 'si' in norm_input or '1' in norm_input or 'ok' in norm_input:
        real_name = state.pop('temp_sector', '')
        return _register_internet_request(real_name, state)
    else:
        state = {'step': 'menu_start', 'phone': state.get('phone')}
        return (MSG_GLOBAL_CANCEL + MSG_MENU_MAIN), state

def handle_no_coverage(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    
    if '1' in norm_input or 'productos' in norm_input or 'seguridad' in norm_input:
        state['step'] = 'prod_ask_type'
        return MSG_PROD_MENU_TYPE, state
    elif '2' in norm_input or 'cancelar' in norm_input or 'volver' in norm_input or 'menu' in norm_input:
        state = {'step': 'menu_start', 'phone': state.get('phone')}
        return (MSG_GLOBAL_CANCEL + MSG_MENU_MAIN), state
    else:
        return MSG_COV_INVALID_OPTION, state

def _register_internet_request(sector: str, state: dict) -> tuple[str, dict]:
    phone = state.get('phone', 'WEB')
    referral = state.get('referral', 'Desconocido')
    
    payload = {
        "Fecha": datetime.datetime.utcnow().isoformat(),
        "Telefono": phone,
        "Categoria": "Internet",
        "Sector": sector,
        "Adicional": "-",
        "ReferidoPor": referral
    }
    
    success = send_to_appsheet("Solicitudes", payload)
    
    state = {'step': 'menu_start', 'phone': phone}
    
    if success:
        return (MSG_COV_SUCCESS.format(sector=sector, phone=phone) + MSG_MENU_MAIN), state
    else:
        return (MSG_COV_ERROR_APPSHEET + MSG_MENU_MAIN), state
