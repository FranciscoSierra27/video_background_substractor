import sys
import cv2
import numpy as np
from multiprocessing import Process, Queue
from image_slicer import slice


def modelo_Fondo(rho, image):
  try:
    M = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # _, img = video.read()
    img = image
    imagen = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret = imagen
    
    if ret.any():
      # ---------------MODELO DE FONDO GAUSIANO----------------------#
      
      M = rho * M + (1 - rho) * imagen
      # S = rho * S + (1 - rho) * (M - imagen) ** 2 | S es para deteccion de movimiento
      
      cv2.imshow('Videos Orginal', np.uint8(imagen))
      cv2.imshow('Media Estimada', np.uint8(np.fix(M)))
      
      if cv2.waitKey(24) & 0xFF == ord('s'):
        pass
    else:
      pass
    return M, imagen
  except:
    return print("Unexpected error:", sys.exc_info()[0])


def detencion_Movimiento(rho, S, image):
  try:
    M = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # _, img = video.read()
    img = image
    imagen = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret = imagen
    
    if ret.any():
      
      # ---------------MODELO DE FONDO GAUSIANO----------------------#
      
      M = rho * M + (1 - rho) * imagen
      S = rho * S + (1 - rho) * (M - imagen) ** 2
      
      # -------------------DETECTAR MOVIMIENTO-----------------------#
      
      Cp = np.sqrt(((imagen - M) ** 2) / S)
      Mov = Cp > 2
      MovT = Mov * imagen
      
      cv2.imshow('Mapa del Movimiento 1', np.uint8((Mov * 255)))
      cv2.imshow('Mapa del Movimiento 2', MovT)
      
      if cv2.waitKey(24) & 0xFF == ord('s'):
        pass
    else:
      pass
    return Mov, MovT
  except:
    return print("Unexpected error:", sys.exc_info()[0])


if __name__ == '__main__':
  consulta = Queue()
  
  video = cv2.VideoCapture('resources/secuencia1.avi')
  _, img = video.read()

  # M = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  | La calculamos para cada imagen dentro de ña funcion
  
  S = 100 * np.ones((240, 360))
  rho = 1 - 1 / (30 * 10)

  # cv2.imwrite('img.jpg',img)
  # s_image = cv2.imread('img.jpg')

  # -------------------------DIVIDIMNOS LA IMAGEN(ARRAY) EN 4 PARTES--------------------#

  
  while video.isOpened():
    # ----------------------CALCULO DEL MODELO DE FONDO EN PARALELO------------------------#

    p_fondo1 = Process(target=modelo_Fondo, args=(rho, img))
    
    p_fondo1.start()
    p_fondo1.join()
    
    # ----------------------DETECCION DE MOVIMIENTO EN PARALELO-------------------------#
    
    p_movi1 = Process(target=detencion_Movimiento, args=(rho, S, img))
    
    p_movi1.start()
    p_movi1.join()
    
    # ---------------------PRUEBA SIN PARALELO-----------------#
    # imagen = video.read()
    # mf = modelo_Fondo(rho, img1)
    # dm = detencion_Movimiento(rho, M, S, img1)
  
  video.release()
  cv2.destroyAllWindows()
