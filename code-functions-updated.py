import subprocess
import logging
from pathlib import Path
import json
from gpt4all import GPT4All  # Modelo de lenguaje gratuito
import requests
from bs4 import BeautifulSoup

class CodeHandler:
    def __init__(self):
        self.model = GPT4All("ggml-model-gpt4all-j-v1.3-groovy")  # Modelo gratuito
        logging.basicConfig(
            filename='resources/code.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def edit_code(self, file_path, nuevo_codigo=None):
        """Edita archivos de código usando el editor predeterminado"""
        try:
            file_path = Path(file_path)
            if nuevo_codigo:
                with open(file_path, 'w') as f:
                    f.write(nuevo_codigo)
                logging.info(f"Código actualizado en {file_path}")
                return True
            else:
                with open(file_path, 'r') as f:
                    return f.read()
        except Exception as e:
            logging.error(f"Error al manipular archivo: {str(e)}")
            return None

    def correct_code(self, codigo):
        """Corrige el código usando GPT4All"""
        try:
            prompt = f"""Revisa y corrige el siguiente código Python:
            {codigo}
            Proporciona solo el código corregido sin explicaciones adicionales."""
            
            respuesta = self.model.generate(prompt, max_tokens=500)
            logging.info("Código corregido generado")
            return respuesta
        except Exception as e:
            logging.error(f"Error al corregir código: {str(e)}")
            return f"Error al corregir el código: {str(e)}"

    def suggest_improvements(self, codigo):
        """Genera sugerencias usando GPT4All"""
        try:
            prompt = f"""Analiza este código Python y sugiere mejoras:
            {codigo}
            Proporciona sugerencias específicas y prácticas."""
            
            respuesta = self.model.generate(prompt, max_tokens=500)
            logging.info("Sugerencias generadas")
            return respuesta
        except Exception as e:
            logging.error(f"Error al generar sugerencias: {str(e)}")
            return f"Error al generar sugerencias: {str(e)}"

    def search_online(self, consulta):
        """Realiza búsquedas usando Searx (motor de búsqueda libre)"""
        try:
            # Usa una instancia pública de Searx
            url = f"https://searx.be/search?q={consulta}&format=json"
            respuesta = requests.get(url)
            resultados = respuesta.json()
            
            if resultados.get('results'):
                return resultados['results'][0]['content']
            else:
                return "No se encontraron resultados"
        except Exception as e:
            logging.error(f"Error en búsqueda: {str(e)}")
            return "Error al realizar la búsqueda"

    def open_editor(self, file_path):
        """Abre el editor de código predeterminado"""
        try:
            if Path(file_path).exists():
                if os.name == 'nt':  # Windows
                    os.startfile(file_path)
                else:  # Linux/Mac
                    subprocess.run(['xdg-open', file_path])
                logging.info(f"Editor abierto para {file_path}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error al abrir editor: {str(e)}")
            return False
