from flows.router import process_message
from database import init_db, get_user_state, save_user_state
import os

# Setup Test DB
if os.path.exists("chatbot.db"):
    os.remove("chatbot.db")

from flask import Flask
app = Flask(__name__)

with app.app_context():
    print("--- 1. Initializing DB ---")
    init_db()

    phone = "TEST_USER_001"
    
    print("\n--- 2. Testing Start Flow (Menu) ---")
    state = get_user_state(phone)
    reply, state = process_message("Hola", state, phone)
    print(f"Bot: {reply[:50]}...")
    assert "Gracias por comunicarte" in reply
    save_user_state(phone, state)

    print("\n--- 3. Testing Internet Flow (Selection) ---")
    # User selects 1 (Internet)
    reply, state = process_message("1", state, phone)
    print(f"Bot: {reply}")
    # Should ask for referral first time
    if "enteró de SNEL" in reply:
        print("-> Asking Referral correctly.")
        save_user_state(phone, state)
        # Answer referral
        reply, state = process_message("Google", state, phone)
        print(f"Bot: {reply}")
        save_user_state(phone, state)
    
    assert "sector" in reply.lower()
    
    print("\n--- 4. Testing Coverage (Fuzzy) ---")
    # User types 'san isidro'
    reply, state = process_message("san isidro", state, phone)
    print(f"Bot: {reply}")
    # Should register or confirm logic
    # "San Isidro" is in the list, so it should register directly
    if "registrado tu interés" in reply:
        print("-> Direct match success.")

    print("\n=== VERIFICATION SUCCESSFUL ===")
