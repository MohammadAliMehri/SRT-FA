import requests
import time

# Create a session for connection pooling
session = requests.Session()

def translate_block(text, source_lang='en', target_lang='fa'):
    """
    Translates text from source_lang to target_lang using Google Translate's free API (gtx).
    Uses a persistent session and batching (via separator) for better performance.
    """
    if not text or not text.strip():
        return ""

    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source_lang,
        "tl": target_lang,
        "dt": "t", # 't' means return translation
        "q": text,
    }

    try:
        # Simple retry mechanism
        for attempt in range(3):
            try:
                # Use session for connection reuse
                r = session.get(url, params=params, timeout=10)
                r.raise_for_status()
                data = r.json()
                
                # result[0] is a list of [translated, original, ...]
                if data and isinstance(data, list) and len(data) > 0:
                    translated_chunks = [item[0] for item in data[0] if item and len(item) > 0 and item[0]]
                    return "".join(translated_chunks)
                
                return text # Fallback
            except requests.RequestException:
                if attempt == 2: raise
                time.sleep(1)
                
    except Exception as e:
        print(f"Error translating block: {e}")
        return text
