import speech_recognition as sr
import pyttsx3
import logging
from config import Config

class VoiceHandler:
    def __init__(self):
        self.config = Config()
        self.speech = sr.Recognizer()
        self.engine = pyttsx3.init(self.config.get('voice_engine'))
        
        # Configuración del reconocimiento de voz
        self.speech.dynamic_energy_threshold = True
        self.speech.energy_threshold = 4000
        
        # Configuración del logger
        logging.basicConfig(
            filename='resources/voice.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def listen(self):
        """Escucha y reconoce comandos de voz usando Google Speech Recognition"""
        with sr.Microphone() as fuente:
            print("Escuchando...")
            self.speech.adjust_for_ambient_noise(fuente, duration=1)
            audio = self.speech.listen(fuente)
            try:
                texto = self.speech.recognize_google(audio, language=self.config.get('language'))
                logging.info(f"Comando reconocido: {texto}")
                print(f"Has dicho: {texto}")
                return texto.lower()
            except sr.UnknownValueError:
                logging.error("No se pudo entender el audio")
                return "No he podido entender el audio"
            except sr.RequestError as e:
                logging.error(f"Error en el servicio de reconocimiento: {str(e)}")
                return "Error en el servicio de reconocimiento de voz"

    def speak(self, texto):
        """Sintetiza texto a voz"""
        try:
            self.engine.say(texto)
            self.engine.runAndWait()
            logging.info(f"Mensaje hablado: {texto}")
        except Exception as e:
            logging.error(f"Error en síntesis de voz: {str(e)}")
            print(f"Error en síntesis de voz: {str(e)}")
