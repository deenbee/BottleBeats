from email.policy import default
from tkinter import NO
from turtle import color
import pygame
#import #wiringpi
import os
from multiprocessing import parent_process
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import fftconvolve
from collections import deque

class Ver_info:

    def __init__(self):
        self.ver_ = "0.2.3 Beta"
        self.last_update = "28 Mar 2025"
        self.author = "Danubio Rodriguez"
        self.color = (255, 255, 255)

    def mostrar_version_(self, x, y):
        self.ver_txt = font.render(f"Version: {self.ver_}", True, self.color)
        screen.blit(self.ver_txt, (x, y))

        self.last_txt = font.render(f"Last update {self.last_update}", True, self.color)
        screen.blit(self.last_txt, (x , y + 20))

        self.by_txt = font.render(f"Developer: {self.author}", True, self.color)
        screen.blit(self.by_txt, (x , y + 40))

        self.text1 = font_bold.render("Special thanks to: ", True, self.color)
        self.text2 = font.render("Danubio R: https://github.com/deenbee", True, self.color)
        self.text3 = font.render("Pygame: https://www.pygame.org", True, self.color)
        self.text4 = font.render("Sound-Device: https://github.com/spatialaudio/python-sounddevice/", True, self.color)
        self.text5 = font.render("Grok3 and Chat-Gpt", True, self.color)

        screen.blit(self.text1, (x , y + 220))
        screen.blit(self.text2, (x , y + 250))
        screen.blit(self.text3, (x , y + 270))
        screen.blit(self.text4, (x , y + 290))
        screen.blit(self.text5, (x , y + 310))

        pic = pygame.image.load("bottlebeats.png")
        pic_rec = pic.get_rect(center=(x + 360, y + 150))
        screen.blit(pic, pic_rec)

    
    def logo_escalado(self, pos_x, pos_y, size_x, size_y):
        
        self.pic = pygame.image.load("bottlebeats.png")
        self.pic_scale = pygame.transform.scale(self.pic, (size_x, size_y))  # Se pasa como tupla
        self.pic_rec = self.pic_scale.get_rect(center=(pos_x, pos_y))  # Se usa pic_scale en lugar de pic
        screen.blit(self.pic_scale, self.pic_rec)


ver = Ver_info()

class Samples_banks:
    
    def __init__(self):
                   
        # Ajustar base_path para apuntar al directorio raíz del proyecto
        #base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # Lista de archivos WAV
        self.wav_files = [
            "samples/808/Kick Basic.wav",
            "samples/808/Kick Long.wav",
            "samples/808/Kick Mid.wav",
            "samples/808/Kick Short.wav",
            "samples/808/Snare Mid.wav",
            "samples/808/Snare Low.wav",
            "samples/808/Snare High.wav",
            "samples/808/Snare Bright.wav",
            "samples/808/Rimshot.wav",
            "samples/808/Open Hat Short.wav",
            "samples/808/Open Hat Long.wav",
            "samples/808/Hihat.wav",
            "samples/808/Cymbal.wav",
            "samples/808/Cowbell.wav",
            "samples/808/Clap.wav",
            "samples/808/Conga Mid.wav",
            "samples/808/Conga Low.wav",
            "samples/808/Conga High.wav",
            "samples/808/Claves.wav",
            "samples/808/Maracas.wav",
            "samples/808/Tom Mid.wav",
            "samples/808/Tom Low.wav",
            "samples/808/Tom High.wav",
            "samples/808/808.wav",
            "samples/custom/ah.wav",
            "samples/custom/kinder.wav",
            "samples/custom/planet.wav",
            "samples/custom/bass1.wav",
            "samples/custom/bass2.wav",
            "samples/custom/bass3.wav",
        ]

        self.T909 = [
            "samples/909/bd01.wav",
            "samples/909/bd02.wav",
            "samples/909/bd03.wav",
            "samples/909/bd04.wav",
            "samples/909/bd05.wav",
            "samples/909/bd06.wav",
            "samples/909/cp01.wav",
            "samples/909/cr01.wav",
            "samples/909/cp02.wav",
            "samples/909/cr02.wav",
            "samples/909/rd01.wav",
            "samples/909/rs01.wav",
            "samples/909/hh01.wav",
            "samples/909/rs02.wav",
            "samples/909/rd03.wav",
            "samples/909/hh02.wav",
            "samples/909/rd04.wav",
            "samples/909/mt03.wav",
            "samples/909/sd01.wav",
            "samples/909/oh01.wav",
            "samples/909/sd02.wav",
            "samples/909/oh02.wav",
            "samples/909/mt01.wav",
            "samples/909/mt02.wav",
            "samples/custom/ah.wav",
            "samples/custom/kinder.wav",
            "samples/custom/planet.wav",
            "samples/custom/bass1.wav",
            "samples/custom/bass2.wav",
            "samples/custom/bass3.wav",
        ]

        self.C64 = [
            "samples/c64/kick1.wav",
            "samples/c64/clap.wav",
            "samples/c64/kick2.wav",
            "samples/c64/cowbell.wav",
            "samples/c64/kick3.wav",
            "samples/c64/hihat1.wav",
            "samples/c64/kick4.wav",
            "samples/c64/hihat2.wav",
            "samples/c64/kick5.wav",
            "samples/c64/snare1.wav",
            "samples/c64/kick6.wav",
            "samples/c64/snare2.wav",
            "samples/c64/kick7.wav",
            "samples/c64/snare3.wav",
            "samples/c64/kick8.wav",
            "samples/c64/snare4.wav",
            "samples/808/Tom High.wav",
            "samples/c64/snare6.wav",
            "samples/808/Conga Low.wav",
            "samples/c64/snare7.wav",
            "samples/808/Hihat.wav",
            "samples/c64/snare8.wav",
            "samples/c64/tom1.wav",
            "samples/c64/tom2.wav",
            "samples/custom/ah.wav",
            "samples/custom/kinder.wav",
            "samples/custom/planet.wav",
            "samples/custom/bass1.wav",
            "samples/custom/bass2.wav",
            "samples/custom/bass3.wav",
        ]


