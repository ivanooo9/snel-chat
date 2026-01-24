from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_ID = '339d3661b13192ae764b2b469df74870e9738b47db5044d380f2f5cd986dec72@group.calendar.google.com'
TIMEZONE = 'America/Guayaquil'


def obtener_servicio_calendar():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=credentials)


def crear_cita(resumen, descripcion, fecha, hora):
    service = obtener_servicio_calendar()

    start_dt = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + timedelta(hours=1)

    # ---------- VALIDACIÓN DE CHOQUE ----------
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat() + '-05:00',
        timeMax=end_dt.isoformat() + '-05:00',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    if events_result.get('items', []):
        return {
            "status": "ocupado",
            "mensaje": (
                "⛔ Ese horario ya está ocupado.\n"
                "Elige otra hora o escribe *Menu* para volver al inicio."
            )
        }

    # ---------- CREAR EVENTO ----------
    evento = {
        'summary': resumen,
        'description': descripcion,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': TIMEZONE,
        },
    }

    evento_creado = service.events().insert(
        calendarId=CALENDAR_ID,
        body=evento
    ).execute()

    return {
        "status": "ok",
        "link": evento_creado.get('htmlLink'),
        "mensaje": (
            "✅ Tu cita fue agendada con éxito.\n"
            f"🔗 Link del evento: {evento_creado.get('htmlLink')}\n\n"
            "Escribe *Menu* para volver al menú principal."
        )
    }
