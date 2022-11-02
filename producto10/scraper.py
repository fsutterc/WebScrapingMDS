#!/usr/bin/env python
# coding: utf-8

# In[1]:


#--------------------------------------------------------------------------------
# 01. Librerías
#--------------------------------------------------------------------------------

## Para Guardar en Carpetas
import os 

## Generar Pausas
import time  
import datetime



## Herramienta de recolección de datos para Web hecha con Javascript
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select 
from selenium.common.exceptions import NoSuchElementException   

## Driver Google Chrome
from webdriver_manager.chrome import ChromeDriverManager

## Manejo de DataFrame
import pandas as pd


# In[2]:


#--------------------------------------------------------------------------------
# 02. Configuración y Activación del Driver de Google 
#--------------------------------------------------------------------------------

## Configurar el Driver
chromeOptions = webdriver.ChromeOptions()
path = os.path.join(os.getcwd(), 'output basico\\')
prefs = {'download.default_directory': path, 'directory_upgrade': True}
chromeOptions.add_experimental_option('prefs', prefs)
# chromeOptions.add_argument('--headless') ## Trabajar en segundo Plano


# In[ ]:


#--------------------------------------------------------------------------------
# 03. Etapa de Extracción
#--------------------------------------------------------------------------------

categorias = ['vinos-cervezas-y-licores']

URL = 'https://www.jumbo.cl/'

## Uso del Driver
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chromeOptions)

marca = [] 
nombre = []
unidad = [] 
precio = [] 


## Recorriendo las Categorías (para efectos prácticos, solo se consideraron las tres categorías inicales)
for categoria in categorias[0:3]:
    ## Recorriendo las páginas de la categoría de momento
    for i in range(1,5,1):
        driver.get(URL+categoria+'?page='+str(i))
        ## Una pausa (dependerá de la conexión de internet y de los elementos que tiene la página JS)
        time.sleep(10) 
        ## Recorrer la lista de precios por hoja 
        for j in range(1,50,1):
            try:
                ## Verificar si tenemos el precio. Dado a esto, captamos el resto de información. Caso contrario, Ignorar y seguir con el siguiente.
                precio.append(driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/main/div[3]/div[2]/div[1]/ul/li['+str(j)+']/div/div[2]/div/span[1]').text)
                try:
                    marca.append(driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/main/div[3]/div[2]/div[1]/ul/li['+str(j)+']/div/div[1]/div[3]/div/a[1]/h2').text)
                    nombre.append(driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/main/div[3]/div[2]/div[1]/ul/li['+str(j)+']/div/div[1]/div[3]/div/a[2]/h2').text)
                    unidad.append(driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/main/div[3]/div[2]/div[1]/ul/li['+str(j)+']/div/div[1]/div[3]/div/span').text)
                except NoSuchElementException:
                    False 
                True
            except NoSuchElementException:
                False 
            True 
        time.sleep(5)

driver.close() ## Cerrar el navegador robot
#--------------------------------------------------------------------------------
# 04. Llevar la extracción a un DataFrame
#--------------------------------------------------------------------------------

dataset = pd.DataFrame([marca,nombre,unidad,precio]).T.rename(columns= {0: 'marca', 1:'nombre',2:'unidad',3: 'precio'})

dataset.sample(25)




# In[4]:


dataset.to_excel('JUMBO_precios_Vinos_y_Licores '+str(datetime.date.today())+'.xlsx')


# In[ ]:


#--------------------------------------------------------------------------------
# 05. ANEXO
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
## Base Producto (Marca, Nombre, Precio, etc.)
# //*[@id="root"]/div/div[2]/div/div/main/div[3]/div[2]/div[1]/ul/li[1]

#--------------------------------------------------------------------------------
## Marca
# //*[@id="root"]/div/div[2]/div/div/main/div[3]/div[2]/div[1]/ul/li[1]/div/div[1]/div[3]/div/a[1]/h2

#--------------------------------------------------------------------------------
## Nombre Producto
# //*[@id="root"]/div/div[2]/div/div/main/div[3]/div[2]/div[1]/ul/li[1]/div/div[1]/div[3]/div/a[2]/h2

#--------------------------------------------------------------------------------
## Unidad
# //*[@id="root"]/div/div[2]/div/div/main/div[3]/div[2]/div[1]/ul/li[1]/div/div[1]/div[3]/div/span

#--------------------------------------------------------------------------------
## Precio
# //*[@id="root"]/div/div[2]/div/div/main/div[3]/div[2]/div[1]/ul/li[2]/div/div[2]/div/span[1]

