import os
import logging
from pathlib import Path
from voice_commands import VoiceHandler
from code_functions import CodeHandler
from config import Config

class PersonalAssistant:
    def __init__(self):
        self.config = Config()
        self.voice_handler = VoiceHandler()
        self.code_handler = CodeHandler()
        self.current_file = None
        
        # Configurar logging
        logging.basicConfig(
            filename='resources/assistant.log',
            level=getattr(logging, self.config.get('log_level')),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Crear directorio de trabajo
        self.workspace = Path('workspace')
        self.workspace.mkdir(exist_ok=True)

    def process_command(self, comando):
        """Procesa los comandos de voz"""
        try:
            if not comando or not isinstance(comando, str):
                self.voice_handler.speak("No he podido procesar el comando")
                return

            logging.info(f"Procesando comando: {comando}")

            if 'abrir archivo' in comando:
                nombre_archivo = comando.split('abrir archivo')[-1].strip()
                path = self.workspace / nombre_archivo
                if self.code_handler.open_editor(path):
                    self.current_file = path
                    self.voice_handler.speak(f"Archivo {nombre_archivo} abierto")
                else:
                    self.voice_handler.speak("No se pudo abrir el archivo")

            elif 'corregir código' in comando:
                if not self.current_file:
                    self.voice_handler.speak("Primero debes abrir un archivo")
                    return
                
                codigo_actual = self.code_handler.edit_code(self.current_file)
                if codigo_actual:
                    codigo_corregido = self.code_handler.correct_code(codigo_actual)
                    if self.code_handler.edit_code(self.current_file, codigo_corregido):
                        self.voice_handler.speak("He corregido el código")
                    else:
                        self.voice_handler.speak("Hubo un error al aplicar las correcciones")

            elif 'sugerir mejoras' in comando:
                if not self.current_file:
                    self.voice_handler.speak("Primero debes abrir un archivo")
                    return
                
                codigo_actual = self.code_handler.edit_code(self.current_file)
                if codigo_actual:
                    sugerencias = self.code_handler.suggest_improvements(codigo_actual)
                    self.voice_handler.speak("Aquí están mis sugerencias para mejorar el código")
                    print(sugerencias)

            elif 'buscar' in comando:
                consulta = comando.split('buscar')[-1].strip()
                resultado = self.code_handler.search_online(consulta)
                self.voice_handler.speak(resultado)
                print(resultado)

            elif 'ayuda' in comando:
                self.show_help()

            else:
                self.voice_handler.speak("Comando no reconocido. Di 'ayuda' para ver los comandos disponibles")

        except Exception as e:
            logging.error(f"Error procesando comando: {str(e)}")
            self.voice_handler.speak("Hubo un error al procesar el comando")

    def show_help(self):
        """Muestra la lista de comandos disponibles"""
        help_text = """
        Comandos disponibles:
        - 'abrir archivo [nombre]': Abre un archivo en el editor
        - 'corregir código': Corrige el código del archivo actual
        - 'sugerir mejoras': Sugiere mejoras para el código actual
        - 'buscar [consulta]': Realiza una búsqueda en línea
        - 'ayuda': Muestra esta lista de comandos
        - 'salir': Cierra el asistente
        """
        print(help_text)
        self.voice_handler.speak("He mostrado la lista de comandos disponibles")

def main():
    asistente = PersonalAssistant()
    print("Asistente personal iniciado. Di 'ayuda' para ver los comandos disponibles.")
    
    while True:
        comando = asistente.voice_handler.listen()
        if comando == "salir":
            print("¡Hasta luego!")
            break
        asistente.process_command(comando)

if __name__ == "__main__":
    main()
