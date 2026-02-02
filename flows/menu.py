from config import normalize
from utils.messages import MSG_MENU_MAIN, MSG_MENU_ERROR_SELECTION, MSG_REFERRAL_QUESTION, MSG_REFERRAL_ERROR, MSG_PROD_MENU_TYPE, MSG_COV_ASK_SECTOR, MSG_CAL_ASK_DATE
from utils.logger import setup_logger

logger = setup_logger(__name__)

def handle_menu_start(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    
    # 1. Internet
    if '1' in norm_input or 'internet' in norm_input or 'planes' in norm_input:
        if 'referral' not in state:
            state['pending_next_step'] = 'cov_ask_sector'
            state['step'] = 'global_ask_referral'
            return MSG_REFERRAL_QUESTION, state
            
        state['step'] = 'cov_ask_sector'
        return MSG_COV_ASK_SECTOR, state

    # 2. Productos
    elif '2' in norm_input or 'producto' in norm_input or 'seguridad' in norm_input:
        if 'referral' not in state:
            state['pending_next_step'] = 'prod_ask_type'
            state['step'] = 'global_ask_referral'
            return MSG_REFERRAL_QUESTION, state

        state['step'] = 'prod_ask_type'
        return MSG_PROD_MENU_TYPE, state

    # 3. Calendar
    elif '3' in norm_input or 'agendar' in norm_input or 'cita' in norm_input:
        state['step'] = 'cal_ask_date'
        return MSG_CAL_ASK_DATE, state

    else:
        return MSG_MENU_MAIN + MSG_MENU_ERROR_SELECTION, state

def handle_referral(text: str, state: dict) -> tuple[str, dict]:
    norm_input = normalize(text)
    ref_map = {
        '1': "Redes Sociales",
        '2': "Volantes",
        '3': "Google",
        '4': "ChatGPT",
        '5': "Pantalla Publicitaria",
        '6': "Eventos"
    }
    
    selected = None
    for k, v in ref_map.items():
        if k in norm_input or normalize(v) in norm_input:
            selected = v
            break
    
    if selected:
        state['referral'] = selected
        next_step = state.get('pending_next_step', 'menu_start')
        state['step'] = next_step
        
        # Resume flow
        if next_step == 'cov_ask_sector':
            return MSG_COV_ASK_SECTOR, state
        
        elif next_step == 'prod_ask_type':
            return MSG_PROD_MENU_TYPE, state
        
        else:
            return MSG_MENU_MAIN, {'step': 'menu_start'}
    else:
        return (MSG_REFERRAL_ERROR + MSG_REFERRAL_QUESTION), state

