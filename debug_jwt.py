from datetime import datetime, timezone
from jose import jwt, JWTError
from app.core.config import settings

# Script para debuggear JWT tokens

def test_token_generation():
    """Prueba generar y decodificar un token"""
    print("=== TEST DE GENERACIÓN DE TOKEN ===\n")
    
    # Datos de prueba
    test_data = {"sub": 1}
    
    # Crear token
    from app.core.jwt import create_access_token
    token = create_access_token(test_data)
    
    print(f"Token generado: {token[:50]}...\n")
    
    # Intentar decodificar
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print("✅ Token decodificado exitosamente")
        print(f"Payload: {payload}\n")
        
        # Verificar expiración
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            diff = exp_time - now
            
            print(f"Hora actual (UTC): {now}")
            print(f"Expira en (UTC): {exp_time}")
            print(f"Tiempo restante: {diff.total_seconds()/60:.2f} minutos")
            
            if diff.total_seconds() > 0:
                print("✅ Token válido y no expirado")
            else:
                print("❌ Token ya expiró!")
    except JWTError as e:
        print(f"❌ Error al decodificar: {e}")
    
    return token


def test_token_from_env():
    """Verifica la configuración desde .env"""
    print("\n=== VERIFICACIÓN DE CONFIGURACIÓN ===\n")
    print(f"DATABASE_URL: {settings.DATABASE_URL[:30]}...")
    print(f"SECRET_KEY length: {len(settings.SECRET_KEY)} caracteres")
    print(f"ALGORITHM: {settings.ALGORITHM}")
    print(f"ACCESS_TOKEN_EXPIRE_MINUTES: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
    print(f"REFRESH_TOKEN_EXPIRE_DAYS: {settings.REFRESH_TOKEN_EXPIRE_DAYS}\n")


def test_decode_specific_token(token: str):
    """Decodifica un token específico"""
    print("\n=== DECODIFICACIÓN DE TOKEN ESPECÍFICO ===\n")
    print(f"Token: {token[:50]}...\n")
    
    try:
        # Intentar decodificar sin verificar expiración
        payload_no_verify = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": False}
        )
        print("Payload (sin verificar expiración):")
        print(payload_no_verify)
        
        exp_timestamp = payload_no_verify.get("exp")
        if exp_timestamp:
            exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            diff = exp_time - now
            
            print(f"\nHora actual (UTC): {now}")
            print(f"Token expira en: {exp_time}")
            print(f"Diferencia: {diff.total_seconds()/60:.2f} minutos")
            
            if diff.total_seconds() < 0:
                print("❌ Token EXPIRADO")
            else:
                print("✅ Token VÁLIDO")
        
        # Ahora con verificación
        print("\n--- Verificando con validación completa ---")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print("✅ Token válido y no expirado")
        
    except jwt.ExpiredSignatureError:
        print("❌ ERROR: Token expirado")
    except jwt.JWTError as e:
        print(f"❌ ERROR JWT: {e}")


if __name__ == "__main__":
    # Test 1: Configuración
    test_token_from_env()
    
    # Test 2: Generar nuevo token
    new_token = test_token_generation()
    
    # Test 3: Si tienes un token que falla, ponlo aquí
    print("\n" + "="*50)
    failing_token = input("\n¿Tienes un token que está fallando? Pégalo aquí (o Enter para omitir): ").strip()
    
    if failing_token:
        test_decode_specific_token(failing_token)
