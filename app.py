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
import json


reload(sys)
print(sys.getdefaultencoding())
instanciaGPT = OpenAI( api_key = os.getenv("GPT"))

#EJECUTAMOS ESTE CODIGO CUANDO SE INGRESE A LA RUTA 
def crear_app():

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
    prub=[]
    prub.append(1)
    return render_template('index.html',packjson=json.dumps(prub),packjson2=json.dumps(prub))
  @app.route("/resp/", methods=["POST", "GET"])



  def cv_envio():
      #SI HAY DATOS RECIBIDOS VIA GET
      if request.method == "POST":
          if(request.method=='POST'):
            if(request.files['cv[]']):
              file = request.files.getlist('cv[]')
              ruta = rut.dirname(__file__)
              nombres,respuestas,jason,jason2 = [],[],[],[]
              cantno_ttl,cantsi_ttl,cantacept,cantden=0,0,0,0
              for index,fil in enumerate(file):
                nombres.append(secure_filename(fil.filename))
                nombres[index] = "cvs/" + nombres[index]
                if(nombres[index].endswith('pdf')):
                    respuesta_cont = []
                    ruta_subida = rut.join(ruta,nombres[index])
                    file[index].save(ruta_subida)
                    rpta = consulta(fil)
                    aux1,aux2,rest,cantno,cantsi,cant,nom = validaxionxentropia(rpta)
                    if(rest):
                      cantacept+=1
                    else:
                      cantden+=1
                    cantno_ttl += cantno
                    cantsi_ttl += cantsi
                    respuesta_cont.append(aux1)
                    respuesta_cont.append(aux2)
                    respuesta_cont.append(rest)
                    respuesta_cont.append(cantno)
                    respuesta_cont.append(cantsi)
                    respuesta_cont.append(cant)
                    respuesta_cont.append(nom)
                    respuestas.append(respuesta_cont)
                    
                    os.remove(ruta_subida) 
                else:
                    return render_template('index.html',conf=True) 
      h1,h2=entropia(cantsi_ttl,cantno_ttl,cantsi_ttl+cantno_ttl)
      jason.append(h1)
      jason.append(h2)
      jason2.append(cantacept)
      jason2.append(cantden)
      return render_template('index.html',packjson2 = json.dumps(jason2),packjson = json.dumps(jason),conf1=True, respuestas= respuestas)
        

  def entropia(caso_1,caso_2,casos):
    inc1 = caso_1/casos
    inc2 = caso_2/casos
    if (caso_1!= 0 ):
      h1=(inc1*m.log2(inc1))*casos*-1
    else:
      h1=0
    if (caso_2!= 0 ):
      h2=(inc2*m.log2(inc2))*casos*-1
    else:
      h2=0
    return h1,h2  
  
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
        print(g)
        contador_pos+= 1
      aux_neg = dic_nega.count(g)
      contador_neg+= aux_neg
    for g in rpta2:
      if g in dic_posi:
        print(g)
        contador_pos+= 1
      aux_neg = dic_nega.count(g)
      contador_neg+= aux_neg
    for g in rpta3:
      if g in dic_posi:
        print(g)
        contador_pos+= 1
      aux_neg = dic_nega.count(g)
      contador_neg+= aux_neg
    
    h1,h2= entropia(contador_pos,contador_neg,contador_pos+contador_neg)

    if (h1<=h2):
      result = True
    else:
      result = False
    print(rpta[3].content)
    try:
      punto1 = rpta4.index('**Nombre:**')
    except:
      try:
        punto1 = rpta4.index('**Nombre**:')
      except:
        punto1=99
    try:
      tam1 = len('**Nombre:**')
      punto2 = rpta4.index('**Trabajo')
      tam2 = len('**Trabajo más relevante:**')
      punto3 = rpta4.index('**Experiencia')
      tam3 = len('**Experiencia más relevante:**')
      punto4 = rpta4.index('**Grado')
      tam4 = len('**Grado de educación:**')
    except:
      if(punto1==99):
        nombre = 'hubo un error al analizar el nombre'
      else:
        for i in range(punto2-(punto1+1)):
          nombre = nombre + rpta4[punto1+i+1]
          nombre += ' '
          print(nombre)
      return h1,h2,result,contador_neg,contador_pos,contador_pos+contador_neg,nombre
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
      experiencia += rpta4[punto3+i+2]

    for i in range(len(rpta4)-(punto4+3)):
      grado += rpta4[punto4+i+3]
      grado += ' '
    print('nombre: '+nombre,'\ntrabajo: '+trabajo,'\nnombre: '+experiencia,'\ngra: '+grado)
    return h1,h2,result,contador_neg,contador_pos,contador_pos+contador_neg,nombre
  return app
if __name__ == "__main__":
  app = crear_app()
  app.run(debug=True)
