from flask import Flask, render_template, request, jsonify, session
from twilio.twiml.messaging_response import MessagingResponse
from config import SECRET_KEY, DEBUG, ONBOARDING_VIDEO_URL
from database import init_db, get_user_state, save_user_state
from flows.router import process_message
from utils.security import validate_twilio_request, sanitize_phone
from utils.logger import setup_logger
from utils.messages import MSG_FALLBACK_DEFAULT, MSG_GLOBAL_ERROR

logger = setup_logger(__name__)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize DB on startup
with app.app_context():
    init_db()

@app.route('/')
def index():
    session.clear() 
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    logger.info("--- INCOMING REQUEST /chat ---")
    
    # TEMPORARY: Validation only for WhatsApp
    is_whatsapp = "From" in request.form
    if is_whatsapp:
        if not validate_twilio_request(request):
            logger.warning("Twilio request validation failed.")
            return "Forbidden", 403

    try:
        # 1. Detect Source and Parse Input
        # is_whatsapp already calculated above
        user_input = request.form.get('Body', '') or request.form.get('message', '')
        
        sender_phone = None
        if is_whatsapp:
            sender_phone = sanitize_phone(request.form.get('From', ''))
        else:
            sender_phone = session.get('phone', 'WEB')
            # Special Web Init
            if user_input == "MENU_INIT":
                session.clear()
                session['step'] = 'menu_start'
                session['phone'] = 'WEB'
                return jsonify({'reply': "¡Hola soy Jenny tu asesora SNEL!..."}) # Simplified init reply or call router

        logger.info(f"Source: {'WhatsApp' if is_whatsapp else 'Web'} | Phone: {sender_phone} | Input: '{user_input}'")

        if not sender_phone:
             logger.error("Missing Phone in request")
             return "Missing Phone", 400

        # 2. State Management (SQLite)
        state = {}
        if is_whatsapp:
            state = get_user_state(sender_phone)
            if not state:
                state = {'step': 'menu_start', 'phone': sender_phone, 'video_sent': False}
        else:
            state = dict(session)
            state.setdefault('step', 'menu_start')
            state['phone'] = 'WEB'

        # 3. Process Message
        response_text, new_state = process_message(user_input, state, phone=sender_phone)
        
        # Fallback
        if not response_text:
            response_text = MSG_FALLBACK_DEFAULT

        # 4. Save State & Send Response
        if is_whatsapp:
            # Video Logic
            should_send_video = False
            if not state.get('video_sent', False):
                should_send_video = True
                new_state['video_sent'] = True
            
            save_user_state(sender_phone, new_state)
            
            # TwiML
            resp = MessagingResponse()
            msg = resp.message(response_text)
            
            if should_send_video and ONBOARDING_VIDEO_URL:
                logger.info(f"-> Attaching Video: {ONBOARDING_VIDEO_URL}")
                msg.media(ONBOARDING_VIDEO_URL)
            
            return str(resp), 200, {'Content-Type': 'application/xml'}

        else:
            # Web Response
            session.clear()
            for k, v in new_state.items():
                session[k] = v
            return jsonify({'reply': response_text})

    except Exception as e:
        logger.critical(f"CRITICAL ERROR in /chat: {e}", exc_info=True)
        return str(MessagingResponse().message(MSG_GLOBAL_ERROR))

if __name__ == '__main__':
    logger.info("Asistente SNEL Professional (Refactored) Running...")
    app.run(debug=DEBUG, port=5000)
