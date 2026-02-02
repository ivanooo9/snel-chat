import requests
from xml.etree import ElementTree

URL = "http://localhost:5000/chat"
PHONE = "whatsapp:+1234567897" # New number

def test_onboarding_flow():
    print("--- Starting Onboarding Flow Test (Single Message Caption) ---")

    # 2. First REAL interaction
    print("\n[Client] Sending 'Hola' (First real message)...")
    payload = {'From': PHONE, 'Body': 'Hola'}
    try:
        r = requests.post(URL, data=payload)
        r.raise_for_status()
        
        print(f"[Server] Response: {r.text}")
        root = ElementTree.fromstring(r.text)
        
        # In TwiML, when using resp.message("text").media("url"), it creates:
        # <Message>Text Content<Media>URL</Media></Message>
        # The text is the text content of the Message element, not a child element called Body.
        
        messages = root.findall('Message')
        if len(messages) == 1:
            msg = messages[0]
            media = msg.find('Media')
            
            # Check text content of <Message> (recursively or directly)
            # ElementTree .text property gives text before first child.
            text_content = msg.text if msg.text else ""
            
            has_media = media is not None and "cloudinary" in media.text
            has_text = "SNEL" in text_content
            
            if has_media and has_text:
                 print("✅ PASS: Single Message contains Text + Media.")
            else:
                 print(f"❌ FAIL: Missing Media or Text. Media={has_media}, TextContentFound={has_text}")
        else:
            print(f"❌ FAIL: Expected exactly 1 message, got {len(messages)}.")
            
    except Exception as e:
        print(f"❌ FAIL: Request error: {e}")

if __name__ == "__main__":
    test_onboarding_flow()