Samples = Samples_banks()


    


class Color:
    g = (150, 150, 150)
    r = (255, 0, 0) 
    w = (255, 255, 255)
    bg = (0, 0, 0)
    gn = (0, 0, 0)

class Main_patterns:

    def __init__(self):
        self.largo = len(Samples.wav_files)
        self.mtx_p = [[[0] * 16 for _ in range(self.largo)] for _ in range(32)]  # Matrix de 32 patterns
       
    
    

Patt = Main_patterns()



# Configuración del secuenciador
class Sequence:

    def __init__(self):
        
        # Diccionario de notas musicales con octavas
        # Factores relativos a C (1.0 = C de la octava base)
        self.NOTAS = {
            # Octava -1 (una octava abajo)
            "C-1": 0.5,         # Do
            "C#-1": 0.529732,   # Do sostenido
            "D-1": 0.561231,    # Re
            "D#-1": 0.594604,   # Re sostenido
            "E-1": 0.629961,    # Mi
            "F-1": 0.667420,    # Fa
            "F#-1": 0.707107,   # Fa sostenido
            "G-1": 0.749154,    # Sol
            "G#-1": 0.793701,   # Sol sostenido
            "A-1": 0.840896,    # La
            "A#-1": 0.890899,   # La sostenido
            "B-1": 0.943874,    # Si
            
            # Octava 0 (base)
            "C": 1.0,           # Do
            "C#": 1.059463,     # Do sostenido
            "D": 1.122462,      # Re
            "D#": 1.189207,     # Re sostenido
            "E": 1.259921,      # Mi
            "F": 1.334840,      # Fa
            "F#": 1.414214,     # Fa sostenido
            "G": 1.498307,      # Sol
            "G#": 1.587401,     # Sol sostenido
            "A": 1.681793,      # La
            "A#": 1.781797,     # La sostenido
            "B": 1.887749,      # Si
            
            # Octava +1 (una octava arriba)
            "C+1": 2.0,         # Do
            "C#+1": 2.118926,   # Do sostenido
            "D+1": 2.244924,    # Re
            "D#+1": 2.378414,   # Re sostenido
            "E+1": 2.519842,    # Mi
            "F+1": 2.669680,    # Fa
            "F#+1": 2.828428,   # Fa sostenido
            "G+1": 2.996614,    # Sol
            "G#+1": 3.174802,   # Sol sostenido
            "A+1": 3.363586,    # La
            "A#+1": 3.563594,   # La sostenido
            "B+1": 3.775498    # Si
        }

        self.current_note = ["C"] * 4  # Nota inicial (octava base)
        self.note_index = [12] * 4    # Índice inicial (C en octava 0)
        self.notes_list = list(self.NOTAS.keys())  # Lista ordenada de notas (Comun a las 4)
        
        # Le agregamos 6 porque tiene 2 sonidos adicionales en total 30 len(Samples.wav_files)
        self.sq2_note = [[[1] * 16 for _ in range(6)] for _ in range(32)] # Almacena las notas de los (4 canales Secuenciador 2)

        self.txt2_note = [[["C"] * 16 for _ in range(6)] for _ in range(32)] # Almacena las notas de los (4 canales Secuenciador 2)
        
        self.largo = len(Samples.wav_files)
        self.tempo = 100
        self.tpo_txt = str(self.tempo)  # tempo_text
        self.m_vol = 1.0           # master_volume: Volumen master
        self.m_opn = False # menu_open
        self.playing = False
        self.lstime = 0 # last_step_time
        self.s_idx = 0 # step_index
        self.tpt = 1    # total_patt : Total numbers of patterns (máximo 32)
        self.apt = 1   # Active Song position (VARIABLE PRINCIPAL)
        self.act_chs = {} # Active channels
        self.s_mem = 1 # Selected_memory

        self.channel_volumes = [1.0] * self.largo  # Volumen por canal (0.0 a 1.0)
        self.pan_volumes = [0.0] * self.largo      # Panorama por canal (-1.0 a 1.0)
        self.tones = [1.0] * self.largo

        self.pattern_num = 1             # Pattern seleccionada por los numeros del 1 al 32
        self.patt_state = [1] * 32       # Segun la posicion de la cancion (variable apt), se inician todos en 1 porque no puede haber 0
        self.patt = 1                    # Pattern actual de 1 a 32

        self.pulsador_stop = False

    def obtener_nombre_nota(self, valor):
        for nota, indice in self.NOTAS.items():
            if valor == indice:
                return nota
        return "Nota no encontrada"


    def bajar_semitono(self, channel):
        # Subir un semitono
        if self.note_index[channel] < len(self.notes_list) - 1:
            self.note_index[channel] += 1
            self.current_note[channel] = self.notes_list[self.note_index[channel]]
        
        return self.current_note[channel]

    def subir_semitono(self, channel):
        # Bajar un semitono
        if self.note_index[channel] > 0:
            self.note_index[channel] -= 1
            self.current_note[channel] = self.notes_list[self.note_index[channel]]

        return self.current_note[channel]

    def bajar_octava(self, channel):
        # Subir una octava completa (12 semitonos)
        if self.note_index[channel] + 12 < len(self.notes_list):
            self.note_index[channel] += 12
            self.current_note[channel] = self.notes_list[self.note_index[channel]]

    def subir_octava(self, channel):
        # Bajar una octava completa (12 semitonos)
        if self.note_index[channel] - 12 >= 0:
            self.note_index[channel] -= 12
            self.current_note[channel] = self.notes_list[self.note_index[channel]]

    def get_factor(self, channel):
        # Obtener el factor de tono actual
        return Seq.NOTAS[self.current_note[channel]]    


Seq = Sequence() # Crear el objeto Seq



# Inicializar Pygame y #wiringpi
pygame.init()


#pygame.mixer.set_num_channels(24)
#wiringpi.#wiringpiSetup()

# Configuración de la ventana
WINDOW_WIDTH = 830
WINDOW_HEIGHT = 850

# Configurar ventana
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(f"Bottle Beats {ver.ver_} by {ver.author}")

