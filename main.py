import asyncio

from app.controller.background_substractor import run_secuence

# coorelaciones con matlab
# "background_mean" es la variable "T"
# Francisco Sierra Pérez

# TODO: Cambiar Listas a Tuplas
# TODO: Implementar hilos para generar mensaje
# TODO: Substracción de fondo debe trabajar a colores
if __name__ == '__main__':
    videos = [
        "resources/secuencia1.avi",
        # "resources/secuencia2.avi",
        # "resources/secuencia3.avi",
        # "resources/secuencia4.avi",
        # "resources/secuencia5.avi",
        # "resources/secuencia6.avi",
        # "resources/secuencia7.avi",
        # "resources/grandcentral.avi"
    ]
    for video in videos:
        try:
            run_secuence(video, hilos=1)
        except Exception as e:
            print(f"Exception: {e}")
            pass
