import requests
import time
from config import APPSHEET_APP_ID, APPSHEET_KEY, APPSHEET_RETRIES, APPSHEET_TIMEOUT, APPSHEET_TEST_PHONE
from utils.logger import setup_logger

logger = setup_logger(__name__)

def send_to_appsheet(table_name: str, row_data: dict) -> bool:
    """
    Sends data to AppSheet with retry logic and timeout.
    Returns True if successful, False otherwise.
    """
    # Normalize Phone for testing/web
    phone = row_data.get("Telefono", "")
    if not phone or phone == "WEB" or len(str(phone)) < 5:
        logger.warning(f"Invalid Phone detected: '{phone}'. Replacing with TEST_PHONE.")
        row_data["Telefono"] = APPSHEET_TEST_PHONE
        
        # Append original source to Referral to keep track
        original_ref = row_data.get("ReferidoPor", "")
        row_data["ReferidoPor"] = f"{original_ref} (Source: {phone})"

    url = f"https://api.appsheet.com/api/v2/apps/{APPSHEET_APP_ID}/tables/{table_name}/Action"

    payload = {
        "Action": "Add",
        "Properties": {
            "Locale": "es-EC",
            "Timezone": "America/Guayaquil"
        },
        "Rows": [row_data]
    }

    headers = {
        "ApplicationAccessKey": APPSHEET_KEY,
        "Content-Type": "application/json"
    }

    logger.info(f"Sending to AppSheet Table: {table_name}")
    
    for attempt in range(1, APPSHEET_RETRIES + 1):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=APPSHEET_TIMEOUT)
            
            if response.status_code == 200:
                logger.info(f"AppSheet Success (Attempt {attempt})")
                return True
            else:
                logger.warning(f"AppSheet Failed (Attempt {attempt}): {response.status_code} - {response.text}")
        
        except requests.exceptions.RequestException as e:
            logger.warning(f"AppSheet Error (Attempt {attempt}): {e}")
        
        if attempt < APPSHEET_RETRIES:
            time.sleep(1) # Linear backoff

    logger.error("Failed to send to AppSheet after all retries.")
    return False