# Cargar el ícono
icono = pygame.image.load("bottlebeats.png")
pygame.display.set_icon(icono)


# Fuentes
font = pygame.font.SysFont("Arial", 16)
font_small = pygame.font.SysFont("Arial", 12)

font_bold = pygame.font.SysFont("Arial", 18)
font_bold.set_bold(True)


# Pines GPIO para 24 LEDs
led_pins = [0, 7, 14, 15, 9, 6, 12, 10, 8, 4, 11, 2] * 2
#for pin in led_pins:
    #wiringpi.pinMode(pin, 1)


class Tabs:

    def __init__(self):

        self.confirm_close = False  # Confirma si quiere salir de la aplicacion 
        self.mixer = False
        self.settings = False       # Activa pestaña Settings
        self.sequencer_1 = True
        self.sequencer_2 = False    # Activa para mostrar el segundo secuenciador
        self.about = False          # Activa la pestaña about


        self.BTN_MIXER = pygame.Rect(690, 490, 120, 25)
        self.BTN_SQ_1 = pygame.Rect(690, 520, 120, 25)
        self.BTN_SQ_2 = pygame.Rect(690, 550, 120, 25)
        
        self.BTN_ABOUT = pygame.Rect(690, 30, 120, 25)
        self.BTN_SET = pygame.Rect(690, 60, 120, 25)

        self.LED = pygame.Rect(812, 520, 6, 25)
    
        self.btn_color = (30, 30, 30)
        self.text_color  = (255, 255, 255)

        self.led_on_color = (255, 0, 0)


    def draw(self):
        
        pygame.draw.rect(screen, self.btn_color, self.BTN_MIXER)
        pygame.draw.rect(screen, self.btn_color, self.BTN_SQ_1)
        pygame.draw.rect(screen, self.btn_color, self.BTN_SQ_2)
        pygame.draw.rect(screen, self.btn_color, self.BTN_SET)
        pygame.draw.rect(screen, self.btn_color, self.BTN_ABOUT)
        
        pygame.draw.rect(screen, self.led_on_color, self.LED)

    def text(self):

        self.mixer_text = font_bold.render("Mixer", True, self.text_color)
        self.seq_1_text = font_bold.render("Sequencer 1", True, self.text_color)
        self.seq_2_text = font_bold.render("Sequencer 2", True, self.text_color)
        self.sett_text = font_bold.render("Options", True, self.text_color)
        self.about_text = font_bold.render("About", True, self.text_color)

    def show(self):
        
        screen.blit(self.mixer_text, (self.BTN_MIXER.x + 10, self.BTN_MIXER.y + 2))
        screen.blit(self.seq_1_text, (self.BTN_SQ_1.x + 10, self.BTN_SQ_1.y + 2))
        screen.blit(self.seq_2_text, (self.BTN_SQ_2.x + 10, self.BTN_SQ_2.y + 2))

        screen.blit(self.sett_text, (self.BTN_SET.x + 10, self. BTN_SET.y + 2))
        screen.blit(self.about_text, (self.BTN_ABOUT.x + 10, self.BTN_ABOUT.y + 2))

    def confirm_clse(self):
        Seq.playing = False
        Seq.pulsador_stop = True
        Botones.write_mode = False               # Quita el modo de escritura
        Botones.color_write = Botones.off_color     # Quita el color de escritura
        Seq.s_idx = 0
        self.confirm_close = True
        self.about = False
        self.sequencer_1 = False
        self.sequencer_2 = False
        self.mixer = False
        self.settings = False
        
        
    def close(self, pos, running):
        
        if Botones.BTN_CLOSE_NO.collidepoint(pos) and self.confirm_close == True:
            self.confirm_close = False
            return running
        if Botones.BTN_CLOSE_YES.collidepoint(pos) and self.confirm_close == True:
            return False
        return running
    
    def tab_selection(self):
        if self.sequencer_1 == True:
            self.LED = pygame.Rect(812, self.BTN_SQ_1.y, 6, 25)
        if self.sequencer_2 == True:
            self.LED = pygame.Rect(812, self.BTN_SQ_2.y, 6, 25)
        if self.settings == True:
            self.LED = pygame.Rect(812, self.BTN_SET.y, 6, 25)
        if self.about == True:
            self.LED = pygame.Rect(812, self.BTN_ABOUT.y, 6, 25)
        if self.mixer == True:
            self.LED = pygame.Rect(812, self.BTN_MIXER.y, 6, 25)      

    
    def tab_buttons_actions(self, pos):
        if self.BTN_ABOUT.collidepoint(pos):
            self.about = True
            self.settings = False
            self.sequencer_1 = False
            self.sequencer_2 = False
            self.mixer = False

        if self.BTN_SET.collidepoint(pos):
            self.about = False
            self.settings = True
            self.sequencer_1 = False
            self.sequencer_2 = False
            self.mixer = False

        if self.BTN_MIXER.collidepoint(pos):
            self.about = False
            self.settings = False
            self.sequencer_1 = False
            self.sequencer_2 = False
            self.mixer = True

        if self.BTN_SQ_1.collidepoint(pos):
            self.about = False
            self.settings = False
            self.sequencer_1 = True
            self.sequencer_2 = False
            self.mixer = False

        if self.BTN_SQ_2.collidepoint(pos):
            self.about = False
            self.settings = False
            self.sequencer_1 = False
            self.sequencer_2 = True
            self.mixer = False        


Pestania = Tabs() # Make tabs object
    


