import os
import sys
import subprocess
import json
import platform
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 8):
        print("Se requiere Python 3.8 o superior")
        sys.exit(1)

def create_directory_structure():
    """Crea la estructura de directorios"""
    directories = [
        'resources',
        'workspace',
        'models',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Directorio '{directory}' creado")

def create_config():
    """Crea el archivo de configuración inicial"""
    config = {
        "language": "es-ES",
        "voice_engine": "sapi5" if platform.system() == "Windows" else "espeak",
        "log_level": "INFO",
        "workspace_path": str(Path("workspace").absolute()),
        "model_path": str(Path("models").absolute())
    }
    
    config_path = Path("resources/config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    print("✓ Archivo de configuración creado")

def install_system_dependencies():
    """Instala dependencias del sistema según el OS"""
    system = platform.system()
    
    if system == "Linux":
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y",
                          "python3-pyaudio",
                          "portaudio19-dev",
                          "espeak"], check=True)
            print("✓ Dependencias del sistema instaladas")
        except subprocess.CalledProcessError:
            print("Error instalando dependencias del sistema")
            sys.exit(1)
    elif system == "Windows":
        print("Windows: No se requieren dependencias adicionales del sistema")

def install_python_dependencies():
    """Instala las dependencias de Python"""
    requirements = [
        "speech_recognition==3.10.0",
        "pyttsx3==2.90",
        "requests==2.31.0",
        "gpt4all==1.0.8",
        "beautifulsoup4==4.12.2",
        "pathlib==1.0.1",
        "pyaudio==0.2.13"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencias de Python instaladas")
    except subprocess.CalledProcessError:
        print("Error instalando dependencias de Python")
        sys.exit(1)

def download_gpt4all_model():
    """Descarga el modelo de GPT4All"""
    try:
        from gpt4all import GPT4All
        model_path = Path("models")
        print("Descargando modelo GPT4All (esto puede tardar varios minutos)...")
        GPT4All.download_model("ggml-model-gpt4all-j-v1.3-groovy", model_path)
        print("✓ Modelo GPT4All descargado")
    except Exception as e:
        print(f"Error descargando el modelo GPT4All: {str(e)}")
        sys.exit(1)

def test_installation():
    """Prueba los componentes principales"""
    try:
        # Prueba reconocimiento de voz
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("✓ Micrófono detectado")
        
        # Prueba síntesis de voz
        import pyttsx3
        engine = pyttsx3.init()
        engine.say("Instalación completada con éxito")
        engine.runAndWait()
        print("✓ Síntesis de voz funcionando")
        
        return True
    except Exception as e:
        print(f"Error en la prueba de instalación: {str(e)}")
        return False

def main():
    print("Iniciando instalación del Asistente Personal...")
    
    check_python_version()
    create_directory_structure()
    create_config()
    install_system_dependencies()
    install_python_dependencies()
    download_gpt4all_model()
    
    if test_installation():
        print("\n¡Instalación completada con éxito!")
        print("\nPara iniciar el asistente ejecuta:")
        print("python assistant.py")
    else:
        print("\nLa instalación se completó con algunos errores.")
        print("Por favor, revisa los mensajes anteriores.")

if __name__ == "__main__":
    main()
