import base64
import json

def decode_jwt(jwt_token):
    try:
        # Divide el JWT en sus tres partes
        header, payload, signature = jwt_token.split(".")
        
        # Decodifica el payload (contiene la información del usuario)
        decoded_payload = json.loads(base64.urlsafe_b64decode(payload + "==").decode("utf-8"))
        print(decoded_payload)
        return decoded_payload
    except Exception as e:
        print(f"Error al decodificar el JWT: {e}")
        return None