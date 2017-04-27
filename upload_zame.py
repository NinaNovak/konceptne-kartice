#ujemi napako IOError('File exists.') oziroma OSError: File exists.
#vrni 'Datoteka s tem imenom že obstaja. Ali jo želite zamenjati?'

from bottle import *
import os

############################## NALAGANJE NOVE KARTICE
@route('/nalozi_novo_kartico')
def upload():
    return template('upload')

@route('/nalozi_novo_kartico', method='POST')
def do_upload():
    nalozena_datoteka = request.files.get('upload')
    name, ext = os.path.splitext(nalozena_datoteka.filename)
    if ext != '.pdf':
        return 'Nedovoljena vrsta datoteke.\nDovoljena vrsta datoteke: PDF.'
    save_path = os.getcwd() + '/pdfkartice'
    ##kot za pdf naredi tudi za docx in ostale wordove koncnice
    ##zato, da se konceptno kartico lahko popravi/spremeni
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path,
                                       file=nalozena_datoteka.filename)
    nalozena_datoteka.save(file_path)
    return "Datoteka je bila uspešno shranjena v mapo '{0}'.".format(save_path)
############################## NALAGANJE NOVE KARTICE - KONEC


run(debug=True)
