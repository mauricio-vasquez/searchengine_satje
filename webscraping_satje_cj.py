# -*- coding: utf-8 -*-
"""
Web scraping SATJE - Consejo de la judicatura, Consulta de procesos (información judicial)
Por: Mauricio Vásquez
Proyecto solicitado por: Tax Legal (Paola Gachet, Paula Cabrera, Gina Cevallos)

Created on Tue Nov 15 15:26:38 2022

@author: vasquezm
"""

### 1. Importar librerías
## 1.1. Librerías del sistema
#import os
import datetime

## 1.2. librerías para webscraping
from time import sleep #tiempo de espera para scraping
#from random import randint # Crear un valor aleatorio, para usarlo junto con la función sleep
#import requests
#from bs4 import BeautifulSoup as bs
from helium import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



import html2text
import html_to_json


## Librerías para análisis de datos
# import numpy as np
#import pandas as pd


""" ### Identificación de elementos web ###

# Nota: se ha identificado que XPATHS pueden cambiar entre cada elemento

1. Búsqueda
# Campo buscar "DEMANDADO/PROCESADO", "Apellido(s)/Nombre(s)"
//*[@id="form1:txtDemandadoApellido"]

# Botón buscar: //*[@id="form1:butBuscarJuicios"]/span

2. Tabla primera capa:

# Texto: "Registros encontrados: ####"
//*[@id="form1:dataTableJuicios2:lbConteo"]

# Tabla entera: contenido
//*[@id="form1:dataTableJuicios2"]/div[2]

# Botones bajo columna "Detalle" (Abrir incidentes del proceso judicial No. XXX)
//*[@id="form1:dataTableJuicios2:0:btnAbrirMovimientos"] # botón registro  1
//*[@id="form1:dataTableJuicios2:1:btnAbrirMovimientos"] # botón registro 2
//*[@id="form1:dataTableJuicios2:25:btnAbrirMovimientos"] # botón registro 26


# Botones paginador: número de pagina
//*[@id="form1:dataTableJuicios2_paginator_bottom"]/span/a[1] # Boton pagina 1
//*[@id="form1:dataTableJuicios2_paginator_bottom"]/span/a[2] # Boton pagina 2

# Botones paginador: página siguiente
//*[@id="form1:dataTableJuicios2_paginator_bottom"]/a[3]


3. Tabla segunda capa:

# Tabla entera: Contenido
//*[@id="formJuicioDialogo:dataTableMovimiento_data"]    

# Botón "Actuaciones judiciales"
//*[@id="formJuicioDialogo:dataTableMovimiento:0:j_idt45:0:j_idt70"] # botón registro 1, linea 1 (único registro). Ref: Proceso 17230-2022-20265
//*[@id="formJuicioDialogo:dataTableMovimiento:0:j_idt45:0:j_idt70"] # botón registro 2, linea 1 (único registro). Ref: Proceso 17510-2022-00453	



## XPATHS
//*[@id="formJuicioDialogo:dataTableMovimiento:0:j_idt43:0:j_idt68"] # botón registro 92, linea 1. Ref: Proceso 01571-2022-02523
//*[@id="formJuicioDialogo:dataTableMovimiento:1:j_idt43:0:j_idt68"] # botón registro 92, linea 2. Ref: Proceso 01571-2022-02523
//*[@id="formJuicioDialogo:dataTableMovimiento:2:j_idt43:0:j_idt68"] # botón registro 92, linea 3. Ref: Proceso 01571-2022-02523


## Full XPATHS
/html/body/div[1]/div[4]/div/div/form[2]/div/div[2]/div[2]/table/tbody/tr/td/div/div/div/table/tbody/tr[2]/td[5]/div/button # botón registro 92, linea 1. Ref: Proceso 01571-2022-02523
/html/body/div[1]/div[4]/div/div/form[2]/div/div[2]/div[2]/table/tbody/tr/td/div/div/div/table/tbody/tr[4]/td[5]/div/button # botón registro 92, linea 2. Ref: Proceso 01571-2022-02523
/html/body/div[1]/div[4]/div/div/form[2]/div/div[2]/div[2]/table/tbody/tr/td/div/div/div/table/tbody/tr[6]/td[5]/div/button # botón registro 92, linea 3. Ref: Proceso 01571-2022-02523


4. Tercera capa

# Tabla completa (inclute Detall del proceso y Actuaciones judiciales)
//*[@id="formJuicioDetalle:juicioDetalleDetail"]

# Tabla "Detalle del proceso"
//*[@id="formJuicioDetalle:j_idt75"] # Tabla entera - XPATH

# Tabla entera "Detalle del proceso" - HTML
<div id="formJuicioDetalle:j_idt72" class="ui-panel ui-widget ui-widget-content ui-corner-all" data-widget="widget_formJuicioDetalle_j_idt72"><div id="formJuicioDetalle:j_idt72_content" class="ui-panel-content ui-widget-content"><table id="formJuicioDetalle:j_idt73" class="ui-panelgrid ui-widget" style=" margin-top:4px" role="grid"><tbody><tr class="ui-widget-content ui-panelgrid-even rowBorder" role="row"><td role="gridcell" class="ui-panelgrid-cell titulo"><label>No. proceso:</label></td><td role="gridcell" class="ui-panelgrid-cell descripcion">13802202200555 </td><td role="gridcell" class="ui-panelgrid-cell titulo"><label>No. de ingreso:</label></td><td role="gridcell" class="ui-panelgrid-cell descripcion">1</td>
									<td role="gridcell" class="ui-panelgrid-cell titulo"></td><td role="gridcell" class="ui-panelgrid-cell descripcion"></td></tr><tr class="ui-widget-content ui-panelgrid-odd rowBorder" role="row"><td role="gridcell" class="ui-panelgrid-cell titulo"><label>Dependencia jurisdiccional:</label></td><td role="gridcell" class="ui-panelgrid-cell descripcion">TRIBUNAL CONTENCIOSO ADMINISTRATIVO Y TRIBUTARIO CON SEDE EN EL CANTÓN PORTOVIEJO</td><td role="gridcell" class="ui-panelgrid-cell titulo"><label>Acción/Infracción:</label></td><td role="gridcell" class="ui-panelgrid-cell descripcion">CONTRA RESOLUCIONES</td>
									<td role="gridcell" class="ui-panelgrid-cell titulo"></td><td role="gridcell" class="ui-panelgrid-cell descripcion"></td></tr><tr class="ui-widget-content ui-panelgrid-even rowBorder" role="row"><td role="gridcell" class="ui-panelgrid-cell titulo"><label>Actor(es)/Ofendido(s):</label></td>
									<td role="gridcell" class="ui-panelgrid-cell descripcion"><div id="formJuicioDetalle:j_idt107" class="ui-scrollpanel ui-scrollpanel-native ui-widget ui-widget-content ui-corner-all" style="height:45px;"><div id="formJuicioDetalle:j_idt108" class="ui-datalist ui-widget"><div id="formJuicioDetalle:j_idt108_content" class="ui-datalist-content ui-widget-content"><dl id="formJuicioDetalle:j_idt108_list" class="ui-datalist-data"><dt class="ui-datalist-item">PROFISTEC CIA. LTDA.</dt></dl></div></div></div></td><td role="gridcell" class="ui-panelgrid-cell titulo"><label>Demandado(s)/Procesado(s):</label></td><td role="gridcell" class="ui-panelgrid-cell descripcion"><div id="formJuicioDetalle:j_idt114" class="ui-scrollpanel ui-scrollpanel-native ui-widget ui-widget-content ui-corner-all" style="height:45px"><div id="formJuicioDetalle:j_idt115" class="ui-datalist ui-widget"><div id="formJuicioDetalle:j_idt115_content" class="ui-datalist-content ui-widget-content"><dl id="formJuicioDetalle:j_idt115_list" class="ui-datalist-data"><dt class="ui-datalist-item">PROCURADURIA GENERAL DEL ESTADO</dt><dt class="ui-datalist-item">SERVICIO DE RENTAS INTERNAS</dt></dl></div></div></div></td></tr></tbody></table></div></div>


# Scroller
# juicioDetalleDialogo > div.ui-dialog-content.ui-widget-content # CSS selector
# //*[@id="juicioDetalleDialogo"]/div[2] # XPATH

# Campo "No. proceso:"
//*[@id="formJuicioDetalle:j_idt75"]/tbody/tr[1]/td[2] # XPATH
#formJuicioDetalle\:j_idt73 > tbody > tr:nth-child(1) > td:nth-child(2) #CSS Selector
<td role="gridcell" class="ui-panelgrid-cell descripcion">13802202200555 </td> #HTML


# Campo "Dependencia jurisdiccional:"
//*[@id="formJuicioDetalle:j_idt75"]/tbody/tr[2]/td[2]/text() # XPATH
#formJuicioDetalle\:j_idt75 > tbody > tr.ui-widget-content.ui-panelgrid-odd.rowBorder > td:nth-child(2) # CSS Selector


# Campo "Actor(es)/Ofendido(s):"
//*[@id="formJuicioDetalle:j_idt111_list"]/dt # XPATH
#formJuicioDetalle\:j_idt111_list > dt #CSS selector 
<dt class="ui-datalist-item">MILTON TARQUINO FARFAN FLORES</dt> # OuterHTML, proceso No. 01571202202523


# Campo "No. de ingreso:"
//*[@id="formJuicioDetalle:j_idt75"]/tbody/tr[1]/td[4]
#formJuicioDetalle\:j_idt75 > tbody > tr:nth-child(1) > td:nth-child(4) #CSS Selector


# Campo "Acción/Infracción:"
//*[@id="formJuicioDetalle:j_idt75"]/tbody/tr[2]/td[4]
#formJuicioDetalle\:j_idt75 > tbody > tr.ui-widget-content.ui-panelgrid-odd.rowBorder > td:nth-child(4) #CSS Selector


# Campo "Demandado(s)/Procesado(s):"
//*[@id="formJuicioDetalle:j_idt118_list"] # Nota: Es un listado de elementos, que contienen por separado los demandados

//*[@id="formJuicioDetalle:j_idt115_list"]/dt[1] # XPATH, elemento 1
#formJuicioDetalle\:j_idt115_list > dt:nth-child(1) # CSS selector, elemento 1
#formJuicioDetalle\:j_idt115_list > dt:nth-child(2) # CSS selector, elemento 2


# Tabla "Actuaciones judiciales" - tabla entera
//*[@id="formJuicioDetalle:dataTable_data"] # XPATH
formJuicioDetalle\:dataTable_data # Selector CSS

//*[@id="formJuicioDetalle:dataTable_data"]/tr[1] # XPATH, fila 1 de la lista


# Fechas de la actuación procesal
//*[@id="formJuicioDetalle:dataTable_data"]/tr[1]/td[1] # Fecha 1era linea (XPATH)
#formJuicioDetalle\:dataTable_data > tr > td:nth-child(1) # Fecha 1era linea (CSS Selector) 
<td role="gridcell" style="width:9%;text-align: center">21/11/2022 08:21</td> # HTML 1era linea

//*[@id="formJuicioDetalle:dataTable_data"]/tr[2]/td[1] # Fecha 2da linea (XPATH)

# Actuaciones judiciales

//*[@id="formJuicioDetalle:dataTable:0:j_idt129"] # XPATH, Actuacion judicial 1era línea
#formJuicioDetalle\:dataTable\:0\:j_idt129 # CSS Selector, Actuacion judicial 1era línea

//*[@id="formJuicioDetalle:dataTable:1:j_idt129"] # XPATH, Actuacion judicial 2da línea

## Actuaciones judiciales: Título actuación procesal (ejemplo:"ACTA DE SORTEO")
//*[@id="formJuicioDetalle:dataTable:0:j_idt129"]/legend # XPATH, primera línea
#formJuicioDetalle\:dataTable\:0\:j_idt129 > legend # CSS Selector, 1era línea

## Actuaciones judiciales: Contenido actuación procesal (En el ejemplo anterior, sería el contenido del "ACTA DE SORTEO")
//*[@id="formJuicioDetalle:dataTable:0:j_idt129"]/div/table/tbody/tr/td/span # XPATH, primera línea
#formJuicioDetalle\:dataTable\:0\:j_idt129 > div > table > tbody > tr > td > span # CSS Selector, primera línea

"""

