# evenlabs_api.py

import requests

class ElevenLabsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"

    def synthesize_speech(self, text, voice_id, model_id="eleven_monolingual_v1", stability=0.5, similarity_boost=0.5):
        url = f"{self.base_url}/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open('output.mp3', 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return "output.mp3"
        else:
            return "Erreur lors de la synthèse vocale"

    def get_available_voices(self):
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            voices_data = response.json()
            return voices_data['voices']  # On suppose que la clé 'voices' contient la liste des voix
        else:
            return []
