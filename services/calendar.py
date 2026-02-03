import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import CALENDAR_ID, TIMEZONE, SERVICE_ACCOUNT_FILE, GOOGLE_CALENDAR_SCOPES
from utils.logger import setup_logger
from utils.messages import MSG_CAL_ERROR_COLLISION, MSG_CAL_ERROR_CREATE, MSG_CAL_ERROR_FORMAT

logger = setup_logger(__name__)

def get_calendar_service():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=GOOGLE_CALENDAR_SCOPES
        )
        return build('calendar', 'v3', credentials=credentials)
    except Exception as e:
        logger.error(f"Error initializing Calendar service: {e}")
        return None

def check_collision(service, start_dt: datetime.datetime, end_dt: datetime.datetime) -> bool:
    """
    Checks for event collisions in the given time range.
    Returns True if collision exists, False usually.
    """
    try:
        # Ensure we send proper offset time string if naive
        start_str = start_dt.isoformat()
        end_str = end_dt.isoformat()
        
        if start_dt.tzinfo is None:
             start_str += '-05:00'
             end_str += '-05:00'

        events_result = service.events().list(
            calendarId="339d3661b13192ae764b2b469df74870e9738b47db5044d380f2f5cd986dec72@group.calendar.google.com",
            timeMin=start_str,
            timeMax=end_str,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        items = events_result.get('items', [])
        return len(items) > 0
    except Exception as e:
        logger.error(f"Error checking collisions: {e}")
        return False # Fail open usually safer for UX unless strict.

def create_appointment(summary: str, description: str, date_str: str, time_str: str) -> tuple[bool, str]:
    """
    Creates an appointment if no collision.
    Returns: (success_bool, message_or_link)
    """
    service = get_calendar_service()
    if not service:
        return False, MSG_CAL_ERROR_CREATE

    try:
        # Parse inputs
        start_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + datetime.timedelta(hours=1)
        
        # Check Collision
        if check_collision(service, start_dt, end_dt):
            logger.info(f"Collision detected for {date_str} {time_str}")
            return False, MSG_CAL_ERROR_COLLISION

        # Create Event
        event_body = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': TIMEZONE,
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': TIMEZONE,
            },
        }

        created_event = service.events().insert(
            calendarId=CALENDAR_ID,
            body=event_body
        ).execute()

        link = created_event.get('htmlLink', '')
        logger.info(f"Appointment created: {link}")
        return True, link

    except ValueError:
        logger.warning(f"Invalid date/time format: {date_str} {time_str}")
        return False, MSG_CAL_ERROR_FORMAT
    except Exception as e:
        logger.error(f"Error creating appointment: {e}")
        return False, MSG_CAL_ERROR_CREATE
