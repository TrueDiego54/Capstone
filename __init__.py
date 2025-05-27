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
import pymysql
#LIBRERIAS PARA LAS FUNCIONES MATEMATICAS
import math as m
#LIBRERIAS PARA LA LECTURA DE PDF
import PyPDF2
#LIBRERIAS PARA LA LECTURA DE LOS DICCIONARIOS
import sys



reload(sys)
print(sys.getdefaultencoding())
instanciaGPT = OpenAI(api_key='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')
conect= pymysql.connect(host='mysql-diegodev.alwaysdata.net',port=3306,user='diegodev',passwd='root9070',db='diegodev_2')
#conect= pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='prueba')
slctor = conect.cursor()
#EJECUTAMOS ESTE CODIGO CUANDO SE INGRESE A LA RUTA 
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
  
  mensaje=''
  pdf_lectura = PyPDF2.PdfReader(file)
  for texto in  pdf_lectura.pages:
    mensaje += texto.extract_text()
  print(mensaje)
  stream = instanciaGPT.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role":"system","content":"Eres un reclutador de TI"},
            {"role":"user","content":"el siguiente perfil para el sector de TI es apto para ti?"},
            {"role": "user","content":mensaje
            }],
  )
  return stream.choices[0].message



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
                ruta_subida = rut.join(ruta,nombre)
                file[index].save(ruta_subida)
                rpta = consulta(fil)
                aux1,aux2,rest,cantno,cantsi,cant = validaxionxentropia(rpta)
                respuestas.append(rest)
                os.remove(ruta_subida)
                print(cantno,cantsi,cant)
              else:
                return render_template('index.html',conf=True) 
    return render_template('index.html',conf1=True, respuestas= respuestas,entropia_acep=aux1,entropia_dene=aux2,cant_nega=cantno,cant_posi=cantsi,cant = cant)
      
def validaxionxentropia(rpta):
  rpta1 = rpta.content.split()
  print(rpta1)
  for g in rpta1:
    if g in dic_posi:
      slctor.execute("INSERT INTO entropia (APROV) VALUES (1)")
      result = True
      break
    if g in dic_nega:
      slctor.execute("INSERT INTO entropia (APROV) VALUES (0)")
      result = False
      break

  cntd= slctor.execute("select ID from entropia")
  c1 = slctor.execute("select APROV from entropia where APROV = 0")
  c2 = slctor.execute("select APROV from entropia where APROV = 1")
  inc1 = c1/cntd
  inc2 = c2/cntd
  if (c1!= 0 ):
    h1=inc1*m.log2(inc1)
  else:
    h1=0
  if (c2!= 0):
    h2=inc2*m.log2(inc2)
  else:
    h2=0
  return h1,h2,result,c1,c2,cntd

if __name__ == "__main__":
  app.run(debug=True)