### 2. Creación de bot para extracción de información ###

# 2.1. Iniciar Chrome y buscar las palabras "SERVICIO DE RENTAS INTERNAS" en campo demandado 
driver = start_chrome(headless=False) # Abre Google Chrome. Opción headless: En segundo plano
url ='http://consultas.funcionjudicial.gob.ec/informacionjudicial/public/informacion.jsf' # SATJE, Consulta de procesos del Consejo de la Judicatura
go_to(url) # Abre página del buscador de jurisprudencia de la CNJ
palabras_busq = 'SERVICIO DE RENTAS INTERNAS'
write(palabras_busq, into= S('//*[@id="form1:txtDemandadoApellido"]')) # Escribe la palabra en el buscador de la CNJ. Posteriormente, se debe incluir un prompt para input de usuario
click(S('//*[@id="form1:butBuscarJuicios"]/span')) # clic en el botón "Buscar"


# 2.2. Ingresar hasta tercera capa y extraer código HTML (sin iteración)

# 2.2.2. Previo a generar un loop para la segunda capa, se define una función para extraer datos de tercera capa

########### OJO: PENDIENTE CREAR LOOP DENTRO DE FUNCIÓN QUE ITERE SOBRE CADA PÁGINA DE TERCERA CAPA, EN CASO DE QUE EXISTA MÁS DE UNA ###########
# Se puede probar con condicional: si #formJuicioDetalle\:dataTable_paginator_bottom existe, entonces hacer loop, caso contrario no

