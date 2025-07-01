#LIBRERIAS PARA FRAMEWORK WEB
from ast import Import
from importlib import reload
from operator import contains
from re import split
from xml.dom.minidom import Document
from flask import Flask, jsonify, request, render_template
#LIBRERIAS PARA OBTENCION DEL NOMBRE DEL ARCHIVO
from werkzeug.utils import secure_filename
#LIBRERIAS PARA EL USO DE CHATGPT
from openai import OpenAI
#LIBRERIAS PARA EL GUARDADO TEMPORAL DE ARCHIVOS
import os
from os import path as rut
from os import remove
#LIBRERIA PARA LA CONEXION BD
#LIBRERIAS PARA LAS FUNCIONES MATEMATICAS
import math as m
#LIBRERIAS PARA LA LECTURA DE PDF
import PyPDF2
#LIBRERIAS PARA LA LECTURA DE LOS DICCIONARIOS
import sys



reload(sys)
print(sys.getdefaultencoding())
instanciaGPT = OpenAI( api_key = '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')

#EJECUTAMOS ESTE CODIGO CUANDO SE INGRESE A LA RUTA 
def crear_app():
  #conect= pymysql.connect(host='mysql-diegodev.alwaysdata.net',port=3306,user='',passwd='',db='diegodev_2')
  #conect= pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='prueba')
  #slctor = conect.cursor()
  app = Flask(__name__,template_folder='html',)
  #INICIAMSO FLASK
  dic_nega,dic_posi = [],[]

  with open('positivo/positive-words.txt', newline='') as f:
    for page in f:
      page = page.replace('\n','')
      page = page.replace('\r','')

      dic_posi.append(page)

  with open('negativo/Palabras-Negativas.txt', newline='') as f:
    for page in f:
      page = page.replace('\n','')
      page = page.replace('\r','')

      dic_nega.append(page)

  def consulta(file):
    respuestas = []
    mensaje=''
    pdf_lectura = PyPDF2.PdfReader(file)
    for texto in  pdf_lectura.pages:
      mensaje += texto.extract_text()
    stream1 = instanciaGPT.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"system","content":"Eres un reclutador de TI"},
              {"role":"user","content":"el siguiente perfil es apto para el sector de TI para ti?"},
              {"role": "user","content":mensaje
              }],
    )
    respuestas.append(stream1.choices[0].message)
    stream2 = instanciaGPT.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"system","content":"Eres un reclutador de recursos humanos"},
              {"role":"user","content":"el siguiente perfil es apto para el sector de TI para ti?"},
              {"role": "user","content":mensaje
              }],
    )
    respuestas.append(stream2.choices[0].message)
    stream3 = instanciaGPT.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"system","content":"Eres un Ingenierio de sistemas Senior"},
              {"role":"user","content":"que te aprece el siguiente perfil para el sector de TI?"},
              {"role": "user","content":mensaje
              }],
    )
    respuestas.append(stream3.choices[0].message)
    stream4 = instanciaGPT.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"system","content":"Eres un asistente de datos"},
              {"role":"user","content":"separa los datos del siguiente curriculum y dame los siguientes datso: Nombre, Trabajo mas relevante, Experiencia mas relevante y Grado de educacion"},
              {"role": "user","content":mensaje
              }],
    )
    respuestas.append(stream4.choices[0].message)
    return respuestas



  @app.route("/", methods=["POST", "GET"])
  def root():
    return render_template('index.html')
  @app.route("/resp/", methods=["POST", "GET"])



  def cv_envio():
      #SI HAY DATOS RECIBIDOS VIA GET
      if request.method == "POST":
          if(request.method=='POST'):
            if(request.files['cv[]']):
              file = request.files.getlist('cv[]')
              ruta = rut.dirname(__file__)
              nombres,respuestas = [],[]
              
              for index,fil in enumerate(file):
                nombres.append(secure_filename(fil.filename))
                nombres[index] = "cvs/" + nombres[index]
              for index,nombre in enumerate(nombres):
                if(nombre.endswith('pdf')):
                  respuesta_cont = []
                  ruta_subida = rut.join(ruta,nombre)
                  file[index].save(ruta_subida)
                  rpta = consulta(fil)
                  aux1,aux2,rest,cantno,cantsi,cant = validaxionxentropia(rpta)
                  
                  respuesta_cont.append(aux1)
                  respuesta_cont.append(aux2)
                  respuesta_cont.append(rest)
                  respuesta_cont.append(cantno)
                  respuesta_cont.append(cantsi)
                  respuesta_cont.append(cant)
                  respuestas.append(respuesta_cont)
                  os.remove(ruta_subida)
                  print(cantno,cantsi,cant)
                  print(respuestas)
                else:
                  return render_template('index.html',conf=True) 
      return render_template('index.html',conf1=True, respuestas= respuestas,entropia_acep=aux1,entropia_dene=aux2,cant_nega=cantno,cant_posi=cantsi,cant = cant)
        
  def validaxionxentropia(rpta):
    rpta1 = rpta[0].content.split()
    rpta2 = rpta[1].content.split()
    rpta3 = rpta[2].content.split()
    rpta4 = rpta[3].content.split()
    contador_pos = 0
    contador_neg = 0
    print(rpta1)
    for g in rpta1:
      if g in dic_posi:
        contador_pos+= 1
      if g in dic_nega:
        contador_neg+= 1
    for g in rpta2:
      if g in dic_posi:
        contador_pos+= 1
      if g in dic_nega:
        contador_neg+= 1
    for g in rpta3:
      if g in dic_posi:
        contador_pos+= 1
      if g in dic_nega:
        contador_neg+= 1
    
    print(rpta4)
    cntd= contador_neg+contador_pos 
    inc1 = contador_pos/cntd
    inc2 = contador_neg/cntd
    if (contador_pos!= 0 ):
      h1=(inc1*m.log2(inc1))*cntd*-1
    else:
      h1=0
    if (contador_neg!= 0 ):
      h2=(inc2*m.log2(inc2))*cntd*-1
    else:
      h2=0
    if (h1<=h2):
      result = True
    else:
      result = False
    print(rpta[3].content)
    try:
      punto1 = rpta4.index('**Nombre:**')
    except:
      punto1 = rpta4.index('**Nombre**:')
    tam1 = len('**Nombre:**')
    punto2 = rpta4.index('**Trabajo')
    tam2 = len('**Trabajo más relevante:**')
    punto3 = rpta4.index('**Experiencia')
    tam3 = len('**Experiencia más relevante:**')
    punto4 = rpta4.index('**Grado')
    tam4 = len('**Grado de educación:**')
    nombre=''
    trabajo=''
    experiencia=''
    grado=''
    for i in range(punto2-(punto1+1)):
      nombre = nombre + rpta4[punto1+i+1]
      nombre += ' '
      print(nombre)
    for i in range(punto3-(punto2+3)):
      trabajo += rpta4[punto2+i+3]
    for i in range(punto4-punto3+3):
      experiencia += rpta4[punto3+i+3]

    for i in range(len(rpta4)-(punto4+3)):
      grado += rpta4[punto4+i+3]
      grado += ' '
    print('nombre: '+nombre,'\ntrabajo: '+trabajo,'\nnombre: '+experiencia,'\ngra: '+grado)
    return h1,h2,result,contador_neg,contador_pos,cntd
  return app
if __name__ == "__main__":
  app = crear_app()
  app.run(debug=True)
