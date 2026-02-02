from twilio.request_validator import RequestValidator
from config import TWILIO_AUTH_TOKEN, DEBUG
from utils.logger import setup_logger

logger = setup_logger(__name__)

def validate_twilio_request(request):
    """Validates that incoming requests are from Twilio."""
    # Skip validation in debug/dev mode if token is missing
    if DEBUG and not TWILIO_AUTH_TOKEN:
        logger.warning("Twilio validation skipped (DEBUG mode)")
        return True

    validator = RequestValidator(TWILIO_AUTH_TOKEN)

    # The Twilio signature is passed in the 'X-Twilio-Signature' header
    signature = request.headers.get('X-Twilio-Signature', '')
    
    # The full URL of the request as Twilio sees it
    url = request.url
    if 'http://' in url and 'ngrok' in url:
            url = url.replace('http://', 'https://') # Twilio usually forces https

    # The POST parameters
    params = request.form.to_dict()

    if not validator.validate(url, params, signature):
        logger.error(f"Security Alert: Invalid Twilio Signature. URL: {url}")
        return False
    
    return True

def sanitize_phone(phone_number: str) -> str:
    """Basic sanitization for phone numbers."""
    if not phone_number: return "UNKNOWN"
    return phone_number.replace('whatsapp:', '').strip()
