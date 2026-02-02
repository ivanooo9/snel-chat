from .menu import handle_menu_start, handle_referral
from .internet import handle_coverage_sector, handle_coverage_fuzzy, handle_no_coverage
from .products import (
    handle_product_type,
    handle_product_sector,
    handle_product_additional,
    handle_cam_place,
    handle_cam_conn,
    handle_other_context,
    handle_product_confirm,
    handle_ups_context
)
from .calendar import handle_calendar_date, handle_calendar_time, handle_calendar_confirm
from config import normalize
from utils.messages import MSG_MENU_MAIN, MSG_GLOBAL_ERROR
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Flow Mapping
FLOW_HANDLERS = {
    'menu_start': handle_menu_start,
    'global_ask_referral': handle_referral,
    
    # Internet
    'cov_ask_sector': handle_coverage_sector,
    'cov_confirm_fuzzy': handle_coverage_fuzzy,
    'cov_no_coverage': handle_no_coverage,
    
    # Products
    'prod_ask_type': handle_product_type,
    'prod_ask_sector': handle_product_sector,
    'prod_ask_additional': handle_product_additional,
    'prod_cam_place': handle_cam_place,
    'prod_cam_conn': handle_cam_conn,
    'prod_other_context': handle_other_context,
    'prod_confirm': handle_product_confirm,
    'prod_ask_ups_context': handle_ups_context,
    
    # Calendar
    'cal_ask_date': handle_calendar_date,
    'cal_ask_time': handle_calendar_time,
    'cal_confirm': handle_calendar_confirm,
}

def check_global_commands(user_input: str, state: dict) -> bool:
    norm = normalize(user_input)
    global_commands = ['menu', 'inicio', 'volver', 'empezar', 'cancelar']
    if any(cmd == norm or cmd in norm.split() for cmd in global_commands):
        return True
    return False

def process_message(user_input: str, state: dict, phone: str = None) -> tuple[str, dict]:
    """
    Main Router Function.
    """
    if phone and 'phone' not in state:
        state['phone'] = phone

    # 1. Global Interrupts
    if check_global_commands(user_input, state):
        return MSG_MENU_MAIN, {'step': 'menu_start', 'phone': state.get('phone')}

    # 2. Get Step
    step = state.get('step', 'menu_start')
    
    # 3. Dispatch
    handler = FLOW_HANDLERS.get(step)
    
    if not handler:
        # Fallback
        logger.warning(f"Unknown step {step}, falling back to menu.")
        return MSG_MENU_MAIN, {'step': 'menu_start', 'phone': state.get('phone')}
        
    try:
        reply, new_state = handler(user_input, state)
        return reply, new_state
    except Exception as e:
        logger.error(f"ERROR in flow dispatch: {e}", exc_info=True)
        return MSG_GLOBAL_ERROR, state