class Sonido:
  
    def __init__(self):
        self.largo = len(Samples.wav_files)
        self.volumenes = [1.0] * self.largo
        self.pan = [0.0] * self.largo
        self.audio = [None] * self.largo
        self.samplerate = [None] * self.largo
        self.factor_tono = [1.0] * self.largo
        self.audio_pitch = [None] * self.largo
        self.audio_stereo = [None] * self.largo
        self.active_sounds = []  # Lista de sonidos activos: (audio, samplerate, frame_pos)
             
        self.bank = 0
        self.load_samples_banks(self.bank) # Carga los bancos de sonidos

        
        # Configurar dispositivo de audio
        self.devices = sd.query_devices()  # Guardar lista de dispositivos
        sd.default.device = [None, None]  # [entrada, salida], solo salida en 19
        sd.default.latency = 'low'
        sd.default.samplerate = 44100
        self.blocksize = 512  # Valor inicial del buffer

        self.default_device = sd.default.device
        print("Dispositivo de audio seleccionado por default ", sd.default.device)

        # Intentar iniciar el stream (aquí manejamos errores de la tarjeta)
        try:
            self.stream = sd.OutputStream(
                samplerate=44100,
                channels=2,
                callback=self.callback,
                blocksize=self.blocksize,
                latency='low'
            )
            self.stream.start()
            print("Stream de audio iniciado con latencia mínima.")
        except Exception as e:
            print(f"Error iniciando tarjeta de sonido: {e}")
            Pestania.settings = True  # Abrir pestaña de configuración
            Pestania.sequencer_1 = False
            Pestania.sequencer_2 = False
            Pestania.about = False
            Pestania.mixer = False
            Pestania.confirm_close = False
            self.stream = None  # Marcar que no hay stream activo

    def update_audio_device(self, device_idx, blocksize):
        if hasattr(self, 'stream') and self.stream is not None:
            self.stream.stop()
            self.stream.close()

        sd.default.device = [None, device_idx]  # Forzar [entrada=None, salida=device_idx]
        self.blocksize = blocksize
        self.default_device = sd.default.device

        try:
            self.stream = sd.OutputStream(
                samplerate=44100,
                channels=2,
                callback=self.callback,
                blocksize=self.blocksize,
                latency='low'
            )
            self.stream.start()
            print(f"Stream actualizado: Device {device_idx}, Blocksize {blocksize}")
            return True
        except Exception as e:
            print(f"Error actualizando tarjeta de sonido: {e}")
            self.stream = None
            return False
    
    
    def load_samples_banks(self, b_selected):
        # Cargar y preprocesar sonidos
        if b_selected == 0:
            samples_files = Samples.wav_files       # Elije la lista de wavs
            self.bank = 0                           # Asigna el numero actual de banco seleccionado
        elif b_selected == 1:
            samples_files = Samples.T909
            self.bank = 1
        elif b_selected == 2:
            samples_files = Samples.C64
            self.bank = 2
        else: # Valores por default sino encuentra ningun numero
            samples_files = Samples.wav_files
            self.bank = 0    
        
        largo = len(Samples.wav_files)

        for i in range(largo):
            try:
                self.audio[i], self.samplerate[i] = sf.read(samples_files[i])

                if len(self.audio[i].shape) > 1 and self.audio[i].shape[1] == 2:
                    # Procesar cada canal por separado para preservar estéreo
                    left_channel = self.cambiar_tono(self.audio[i][:, 0], self.factor_tono[i])
                    right_channel = self.cambiar_tono(self.audio[i][:, 1], self.factor_tono[i])
                    self.audio_pitch[i] = np.column_stack((left_channel, right_channel))
                else:
                    # Si es mono, procesar normalmente
                    self.audio_pitch[i] = self.cambiar_tono(self.audio[i], self.factor_tono[i])

                self.audio_pitch[i] *= self.volumenes[i]
                left_gain = np.clip(1.0 - self.pan[i], 0, 1)
                right_gain = np.clip(1.0 + self.pan[i], 0, 1)
                self.audio_stereo[i] = np.column_stack((self.audio_pitch[i][:, 0] * left_gain, self.audio_pitch[i][:, 1] * right_gain)) if len(self.audio_pitch[i].shape) > 1 else np.column_stack((self.audio_pitch[i] * left_gain, self.audio_pitch[i] * right_gain))
            except Exception as e:
                print(f"Error cargando {Samples.wav_files[i]}: {e}")
        
        """
        for i in range(largo):
            try:
                self.audio[i], self.samplerate[i] = sf.read(samples_files[i])

                if len(self.audio[i].shape) > 1 and self.audio[i].shape[1] == 2:
                    self.audio[i] = self.audio[i].mean(axis=1)
                    self.audio_pitch[i] = self.cambiar_tono(self.audio[i], self.factor_tono[i])
                    self.audio_pitch[i] *= self.volumenes[i]
                    left_gain = np.clip(1.0 - self.pan[i], 0, 1)
                    right_gain = np.clip(1.0 + self.pan[i], 0, 1)
                    self.audio_stereo[i] = np.column_stack((self.audio_pitch[i] * left_gain, self.audio_pitch[i] * right_gain))
            except Exception as e:
                    print(f"Error cargando {Samples.wav_files[i]}: {e}")"""


    def callback(self, outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = 0
        sounds_to_remove = []
        for i, (audio, samplerate, frame_pos) in enumerate(self.active_sounds):
            remaining_frames = len(audio) - frame_pos
            if remaining_frames <= 0:
                sounds_to_remove.append(i)
                continue
            chunk = audio[frame_pos:frame_pos + frames]
            if len(chunk) < frames:
                chunk = np.pad(chunk, ((0, frames - len(chunk)), (0, 0)), mode='constant')
            outdata[:] += chunk
            self.active_sounds[i] = (audio, samplerate, frame_pos + frames)
        for i in sorted(sounds_to_remove, reverse=True):
            self.active_sounds.pop(i)
        # Normalizar para evitar clipping
        if np.max(np.abs(outdata)) > 1.0:
            outdata[:] = outdata / np.max(np.abs(outdata))

    def stop(self):
        self.active_sounds.clear()
        print("Reproducción detenida.")


    """
    def cambiar_tono(self, data, factor):
        indices = np.arange(0, len(data), 1 / factor)
        indices = np.clip(indices, 0, len(data) - 1)
        return np.interp(indices, np.arange(len(data)), data)"""
    
    def cambiar_tono(self, data, factor):
        indices = np.arange(0, len(data), 1 / factor)
        indices = np.clip(indices, 0, len(data) - 1)
        if len(data.shape) > 1 and data.shape[1] == 2:  # Si es estéreo
            left_channel = np.interp(indices, np.arange(len(data)), data[:, 0])
            right_channel = np.interp(indices, np.arange(len(data)), data[:, 1])
            return np.column_stack((left_channel, right_channel))
        else:  # Si es mono
            return np.interp(indices, np.arange(len(data)), data)

    """
    def ply(self, channel_index, tono=1.0, vol=1.0, pan=0.0):
        
        #Reproduce un sonido con tono, volumen y paneo ajustables en tiempo real.
        #pan: -1.0 (izquierda), 0.0 (centro), 1.0 (derecha)
        
        if self.audio[channel_index] is not None:
            # Aplicar tono en tiempo real
            audio_tono = self.cambiar_tono(self.audio[channel_index], tono)
            audio_tono *= vol
            # Calcular ganancias para paneo con un solo parámetro
            left_gain = np.clip(1.0 - pan, 0, 1)  # 1.0 en pan=-1.0, 0.0 en pan=1.0
            right_gain = np.clip(1.0 + pan, 0, 1)  # 0.0 en pan=-1.0, 1.0 en pan=1.0
            audio_stereo = np.column_stack((audio_tono * left_gain, audio_tono * right_gain))
            self.active_sounds.append((audio_stereo, self.samplerate[channel_index], 0))
            print(f"Sonido del canal {channel_index} disparado con tono {tono} y paneo {pan}.")
        else:
            print(f"Error: No hay audio en el canal {channel_index}.")"""
    
    def ply(self, channel_index, tono=1.0, vol=1.0, pan=0.0):
        if self.audio[channel_index] is not None:
            # Aplicar tono en tiempo real
            audio_tono = self.cambiar_tono(self.audio[channel_index], tono)
            # Aplicar volumen
            audio_tono *= vol
            # Calcular ganancias para paneo
            left_gain = np.clip(1.0 - pan, 0, 1)
            right_gain = np.clip(1.0 + pan, 0, 1)
            if len(audio_tono.shape) > 1 and audio_tono.shape[1] == 2:
                audio_stereo = np.column_stack((audio_tono[:, 0] * left_gain, audio_tono[:, 1] * right_gain))
            else:
                audio_stereo = np.column_stack((audio_tono * left_gain, audio_tono * right_gain))
            self.active_sounds.append((audio_stereo, self.samplerate[channel_index], 0))
            #print(f"Sonido del canal {channel_index} disparado con tono {tono} y paneo {pan}.")
        else:
            print(f"Error: No hay audio en el canal {channel_index}.")

    def play_on_pattern(self, channel_idx, pattern, step, pattern_values):
        if pattern == 1 and step < len(pattern_values) and pattern_values[step] == 1:
            self.ply(channel_idx)  # Usar tono por defecto, ajustable si querés
        else:
            print(f"Pattern {pattern}, step {step}, valor {pattern_values[step] if step < len(pattern_values) else 'N/A'}, no se reproduce el canal {channel_idx}.")

    
    def test_step(self, contador, channel_idx, pattern, tono=1.0, vol=1.0, pan = 0.0):
        if pattern == 1 and contador == 0:
            self.ply(channel_idx, tono=tono, vol=vol, pan=pan)
            contador += 1
        if pattern == 0 and contador >= 1:
            contador = 0
        
        return False, contador
    
    
    



# Crear el objeto
Sound = Sonido()



class Buttons:
         
    def __init__(self):
        #self.confirm_close = False      # Confirma si quiere salir de la aplicacion 
        largo = len(Samples.wav_files)
        self.color_text = (255, 255, 255) # Color de texto de los botones
        self.color_actual = (255, 225, 255)
        self.on_color = (255, 0, 0)   # Color por defecto de los botones activos
        self.off_color = (60, 20, 20) # Color por defecto de los botones inactivos
        self.color_bank = [self.on_color, self.off_color, self.off_color, self.off_color] # Color por default de los bancos
                        
        self.color_bank_numbers = [self.on_color, self.off_color, self.off_color, self.off_color, self.off_color, self.off_color, self.off_color, self.off_color]
        
        self.bank_number = 0           # Nuero del digitos 1-8 del banco seleccionado
        self.number_state = [0] * 8
        self.number_state[0] = 1       # Inicia por defecto un valor en la primera posicion

        self.bank = 0                  # Numero del banco seleccionado A-B-C-D        
        self.state = [0] * 4
        self.state[0] = 1              # Inicia por defecto un valor en la primera posicion
        
        self.gupo = 0
        self.numero = 0

        self.color_write = self.off_color
        self.write_mode = False

        self.pulsador = False              # Control de botones de las flechas del song position
        self.pulsador_patt_num = False     # Control de pulsador de 1-8
        self.pulsador_bank_num = False     # Control de pulsador de banco A-B-C-D
                
        self.clipboard = [[0] * 16 for _ in range(largo)] # Copied temp memory of active pattern
                  
        self.patterns_numeros = [[0] * 8 for _ in range(4)]

        self.color_copy = (self.off_color)
        self.color_paste = (self.off_color)
        self.COPY_BTN = pygame.Rect(700, 250, 50, 30)
        self.PASTE_BTN = pygame.Rect(760, 250, 50, 30)

        self.color_flechas_izq = (self.on_color)
        self.color_flechas_der = (self.on_color)

        self.skin_color = [self.off_color, self.off_color, self.off_color, self.off_color, self.off_color, self.off_color]

        self.BTN_CLOSE_NO = pygame.Rect(WINDOW_WIDTH / 3 - 50, WINDOW_HEIGHT / 3 + 50, 100, 40)
        self.BTN_CLOSE_YES = pygame.Rect(WINDOW_WIDTH / 3 + 70, WINDOW_HEIGHT / 3 + 50, 100, 40)
        self.BOX_CLOSE = pygame.Rect(WINDOW_WIDTH / 3 - 140, WINDOW_HEIGHT / 3 - 5, 400, 130)
        
        
        self.STOP_BUTTON = pygame.Rect(100, WINDOW_HEIGHT - 61, 80, 40)

        # Triangulos Flechas de Song Position
        self.T1V1 = (700 + 1, 190 - 19) # Vertices
        self.T1V2 = (730 + 1, 200 - 19) # Vertices
        self.T1V3 = (730 + 1, 180 - 19) # Vertices
        self.TRI_BL = [self.T1V1, self.T1V2, self.T1V3]  # Triangulo izquierdo
        self.T2V1 = (790 + 10, 190 - 19) # Vertices
        self.T2V2 = (760 + 10, 200 - 19) # Vertices
        self.T2V3 = (760 + 10, 180 - 19) # Vertices
        self.TRI_BR = [self.T2V1, self.T2V2, self.T2V3] # Triangulo derecho

        # Referencia de las flechas de Song Position
        self.RF_T1 = pygame.Rect(688, 160, 45, 30) # Botones de ref. triangulo 1
        self.RF_T2 = pygame.Rect(760, 160, 45, 30) # Botones de ref. triangulo 2        
        
        # Pattern BOX diseño cuadrado de la caja
        self.PTN_BOX_D = pygame.Rect(690, 290, 130, 170)

        # Pattern BOX 1-2-3-4-5-6-7-8
        self.PTN_1 = pygame.Rect(700, 300, 20, 25)
        self.PTN_2 = pygame.Rect(730, 300, 20, 25)
        self.PTN_3 = pygame.Rect(760, 300, 20, 25)
        self.PTN_4 = pygame.Rect(790, 300, 20, 25)
        self.PTN_5 = pygame.Rect(700, 330, 20, 25)
        self.PTN_6 = pygame.Rect(730, 330, 20, 25)
        self.PTN_7 = pygame.Rect(760, 330, 20, 25)
        self.PTN_8 = pygame.Rect(790, 330, 20, 25)
        
        # Pattern BOX A-B-C-D
        self.PTN_A = pygame.Rect(700, 380, 20, 25)
        self.PTN_B = pygame.Rect(730, 380, 20, 25)
        self.PTN_C = pygame.Rect(760, 380, 20, 25)
        self.PTN_D = pygame.Rect(790, 380, 20, 25)

        # Pattern BOX Write Mode
        self.PIN_WRITE = pygame.Rect(718, 430, 80, 22)
    
    

    def draw(self):
        draw_ref = False

        if Pestania.confirm_close == True:
            pygame.draw.rect(screen, (100, 0, 0), self.BTN_CLOSE_NO)
            pygame.draw.rect(screen, (100, 0, 0), self.BTN_CLOSE_YES)
            pygame.draw.rect(screen, (255, 0, 0), self.BOX_CLOSE, 1)

        pygame.draw.polygon(screen, self.color_flechas_izq, self.TRI_BL) # Triangle
        pygame.draw.polygon(screen, self.color_flechas_der, self.TRI_BR) # Triangle

        if draw_ref == True:
            pygame.draw.rect(screen, Color.r, self.RF_T1)
            pygame.draw.rect(screen, Color.r, self.RF_T2)
            print("Botones de referencia para los triangulos")
        
        pygame.draw.rect(screen, Color.w, self.PTN_BOX_D, 1)
        pygame.draw.rect(screen, self.color_copy, self.COPY_BTN)
        pygame.draw.rect(screen, self.color_paste, self.PASTE_BTN)
        
        pygame.draw.rect(screen, self.color_bank_numbers[0], self.PTN_1)
        pygame.draw.rect(screen, self.color_bank_numbers[1], self.PTN_2)
        pygame.draw.rect(screen, self.color_bank_numbers[2], self.PTN_3)
        pygame.draw.rect(screen, self.color_bank_numbers[3], self.PTN_4)
        pygame.draw.rect(screen, self.color_bank_numbers[4], self.PTN_5)
        pygame.draw.rect(screen, self.color_bank_numbers[5], self.PTN_6)
        pygame.draw.rect(screen, self.color_bank_numbers[6], self.PTN_7)
        pygame.draw.rect(screen, self.color_bank_numbers[7], self.PTN_8)
            
        pygame.draw.rect(screen, self.color_bank[0], self.PTN_A)
        pygame.draw.rect(screen, self.color_bank[1], self.PTN_B)
        pygame.draw.rect(screen, self.color_bank[2], self.PTN_C)
        pygame.draw.rect(screen, self.color_bank[3], self.PTN_D)

        pygame.draw.rect(screen, self.color_write, self.PIN_WRITE)

        if Pestania.settings == True:
            pygame.draw.rect(screen, self.skin_color[0], COLOR_BTN1)
            pygame.draw.rect(screen, self.skin_color[1], COLOR_BTN2)
            pygame.draw.rect(screen, self.skin_color[2], COLOR_BTN3)
            pygame.draw.rect(screen, self.skin_color[3], COLOR_BTN4)
            pygame.draw.rect(screen, self.skin_color[4], COLOR_BTN5)
            pygame.draw.rect(screen, self.skin_color[5], COLOR_BTN6)
        
        pygame.draw.rect(screen, Color.g, Botones.STOP_BUTTON)
        
        
    def text(self):
        
        self.stop_text = font.render("Stop", True, Color.bg)
        
        self.confirm_close_txt = font_bold.render("Confirm close?", True, Color.w)
        self.conf_close_yes = font_bold.render("Yes", True, (255, 255, 255))
        self.conf_close_no = font_bold.render("No", True, (255, 255, 255))

        self.skin_txt = font.render("Skin color" , True, Color.w)
        self.patt_text = font.render(f"Pattern: {Seq.patt}", True, Color.w)
       
        self.song_pos_txt = font.render("Song position", True, Color.w)
        self.copy_text = font.render("Copy", True, Color.w)
        self.paste_text = font.render("Paste", True, Color.w)
        
        self.p1_text = font.render("1", True, self.color_actual)
        self.p2_text = font.render("2", True, self.color_actual)
        self.p3_text = font.render("3", True, self.color_actual)
        self.p4_text = font.render("4", True, self.color_actual)
        self.p5_text = font.render("5", True, self.color_actual)
        self.p6_text = font.render("6", True, self.color_actual)
        self.p7_text = font.render("7", True, self.color_actual)
        self.p8_text = font.render("8", True, self.color_actual)
        
        self.a_text = font.render("A", True, self.color_actual)
        self.b_text = font.render("B", True, self.color_actual)
        self.c_text = font.render("C", True, self.color_actual)
        self.d_text = font.render("D", True, self.color_actual)

        if self.write_mode == True:
            self.write_mode_text = font.render("Write", True, self.color_actual)
        else:
            self.write_mode_text = font.render("Read", True, self.color_actual)    
                        
    
    def show(self):
        if Pestania.confirm_close == True:
            screen.blit(self.confirm_close_txt, (WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3))
            screen.blit(self.conf_close_no, (self.BTN_CLOSE_NO.x + 35, self.BTN_CLOSE_NO.y + 10))
            screen.blit(self.conf_close_yes, (self.BTN_CLOSE_YES.x + 35, self.BTN_CLOSE_YES.y + 10))
            
        if Pestania.settings == True:
            screen.blit(self.skin_txt, (COLOR_BTN1.x + 5, COLOR_BTN1.y - 22))
        
        screen.blit(self.patt_text, (705, 110))
        
        screen.blit(self.song_pos_txt, (705, 130))
        screen.blit(self.copy_text, (self.COPY_BTN.x + 5, self.COPY_BTN.y + 5))
        screen.blit(self.paste_text, (self.PASTE_BTN.x + 5, self.PASTE_BTN.y + 5))
        
        screen.blit(self.p1_text, (self.PTN_1.x + 6, self.PTN_1.y +5 ))
        screen.blit(self.p2_text, (self.PTN_2.x + 6, self.PTN_2.y +5 ))
        screen.blit(self.p3_text, (self.PTN_3.x + 6, self.PTN_3.y +5 ))
        screen.blit(self.p4_text, (self.PTN_4.x + 6, self.PTN_4.y +5 ))
        screen.blit(self.p5_text, (self.PTN_5.x + 6, self.PTN_5.y +5 ))
        screen.blit(self.p6_text, (self.PTN_6.x + 6, self.PTN_6.y +5 ))
        screen.blit(self.p7_text, (self.PTN_7.x + 6, self.PTN_7.y +5 ))
        screen.blit(self.p8_text, (self.PTN_8.x + 6, self.PTN_8.y +5 ))
        
        screen.blit(self.a_text, (self.PTN_A.x + 5, self.PTN_A.y +5 ))
        screen.blit(self.b_text, (self.PTN_B.x + 5, self.PTN_B.y +5 ))
        screen.blit(self.c_text, (self.PTN_C.x + 5, self.PTN_C.y +5 ))
        screen.blit(self.d_text, (self.PTN_D.x + 5, self.PTN_D.y +5 ))

        screen.blit(self.write_mode_text, (self.PIN_WRITE.x + 20, self.PIN_WRITE.y + 2))

        screen.blit(self.stop_text, (self.STOP_BUTTON.x + 10, self.STOP_BUTTON.y + 10))

    
    def stop_now(self):
        Seq.playing = False
        Seq.pulsador_stop = True
        self.write_mode = False               # Quita el modo de escritura
        self.color_write = self.off_color     # Quita el color de escritura
        Sound.stop()                          # Limpia los hilos
        Seq.s_idx = 0    

    
    def stop_song_(self, pos):
        if self.STOP_BUTTON.collidepoint(pos):
            self.stop_now()  


    def write_mode_button(self, pos):
        if self.PIN_WRITE.collidepoint(pos) and Seq.playing == False:  # Si se pulsa el botón de escritura o lectura
            self.write_mode = not self.write_mode                      # Cambiar el modo de escritura
            Seq.patt_state[Seq.apt - 1] = Seq.pattern_num              # Graba en el momento de presionar write mode

        if Seq.playing == True:
            self.write_mode = False

        if self.write_mode == True:
            self.color_write = self.on_color
        else:  
            self.color_write = self.off_color  
        
       
           
    def copy_paste(self, pos):
            largo = len(Samples.wav_files)
            if self.COPY_BTN.collidepoint(pos):
                #print("Pattern Copied ", "POS ", pos)
                self.color_copy = self.on_color
                for channel_idx in range(largo):
                    for step_idx in range(16):
                        self.clipboard[channel_idx][step_idx] = Patt.mtx_p[Seq.patt - 1][channel_idx][step_idx]
                    
            
            if self.PASTE_BTN.collidepoint(pos):
                #print("Pattern Copied ", "POS ", pos)
                self.color_paste = self.on_color
                for channel_idx in range(largo):
                    for step_idx in range(16):
                        Patt.mtx_p[Seq.patt - 1][channel_idx][step_idx] = self.clipboard[channel_idx][step_idx]

    
    def reset_colors_copy_paste(self):
        if not hasattr(self, '_last_reset_time'):
            self._last_reset_time = pygame.time.get_ticks()
        
        current_time = pygame.time.get_ticks()
        if current_time - self._last_reset_time > 200:  # 500 ms delay
            self.color_copy = self.off_color
            self.color_paste = self.off_color
            self._last_reset_time = current_time
        
 
    def reset_colors_flechas_song_position(self):
        if not hasattr(self, '_last_reset_time_'):
            self._last_reset_time_ = pygame.time.get_ticks()
        
        current_time_ = pygame.time.get_ticks()
        if current_time_ - self._last_reset_time_ > 200:
            self.color_flechas_izq = self.off_color
            self.color_flechas_der = self.off_color
            self._last_reset_time_ = current_time_

    def pattern_sel(self):
        # Obtener el índice del botón activo (A=0, B=1, C=2, D=3)
        self.grupo = self.state.index(1)  
        # Obtener el índice del botón numérico activo (1 al 8)
        self.numero = self.number_state.index(1) + 1  
        # Calcular el valor total
        valor = self.grupo * 8 + self.numero
        print("VALOR PATTERNS ", valor)
        Seq.pattern_num = valor

        
        
        
     
    def toggle_bank(self, bank, button, pos):
               
        if button.collidepoint(pos) and not Seq.playing:

            self.pulsador_bank_num = True
            # Si el banco ya está activo, no hace nada
            if self.state[bank] == 1:
                print("Bank already active, no changes made.")
                return
            
            # Desactiva todos los demás bancos y resetea sus patrones
            for i in range(4):
                if i != bank:
                    self.state[i] = 0
                    self.color_bank[i] = self.off_color
                    for nums in range(8):
                        #print("Nums ---------------------------------", nums)
                        self.patterns_numeros[i][nums] = 0

            # Activa el banco seleccionado
            self.state[bank] = 1
            self.color_bank[bank] = self.on_color
            # Marca el patrón actual en ese banco
            self.patterns_numeros[bank][self.bank_number] = 1
            
            self.pattern_sel()

            print(f"Activando bank {bank}, bank_number: {self.bank_number}")
            print("Estado de bancos: ", self.state)
                          

    def handle_patterns(self, pos):
        self.toggle_bank(0, self.PTN_A, pos)
        self.toggle_bank(1, self.PTN_B, pos)
        self.toggle_bank(2, self.PTN_C, pos)
        self.toggle_bank(3, self.PTN_D, pos)
        

        


    
    def handle_pattern_numbers(self, pos):
        if not Seq.playing:
            for num, button in enumerate([self.PTN_1, self.PTN_2, self.PTN_3, self.PTN_4, 
                                          self.PTN_5, self.PTN_6, self.PTN_7, self.PTN_8]):
                if button.collidepoint(pos):
                    self.number_state = [1 if i == num else 0 for i in range(8)]
                    self.color_bank_numbers = [self.on_color if i == num else self.off_color for i in range(8)]
                    self.pulsador_patt_num = True
                    self.pattern_sel()
                    print(f"Botón {num + 1}")
                    
                    break
        """
        # Mostrar el valor de pattern y los bancos seleccionados      
        for i in range(8):
            print("Numbers 1-8 ", self.number_state[i])

        for i in range(4):
            print("Banks A-B-C-D ", self.state[i])"""
    
    

    def handle_botones_triangulo(self, pos):
        if Pestania.sequencer_1 == True or Pestania.sequencer_2 == True:
          
            if self.RF_T1.collidepoint(pos) and Seq.apt > 1 : # Triangulo izquierdo
                if pygame.mouse.get_pressed()[0]:
                    self.color_flechas_izq = self.on_color
                    Seq.apt -= 1
                    self.pulsador = True        # Controla si se pulso
                    print("Valor de la pattern en la funcion botones del trianguos", Seq.patt, "La posicion de la cancion es ", Seq.apt)  
                    
            if self.RF_T2.collidepoint(pos) and Seq.apt < 32 and Seq.apt < Seq.tpt: # Triangulo derecho
                if pygame.mouse.get_pressed()[0]:
                    self.color_flechas_der = self.on_color
                    Seq.apt += 1
                    self.pulsador = True        # Controla si se pulso
                    print("Valor de la pattern en la funcion botones del trianguos", Seq.patt, "La posicion de la cancion es ", Seq.apt)  

                        


               
              
Botones = Buttons() # Make Object from class Buttons               
                


## - CONSTANTES - ##

# Configuración de los pasos, volúmenes y paneo
STEP_WIDTH = 20
STEP_HEIGHT = 25
STEP_MARGIN = 5
COLOR_SIZE = 20
CHANNEL_HEIGHT = STEP_HEIGHT + STEP_MARGIN

TON_WIDTH = 40
TON_HEIGHT = 20
VOL_WIDTH = 40
VOL_HEIGHT = 20
PAN_WIDTH = 60  # Definimos ancho para el paneo
PAN_HEIGHT = 20
DRAW_X = 150  # Posición inicial x de steps

# Botones y cuadros

PLAY_BUTTON = pygame.Rect(10, WINDOW_HEIGHT - 61, 80, 40)

TEMPO_BOX = pygame.Rect(200, WINDOW_HEIGHT - 61, 117, 40)
MASTER_VOL_BOX = pygame.Rect(320, WINDOW_HEIGHT - 61, 130, 40)
PATTERN_BOX = pygame.Rect(690, 152, 130, 40)
PATTERN_TOTAL = pygame.Rect(690, 190, 130, 40)
SETTING_BOX = pygame.Rect(PATTERN_TOTAL.x, PATTERN_TOTAL.y + 350, 95, 60)

# Botones load/save y menú desplegable para las memorias
SAVE_BUTTON = pygame.Rect(690, WINDOW_HEIGHT - 61, 80, 40)
LOAD_BUTTON = pygame.Rect(690, WINDOW_HEIGHT - 105, 80, 40)
MENU_BUTTON = pygame.Rect(690, WINDOW_HEIGHT - 155, 100, 40)

COLOR_BTN1 = pygame.Rect(MASTER_VOL_BOX.x + 220 + 22, WINDOW_HEIGHT - 65, COLOR_SIZE, COLOR_SIZE)
COLOR_BTN2 = pygame.Rect(MASTER_VOL_BOX.x + 250 + 22, WINDOW_HEIGHT - 65, COLOR_SIZE, COLOR_SIZE)
COLOR_BTN3 = pygame.Rect(MASTER_VOL_BOX.x + 280 + 22, WINDOW_HEIGHT - 65, COLOR_SIZE, COLOR_SIZE)
COLOR_BTN4 = pygame.Rect(MASTER_VOL_BOX.x + 220 + 22, WINDOW_HEIGHT - 40, COLOR_SIZE, COLOR_SIZE)
COLOR_BTN5 = pygame.Rect(MASTER_VOL_BOX.x + 250 + 22, WINDOW_HEIGHT - 40, COLOR_SIZE, COLOR_SIZE)
COLOR_BTN6 = pygame.Rect(MASTER_VOL_BOX.x + 280 + 22, WINDOW_HEIGHT - 40, COLOR_SIZE, COLOR_SIZE)

BNK_BUTTON = pygame.Rect(690, WINDOW_HEIGHT - 205, 95, 40)

MENU_WIDTH = 100
MENU_ITEM_HEIGHT = 30
MENU_ITEMS = 10  # 10 memorias (1 a 10)

# Variable para el nombre del preset
current_preset = "default_preset"

LED_DURATION = 50