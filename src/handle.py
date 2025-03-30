from tkinter import SE
import pygame
import test
#import #wiringpi
import sounddevice as sd
from config.variables import TON_HEIGHT, TON_WIDTH, Botones, Samples, Sound
from config.variables import Pestania, Color, Patt, Seq, MENU_BUTTON, MENU_ITEMS, MENU_ITEM_HEIGHT, MENU_WIDTH, DRAW_X, STEP_WIDTH, STEP_MARGIN, STEP_HEIGHT, CHANNEL_HEIGHT, VOL_HEIGHT, VOL_WIDTH, PAN_WIDTH, PAN_HEIGHT, COLOR_BTN1, COLOR_BTN2, COLOR_BTN3, COLOR_BTN4, COLOR_BTN5, COLOR_BTN6, SAVE_BUTTON, LOAD_BUTTON, PLAY_BUTTON, BNK_BUTTON, PATTERN_TOTAL, SETTING_BOX, TEMPO_BOX, MASTER_VOL_BOX, LED_DURATION, led_pins
from .jsncodes import save_preset
from .jsncodes import load_preset


SC_H = 180 # Altura de los botones de la configuracion de sonido
SC1 = pygame.Rect(60, SC_H, 20, 20)
SC2 = pygame.Rect(90, SC_H, 20, 20)

SC_BUF_H = 280
SC_BUFF1 = pygame.Rect(60, SC_BUF_H, 20, 20)
SC_BUFF2 = pygame.Rect(90, SC_BUF_H, 20, 20)

device_rects = {}
buffer_rects = {}
largo = len(Samples.wav_files)
count = [[0] * 16 for _ in range(largo)]



"""
def samples_banks_sel(channels, channel_idx):
    
    # Selector de banco de sonidos
    if Samples.select_bank == 0: 
        sound = sound_objects[channel_idx]
    if Samples.select_bank == 1:
        sound = sound_objects_2[channel_idx]
    if Samples.select_bank == 2:
        sound = sound_objects_3[channel_idx]

    return sound

def play_step_on_stop(channel_idx, patt_in, test):
    global channels
    
    sound = samples_banks_sel(channels, channel_idx)

    if patt_in == 1 and test == True:
        channels[channel_idx].play(sound)
    
    return False



def play_sound_and_light(channel_idx):
    global channels
    #Reproduce un sonido y enciende su LED con volumen y panorama ajustados.
    sound = samples_banks_sel(channels, channel_idx)
    
    vol = Seq.channel_volumes[channel_idx] * Seq.m_vol
    sound.set_volume(vol)
    pin = led_pins[channel_idx]
    #wiringpi.digitalWrite(pin, 1)
    left = (1 - Seq.pan_volumes[channel_idx]) / 2
    right = (1 + Seq.pan_volumes[channel_idx]) / 2
    channels[channel_idx].set_volume(left, right)
    channels[channel_idx].play(sound)
    return pygame.time.get_ticks() + LED_DURATION

def turn_off_led(channel_idx):
    # Apaga el LED de un canal.
    #pin = led_pins[channel_idx]
    #wiringpi.digitalWrite(pin, 0) """

