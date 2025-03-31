import jwt # PyJWT

def decode_jwt(token):
    try:
        # Nota: En producción, deberías verificar la firma con tu clave secreta
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded
    except jwt.exceptions.DecodeError:
        return None