def extraer_datos():
    "Extrae contenido de la tercera capa y lo guarda en un diccionario"
    
    # 2.2.3.1 Extraer datos del proceso (Detalle del Proceso)
    wait_until(S('tbody > tr:nth-child(1) > td:nth-child(2)').exists, timeout_secs=30, interval_secs = 1)
    num_proceso = driver.find_element_by_css_selector('tbody > tr:nth-child(1) > td:nth-child(2)').text
 
    wait_until(S('tbody > tr.ui-widget-content.ui-panelgrid-odd.rowBorder > td:nth-child(2)').exists, timeout_secs=30, interval_secs = 1) 
    dependencia_jurisdiccional = driver.find_element_by_css_selector('tbody > tr.ui-widget-content.ui-panelgrid-odd.rowBorder > td:nth-child(2)').text      
   
    wait_until(S('dt').exists, timeout_secs=30)
    actor_ofendido = driver.find_element_by_css_selector('dt').text
    
    wait_until(S('tbody > tr:nth-child(1) > td:nth-child(4)').exists, timeout_secs=30, interval_secs = 1)   
    num_ingreso = driver.find_element_by_css_selector('tbody > tr:nth-child(1) > td:nth-child(4)').text
    
    wait_until(S('tbody > tr.ui-widget-content.ui-panelgrid-odd.rowBorder > td:nth-child(4)').exists, timeout_secs=30, interval_secs = 1)   
    accion_infraccion = driver.find_element_by_css_selector('tbody > tr.ui-widget-content.ui-panelgrid-odd.rowBorder > td:nth-child(4)').text
    
    demandado_procesado = driver.find_elements_by_css_selector('dt')  #Encuentra todos los elementos web con etiqueta dt
    demandado_procesado = [item.text for item in demandado_procesado[1:len(demandado_procesado)]] # extrae texto de cada elemento web y lo pasa a una lista
    demandado_procesado = '; '.join(demandado_procesado) # Une todos los elementos en un solo texto, separando por punto y coma
    
    
    # 2.2.3.2 Extraer información de "Actuaciones judiciales" 
    
    # Extraer tipos de actuación procesal (Acta, razón, escrito, etc.)
    tipo_actuacion = driver.find_elements_by_css_selector('legend')
    tipo_actuacion = [item.text for item in tipo_actuacion]
    
    # Extraer fechas de actuación procesal
    
    fechas_actuaciones = driver.find_elements_by_xpath('//*[@id="formJuicioDetalle:dataTable_data"]/tr/td[1]')
    fechas_actuaciones = [item.text for item in fechas_actuaciones]
    
    ## Extraer informacion fila por fila, incluyendo fechas y texto
    filas_completas = driver.find_elements_by_xpath('//*[@id="formJuicioDetalle:dataTable_data"]/tr')
    filas_completas = [item.text for item in filas_completas]
    
    #Extraer texto y json de toda la página
    html = driver.page_source
    h = html2text.HTML2Text()
    h.ignore_links = True # Ignore converting links from HTML
    contenido = h.handle(html) # Nota: para mostrar en pantalla el texto legible, usar la función "print"
    #jsonhtml = html_to_json.convert(html)
    
    
    # Guardar sección  "Actuaciones judiciales" en un diccionario
    actuaciones_judiciales = {'Tipo_actuacion':tipo_actuacion,
                              'Fechas_actuaciones': fechas_actuaciones,
                              'Info_actuacion': filas_completas}
        
    ## # 2.2.3.3 Se guarda datos de todo el proceso en un diccionario
    proceso = {'No_proceso': num_proceso,
               'Dependencia_jurisdiccional': dependencia_jurisdiccional,
               'Actor_ofendido': actor_ofendido,
               'No_ingreso': num_ingreso,
               'Accion_infraccion': accion_infraccion,
               'Demandado_procesado': demandado_procesado,
               'Contenido': contenido,
               'Actuaciones_judiciales': actuaciones_judiciales,           
               'Fecha_extraccion': datetime.datetime.now().strftime('%c') }
    
    return proceso