def pattern_control():
    #print("Step actual > > > > > > > ----->", Seq.s_idx)

    # Si llegamos al final de la secuencia completa, reseteamos
    if Seq.s_idx >= 16 * Seq.tpt:
        Seq.s_idx = 0
        Seq.apt = 1
        """       
                
        print("Reset step:", Seq.s_idx, "and active patt:", Seq.apt)
        
        # Mostrar bancos activos
        for i in range(4):
            print("Bank selected ", Botones.state[i])

        # Mostrar patrones activos
        for i in range(8):
            print("Pattern selected ", Botones.number_state[i])"""

    # Calcular el índice de pattern actual según s_idx
    current_pattern_idx = (Seq.s_idx // 16) % Seq.tpt
    if 0 <= current_pattern_idx < Seq.tpt:
        nuevo_apt = current_pattern_idx + 1

        # Si el pattern activo cambia
        if nuevo_apt != Seq.apt:
            Seq.apt = nuevo_apt
           
            Seq.s_idx = (Seq.apt - 1) * 16  # Ajustar el paso al inicio del nuevo pattern

            #Botones.update_pattern_state()
            #print("Active PATT:", Seq.apt, "Patterns: ", patterns)
 
        
                
def handle_input(pos):
    
    # Manejo de clics en la pestaña de configuración
    if Pestania.settings == True and Seq.playing == False:
        
        if SC1.collidepoint(pos):
            print("Cambio audio -")
            Sound.change_audio_driver(0) # 0 para restar
        if SC2.collidepoint(pos):  
            print("Cambio audio +")
            Sound.change_audio_driver(1) # 1 para sumar

        if SC_BUFF1.collidepoint(pos):
            Sound.change_audio_buffer(0) # 0 para restar

        if SC_BUFF2.collidepoint(pos):        
            Sound.change_audio_buffer(1) # 1 para sumar

        """    
        # Seleccionar tarjeta de sonido
        for idx, rect in device_rects.items():
            if rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                success = Sound.update_audio_device(idx, Sound.blocksize)
                if success:
                    Pestania.settings = False  # Cerrar pestaña si funciona
                else:
                    print(f"Fallo al seleccionar dispositivo {idx}")
                break

        # Seleccionar tamaño de buffer
        for i, rect in buffer_rects.items():
            if rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                new_blocksize = [64, 128, 256, 512][i]
                success = Sound.update_audio_device(sd.default.device, new_blocksize)
                if success:
                    print(f"Nueva seleccion de buffer {new_blocksize}")
                else:
                    print(f"Fallo al seleccionar blocksize {new_blocksize}")
                break"""
    

    if MENU_BUTTON.collidepoint(pos):
        Seq.m_opn = not Seq.m_opn
        return

    if Seq.m_opn:
        for i in range(MENU_ITEMS):
            menu_item_rect = pygame.Rect(MENU_BUTTON.x, MENU_BUTTON.y - (i + 1) * MENU_ITEM_HEIGHT, MENU_WIDTH, MENU_ITEM_HEIGHT)
            if menu_item_rect.collidepoint(pos):
                Seq.s_mem = i + 1
                Seq.m_opn = False
                print(f"Memoria seleccionada: {Seq.s_mem}")
                return
    
    if Pestania.confirm_close == False and Pestania.sequencer_1 == True:

        for channel_idx in range(24): # Recorre la matrix de las patterns (((¡¡ SOLO 24 porque es el secuenciador 1 !!)))
            for step_idx in range(16):
                test_play = False
                x = DRAW_X + step_idx * (STEP_WIDTH + STEP_MARGIN)
                y = 30 + channel_idx * CHANNEL_HEIGHT
                rect = pygame.Rect(x, y, STEP_WIDTH, STEP_HEIGHT)
                if rect.collidepoint(pos):
                    test_play = True
                    
                    Patt.mtx_p[Seq.patt - 1][channel_idx][step_idx] = 1 - Patt.mtx_p[Seq.patt - 1][channel_idx][step_idx] # Guarda los cambios en Patt.mtx_p
                     
                    if test_play:
                        test_play, count[channel_idx][step_idx] = Sound.test_step(count[channel_idx][step_idx], channel_idx, Patt.mtx_p[Seq.patt - 1][channel_idx][step_idx])
                                 
                    
                    #for i in range(16):
                    #    print("Channel1 STEP ", i + 1,"Patt.mtx_p", Patt.mtx_p[0][0][i], " Pattern active: ", Seq.patt)
            
            vol_x = DRAW_X + 16 * (STEP_WIDTH + STEP_MARGIN) + 10
            vol_y = 30 + channel_idx * CHANNEL_HEIGHT + (STEP_HEIGHT - VOL_HEIGHT) // 2
            vol_rect = pygame.Rect(vol_x, vol_y, VOL_WIDTH, VOL_HEIGHT)
            if vol_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    Seq.channel_volumes[channel_idx] = min(1.0, Seq.channel_volumes[channel_idx] + 0.05)
                elif pygame.mouse.get_pressed()[2]:
                    Seq.channel_volumes[channel_idx] = max(0.0, Seq.channel_volumes[channel_idx] - 0.05)
            
            pan_x = vol_x + VOL_WIDTH + 10
            pan_rect = pygame.Rect(pan_x, vol_y, PAN_WIDTH, PAN_HEIGHT)
            if pan_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    Seq.pan_volumes[channel_idx] = min(1.0, Seq.pan_volumes[channel_idx] + 0.05)
                elif pygame.mouse.get_pressed()[2]:
                    Seq.pan_volumes[channel_idx] = max(-1.0, Seq.pan_volumes[channel_idx] - 0.05)

            ton_x = DRAW_X - 50
            ton_y = vol_y
            ton_rect = pygame.Rect(ton_x, ton_y, TON_WIDTH, TON_HEIGHT)
            if ton_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    print("Subiendo tono canal ", channel_idx, " value ", Seq.tones[channel_idx])
                    Seq.tones[channel_idx] = min(2.0, Seq.tones[channel_idx] + 0.05)
                elif pygame.mouse.get_pressed()[2]:
                    print("Bajando tono canal ", channel_idx, " value ", Seq.tones[channel_idx])
                    Seq.tones[channel_idx] = max(-1.0, Seq.tones[channel_idx] - 0.05)


    if Pestania.confirm_close == False and Pestania.sequencer_2 == True and Pestania.sequencer_1 == False:

            for channel_idx in range(4): # Recorre la matrix de las patterns
                for step_idx in range(16):
                    test_play = False
                    x = DRAW_X + step_idx * (STEP_WIDTH + STEP_MARGIN)
                    y = 180 + channel_idx * CHANNEL_HEIGHT * 6
                    rect = pygame.Rect(x, y, STEP_WIDTH, STEP_HEIGHT)
                    if rect.collidepoint(pos):
                        test_play = True
                        
                        # Tiene solo 4 posiciones por eso usamos channel_idx de 0 a 3
                        Patt.mtx_p[Seq.patt - 1][channel_idx + 24][step_idx] = 1 - Patt.mtx_p[Seq.patt - 1][channel_idx + 24][step_idx]
                        
                        # Tiene 28 posiciones por eso usamos + 24
                        if test_play:
                            test_play, count[channel_idx + 24][step_idx] = Sound.test_step(count[channel_idx + 24][step_idx], channel_idx + 24, Patt.mtx_p[Seq.patt - 1][channel_idx + 24][step_idx])

                    
                    notes_sum = pygame.Rect(x, y - 67, STEP_WIDTH, STEP_HEIGHT / 2)
                    if notes_sum.collidepoint(pos): # Si toca en la suma
                        
                        note = Seq.subir_semitono(channel_idx)
                       
                        Seq.txt2_note[Seq.patt - 1][channel_idx][step_idx] = note   # Almacena el indice de la nota
                        Seq.sq2_note[Seq.patt - 1][channel_idx][step_idx] = Seq.get_factor(channel_idx)    # Almacena el valor del tono

                    note_rest = pygame.Rect(x, y - 20, STEP_WIDTH, STEP_HEIGHT / 2)
                    if note_rest.collidepoint(pos): # Si toca en la resta
                        
                        note = Seq.bajar_semitono(channel_idx)
                        
                        Seq.txt2_note[Seq.patt - 1][channel_idx][step_idx] = note   # Almacena el indice de la nota
                        Seq.sq2_note[Seq.patt - 1][channel_idx][step_idx] = Seq.get_factor(channel_idx)    # Almacena el valor del tono





    
    if Pestania.settings == True:
        if COLOR_BTN1.collidepoint(pos):
            Color.bg = (0, 0, 0)
            Color.w = (255, 255, 255)
            Color.g = (150, 150, 150)
            Color.gn = (0, 255, 0)
            Color.r = (255, 0, 0)
            Botones.skin_color[0] = Botones.on_color
            for i in range(6):
                if i != 0:
                    Botones.skin_color[i] = Botones.off_color
            print("Color 1")
        if COLOR_BTN2.collidepoint(pos):
            Color.bg = (153, 255, 51)
            Color.w = (0, 0, 0)
            Color.g = (0, 0, 0)
            Color.gn = (255, 0, 0)
            Color.r = (255, 0, 0)
            Botones.skin_color[1] = Botones.on_color
            for i in range(6):
                if i != 1:
                    Botones.skin_color[i] = Botones.off_color
            print("Color 2")
        if COLOR_BTN3.collidepoint(pos):
            Color.bg = (210, 237, 255)
            Color.w = (0, 0, 0)
            Color.g = (110, 110, 110)
            Color.gn = (255, 0, 0)
            Color.r = (255, 255, 0)
            Botones.skin_color[2] = Botones.on_color
            for i in range(6):
                if i != 2:
                    Botones.skin_color[i] = Botones.off_color
            print("Color 3")
        if COLOR_BTN4.collidepoint(pos):
            Color.bg = (60, 60, 60)
            Color.w = (255, 255, 255)
            Color.g = (150, 150, 150)
            Color.gn = (0, 255, 0)
            Color.r = (255, 0, 0)
            Botones.skin_color[3] = Botones.on_color
            for i in range(6):
                if i != 3:
                    Botones.skin_color[i] = Botones.off_color
        if COLOR_BTN5.collidepoint(pos):
            Color.bg = (76, 0, 153)
            Color.w = (255, 255, 255)
            Color.g = (150, 150, 150)
            Color.gn = (255, 0, 0)
            Color.r = (255, 255, 0)
            Botones.skin_color[4] = Botones.on_color
            for i in range(6):
                if i != 4:
                    Botones.skin_color[i] = Botones.off_color
        if COLOR_BTN6.collidepoint(pos):
            Color.bg = (255, 229, 204)
            Color.w = (0, 0, 0)
            Color.g = (150, 150, 150)
            Color.gn = (0, 0, 0)
            Color.r = (0, 0, 0)
            Botones.skin_color[5] = Botones.on_color
            for i in range(6):
                if i != 5:
                    Botones.skin_color[i] = Botones.off_color

        
    
    Pestania.tab_buttons_actions(pos) # Controla la accion de las pestañas
         
    
    if SAVE_BUTTON.collidepoint(pos):
        save_preset()
    if LOAD_BUTTON.collidepoint(pos):
        load_preset()
    
    # Boton play funciona si dichas pestañas estan activas
    if Pestania.sequencer_1 == True or Pestania.sequencer_2 == True or Pestania.mixer == True:
        if PLAY_BUTTON.collidepoint(pos):
            Seq.playing = True
            Botones.write_mode = False               # Quita el modo de escritura
            Botones.color_write = Botones.off_color  # Quita el color de escritura

    if Pestania.settings == True:
        Botones.stop_now()       # Se detiene enseguida

    Botones.stop_song_(pos)      # Controla si se presiona el boton stop
               
    if Seq.playing == False:
        if BNK_BUTTON.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:  # Clic izquierdo: aumentar banco
                bank = min(2, Sound.bank + 1)
                Sound.load_samples_banks(bank)
            elif pygame.mouse.get_pressed()[2]:  # Clic derecho: disminuir banco
                bank = max(0, Sound.bank - 1)
                Sound.load_samples_banks(bank)
        
        Botones.handle_botones_triangulo(pos) # Si la secuencia esta detenida puede manejar los botones del triangulo
              
                
        
        if PATTERN_TOTAL.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                Seq.tpt = min(32, Seq.tpt + 1)

                #Botones.update_pattern_state()
                if Seq.apt > Seq.tpt:
                    Seq.apt = Seq.tpt
                    
            elif pygame.mouse.get_pressed()[2]:
                #Botones.update_pattern_state()
                Seq.tpt = max(1, Seq.tpt - 1)
                if Seq.apt > Seq.tpt:
                    Seq.apt = Seq.tpt
                    
        if SETTING_BOX.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                print("")
            elif pygame.mouse.get_pressed()[2]:
                print("")
        
    
    if TEMPO_BOX.collidepoint(pos):
        if pygame.mouse.get_pressed()[0]:
            Seq.tempo = min(200, Seq.tempo + 2)
        elif pygame.mouse.get_pressed()[2]:
            Seq.tempo = max(20, Seq.tempo - 2)
        Seq.tpo_txt = str(Seq.tempo)
    if MASTER_VOL_BOX.collidepoint(pos):
        if pygame.mouse.get_pressed()[0]:
            Seq.m_vol = min(1.0, Seq.m_vol + 0.01)
        elif pygame.mouse.get_pressed()[2]:
            Seq.m_vol = max(0.0, Seq.m_vol - 0.01)

def update_sequencer():
      
    if not Seq.playing:
        return
    
    current_time = pygame.time.get_ticks()
    beat_duration = 60.0 / Seq.tempo * 1000
    step_duration = beat_duration / 4
    
    expired_channels = [ch for ch, off_time in Seq.act_chs.items() if current_time >= off_time]
    for channel_idx in expired_channels:
        #turn_off_led(channel_idx)
        del Seq.act_chs[channel_idx]
    
    if current_time >= Seq.lstime + step_duration:
        # Calcular el paso dentro del pattern activo
        pattern_offset = (Seq.apt - 1) * 16
        local_step = Seq.s_idx - pattern_offset
        
        if local_step >= 0 and local_step < 16:
            for channel_idx, pattern in enumerate(Patt.mtx_p[Seq.patt - 1]):
                if pattern[local_step] == 1:
                    if channel_idx not in Seq.act_chs:
                        
                        if channel_idx < 24 and channel_idx >= 0: # Reproduce los 24 Canales del Secuenciador 1
                            Sound.ply(channel_idx, Seq.tones[channel_idx], Seq.channel_volumes[channel_idx] * Seq.m_vol, Seq.pan_volumes[channel_idx])
                        else:                # Reproduce los 4 del Secuenciador 2
                            tone = Seq.sq2_note[Seq.patt - 1][channel_idx - 24][local_step]
                            print("Tone actual ", tone)
                            Sound.ply(channel_idx, tone, Seq.channel_volumes[channel_idx] * Seq.m_vol, Seq.pan_volumes[channel_idx])

                        print(". ")
        else:
           # Reiniciar Seq.s_idx si excede el rango del pattern actual 
            Seq.s_idx = pattern_offset        
        
        Seq.lstime = current_time
        Seq.s_idx += 1
    #   print("Seq.s_idx / STEP index ", Seq.s_idx)
        
    pattern_control() # Control de avance de los patterns
