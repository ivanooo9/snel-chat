from services.calendar import create_appointment
from utils.messages import MSG_MENU_MAIN, MSG_GLOBAL_CANCEL, MSG_CAL_ASK_TIME, MSG_CAL_CONFIRM, MSG_CAL_SUCCESS

def handle_calendar_date(text: str, state: dict) -> tuple[str, dict]:
    state['cal_date'] = text.strip()
    state['step'] = 'cal_ask_time'
    return MSG_CAL_ASK_TIME, state

def handle_calendar_time(text: str, state: dict) -> tuple[str, dict]:
    state['cal_time'] = text.strip()
    
    d = state['cal_date']
    t = state['cal_time']
    state['step'] = 'cal_confirm'
    return MSG_CAL_CONFIRM.format(date=d, time=t), state

def handle_calendar_confirm(text: str, state: dict) -> tuple[str, dict]:
    norm_input = text.lower()
    if '1' in norm_input or 'si' in norm_input or 'sí' in norm_input or 'agendar' in norm_input:
        d = state['cal_date']
        t = state['cal_time']
        phone = state.get('phone', 'Desconocido')
        
        success, result = create_appointment(f"Cita SNEL - {phone}", f"Cliente: {phone}", d, t)
        
        if not success:
             # result contains the error message from services/calendar.py which already uses utils.messages
             return result, state
        
        link = result
        state = {'step': 'menu_start', 'phone': phone}
        return (MSG_CAL_SUCCESS.format(link=link) + MSG_MENU_MAIN), state
    else:
        state = {'step': 'menu_start', 'phone': state.get('phone')}
        return (MSG_GLOBAL_CANCEL + MSG_MENU_MAIN), state
