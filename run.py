import os
import sys
import logging
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant import PersonalAssistant

def setup_logging():
    """Configura el sistema de logs"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        filename=log_dir / "assistant.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    """Función principal para ejecutar el asistente"""
    print("Iniciando Asistente Personal...")
    print("\nComandos disponibles:")
    print("- 'abrir archivo [nombre]': Abre un archivo en el editor")
    print("- 'corregir código': Corrige el código del archivo actual")
    print("- 'sugerir mejoras': Sugiere mejoras para el código actual")
    print("- 'buscar [consulta]': Realiza una búsqueda en línea")
    print("- 'ayuda': Muestra esta lista de comandos")
    print("- 'salir': Cierra el asistente")
    
    setup_logging()
    asistente = PersonalAssistant()
    
    try:
        while True:
            comando = asistente.voice_handler.listen()
            if comando == "salir":
                print("¡Hasta luego!")
                break
            asistente.process_command(comando)
    except KeyboardInterrupt:
        print("\nCerrando el asistente...")
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        print("Ocurrió un error inesperado. Consulta los logs para más detalles.")

if __name__ == "__main__":
    main()
