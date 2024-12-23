import PyInstaller.__main__
import sys
import os
import shutil
from pathlib import Path

def clean_dist():
    """Limpia las carpetas de distribución anteriores"""
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    if os.path.exists('asistente.spec'):
        os.remove('asistente.spec')

def copy_resources(dist_path):
    """Copia los recursos necesarios a la carpeta de distribución"""
    resources_dir = os.path.join(dist_path, 'resources')
    models_dir = os.path.join(dist_path, 'models')
    workspace_dir = os.path.join(dist_path, 'workspace')
    
    # Crear directorios necesarios
    for dir_path in [resources_dir, models_dir, workspace_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
    # Copiar archivos de configuración
    if os.path.exists('resources/config.json'):
        shutil.copy2('resources/config.json', resources_dir)

def main():
    clean_dist()
    
    print("Creando ejecutable...")
    
    PyInstaller.__main__.run([
        'run.py',                      # Script principal
        '--name=AsistentePersonal',    # Nombre del ejecutable
        '--onefile',                   # Un solo archivo ejecutable
        '--noconsole',                 # Sin ventana de consola
        '--add-data=voice_commands.py;.',  # Agregar módulos como datos
        '--add-data=code_functions.py;.',
        '--add-data=config.py;.',
        '--add-data=assistant.py;.',
        '--add-data=resources;resources',
        '--hidden-import=voice_commands',
        '--hidden-import=code_functions',
        '--hidden-import=config',
        '--hidden-import=assistant',
        '--hidden-import=pyttsx3.drivers',
        '--hidden-import=pyttsx3.drivers.sapi5',
        '--hidden-import=gpt4all',
        '--hidden-import=pyaudio',
        '--hidden-import=speech_recognition'
    ])
    
    print("\nEjecutable creado exitosamente en la carpeta 'dist'")
    print("Nombre del ejecutable: AsistentePersonal.exe")

if __name__ == "__main__":
    main()