#2.2.1. Clic en botones de primera capa
buttons1 = find_all(Button(below='Detalle')) # Botones primera capa, campo "Detalle"
click(buttons1[3])


#2.2.3. Loop de clics en botones de segunda capa

#def clicks_detalle_incidente():

#Definir elementos para cadena de acciones (ActionChain)
boton_cerrar3 = '//*[@id="formJuicioDetalle:btnCerrar"]/span' # XPATH Boton cerrar tercera capa

# Función para entrar a cada botón de segunda capa, extraer información de tercera capa, cerrar ventana tercera capa y luego iterar sobre cada botón segunda capa
resultados = []
buttons2 = find_all(Button("Ver Detalle del Incidente del Proceso Judicial", below='Actuaciones judiciales')) # Botones segunda capa, campo "Actuaciones judiciales"
for boton in range(len(buttons2)):
    #wait_until(Button("Ver Detalle del Incidente del Proceso Judicial").exists)
    wait_until(buttons2[boton].exists)
    #print(f'extrayendo información de boton No.: {boton}')
    click(buttons2[boton])
    sleep(0.6)
    cerrar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, boton_cerrar3)))
    action = ActionChains(driver)
    action.move_to_element(cerrar) 
    action.perform()
    action.reset_actions()
    proceso = extraer_datos()
    resultados.append(proceso)
    click(S(boton_cerrar3))
    sleep(0.3)




