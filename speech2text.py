import speech_recognition as sr
from pydub import silence
from pydub import AudioSegment

FOLDER_PATH = 'splitted/'

def menor_de_1min(rango):
    '''Determina si el rango es menor a 1 minuto'''
    return rango[1]-rango[0]<60000

def partir_en_menores_de_1min(segmento, rango_orig, sil_len):
    # riesgo de loop infinito si no hay silencio
    print('calculando rango: {0}'.format(rango_orig))
    l_rangos = list()
    sub_rangos = silence.detect_silence(segmento[rango_orig[0]:rango_orig[1]], min_silence_len=sil_len, silence_thresh=-20)
    for rango in sub_rangos:
        fixed_range = [rango_orig[0]+rango[0], rango_orig[0]+rango[1]]
        if (menor_de_1min(rango)):
            print('acepta rango {0}'.format(fixed_range))
            l_rangos.append(fixed_range)
        else:
            print('no acepta rango {0}'.format(fixed_range))
            l_rangos = l_rangos.__add__(partir_en_menores_de_1min(segmento, fixed_range, int(sil_len/2)))
    return l_rangos


def split_on_silence(wav_file_name):
    l_files= list()
    audioSegment = AudioSegment.from_wav(wav_file_name)
    rangos_sin_silencio = partir_en_menores_de_1min(audioSegment, [0, int(audioSegment.duration_seconds*1000)], 2000)
    for i, chunk in enumerate(rangos_sin_silencio):
        l_files.append('{0}splitted{1}.wav'.format(FOLDER_PATH, i))
        audioSegment[chunk[0]: chunk[1]].export(l_files[i], format='wav')
    return l_files


def transcribe_sounds(lista_archivos):
    r = sr.Recognizer()
    l_transcripto = list()
    for archivo in lista_archivos:
        with sr.AudioFile(archivo) as source:
            audio = r.record(source)
        try:
            l_transcripto.append(r.recognize_google(audio, language='es-MX'))
        except:
            print('problema en {0}'.format(archivo))
    return l_transcripto
