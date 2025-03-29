from turtle import st
import pygame
import os
from config.variables import ver, TON_HEIGHT, TON_WIDTH, sd, Seq, Pestania, Sound, font, font_small, font_bold, screen, Color, Patt, Samples, DRAW_X, STEP_WIDTH, STEP_MARGIN, STEP_HEIGHT, CHANNEL_HEIGHT, VOL_HEIGHT, VOL_WIDTH, PAN_HEIGHT, PAN_WIDTH, PLAY_BUTTON, TEMPO_BOX, MASTER_VOL_BOX, SAVE_BUTTON, LOAD_BUTTON, MENU_BUTTON, PATTERN_BOX, PATTERN_TOTAL, BNK_BUTTON, SETTING_BOX, MENU_ITEMS, MENU_WIDTH, MENU_ITEM_HEIGHT
from .handle import Botones

largo = len(Samples.wav_files)
device_rects = {}  # Rectángulos para dispositivos
buffer_rects = {}  # Rectángulos para buffers
STP_IDX_Y = 750

def actualizar_colores_botones(local_pt):
        
        # Calcular banco y número en base a local_pt
        grupo = (local_pt - 1) // 8   # de 0 a 3
        numero = (local_pt - 1) % 8   # de 0 a 7

        # Actualizar colores de los bancos
        for i in range(4):
            if i == grupo:
                Botones.color_bank[i] = Botones.on_color
            else:
                Botones.color_bank[i] = Botones.off_color

        # Actualizar colores de los números
        for i in range(8):
            if i == numero:
                Botones.color_bank_numbers[i] = Botones.on_color
            else:
                Botones.color_bank_numbers[i] = Botones.off_color 

def control_de_pulsadores():
    # Si se esta reproduciendo
    if Seq.playing == True:
        Seq.patt = Seq.patt_state[Seq.apt - 1]   # Si se reproduce solo se actualiza segun la posicion
        Seq.pattern_num = Seq.patt               # Cuando se esta reproduciendo se iguala la variable del numeros de patterns
        actualizar_colores_botones(Seq.patt)
    else: # Si NO se esta reproducciondo:

       # Si esta en modo escritura y no se esta reproduciendo se graba
        if Botones.write_mode == True and Seq.pulsador_stop == False:
            Seq.patt_state[Seq.apt - 1] = Seq.pattern_num  # Write selected pattern in the song position
            Seq.patt = Seq.patt_state[Seq.apt - 1]
            actualizar_colores_botones(Seq.patt)
     
        if Botones.pulsador_patt_num == True  and Botones.pulsador == False and Seq.pulsador_stop == False:
            Seq.patt = Seq.pattern_num       # Como no se esta escribiendo solo se muestra la pattern segun la posicion
            actualizar_colores_botones(Seq.patt)
            Botones.color_write = Botones.off_color
            Botones.pulsador_patt_num = False   # Se restablece
            Botones.write_mode = False          # Se restablece

        if Botones.pulsador_bank_num == True  and Botones.pulsador == False and Seq.pulsador_stop == False:
            Seq.patt = Seq.pattern_num       # Como no se esta escribiendo solo se muestra la pattern segun la posicion
            actualizar_colores_botones(Seq.patt)
            Botones.color_write = Botones.off_color
            Botones.pulsador_bank_num = False   # Se restablece
            Botones.write_mode = False          # Se restablece    
            

        if Botones.pulsador == True and Seq.pulsador_stop == False:
            Seq.patt = Seq.patt_state[Seq.apt - 1]   # Si se presiona las flechas de la posicion se actualiza el estado sin grabar
            Seq.pattern_num = Seq.patt               # Cuando se esta reproduciendo se iguala la variable del numeros de patterns
            actualizar_colores_botones(Seq.patt)
            Botones.pulsador = False     # Se restablece el estado a false

        if Seq.pulsador_stop == True:                # Cuando se presiona stop actualiza el estado segun la posicion 
            Seq.patt = Seq.patt_state[Seq.apt - 1]
            actualizar_colores_botones(Seq.patt)
            Seq.pulsador_stop = False    # Se restablece el estado a false


def draw_steps():
             
    control_de_pulsadores() # Controla la logica de los pulsadores  (play, stop, patterns numbers)

    step_on = Seq.s_idx % 16
    
    if (Pestania.confirm_close == False) and (Pestania.sequencer_1 == True or Pestania.sequencer_2 == True):
        
        ver.logo_escalado(800, 800, 60, 60)

        for i in range(16): # Draw Index steps of leds - (Dibuja los leds de los steps del indice superior e inferior)
            num_text = font_small.render(str(i + 1), True, Color.w)
            screen.blit(num_text, (DRAW_X + i * (STEP_WIDTH + STEP_MARGIN) + STEP_WIDTH // 2 - 5, 5))
            screen.blit(num_text, (DRAW_X + i * (STEP_WIDTH + STEP_MARGIN) + STEP_WIDTH // 2 - 5, STP_IDX_Y + 10))
                    
            if step_on == i:
                pygame.draw.rect(screen, Color.gn, (DRAW_X + i * (STEP_WIDTH + STEP_MARGIN) + STEP_WIDTH // 2 - 10, 20, STEP_WIDTH, STEP_HEIGHT / 4))
                pygame.draw.rect(screen, Color.gn, (DRAW_X + i * (STEP_WIDTH + STEP_MARGIN) + STEP_WIDTH // 2 - 10, STP_IDX_Y, STEP_WIDTH, STEP_HEIGHT / 4))
            else:    
                pygame.draw.rect(screen, Color.g, (DRAW_X + i * (STEP_WIDTH + STEP_MARGIN) + STEP_WIDTH // 2 - 10, 20, STEP_WIDTH, STEP_HEIGHT / 4))
                pygame.draw.rect(screen, Color.g, (DRAW_X + i * (STEP_WIDTH + STEP_MARGIN) + STEP_WIDTH // 2 - 10, STP_IDX_Y, STEP_WIDTH, STEP_HEIGHT / 4))

    if Pestania.confirm_close == False and Pestania.sequencer_1 == True:

        # Draw Samples Names (Sound Bank)
        for channel_idx, pattern in enumerate(Patt.mtx_p[Seq.patt - 1]):
            if channel_idx < 24:
                if Sound.bank == 0:
                    wav_name = os.path.basename(Samples.wav_files[channel_idx]).replace(".wav", "")
                elif Sound.bank == 1:
                    wav_name = os.path.basename(Samples.T909[channel_idx]).replace(".wav", "")
                elif Sound.bank == 2:
                    wav_name = os.path.basename(Samples.C64[channel_idx]).replace(".wav", "")
                else:
                    wav_name = os.path.basename(Samples.wav_files[channel_idx]).replace(".wav", "")
                
                text = font.render(wav_name, True, Color.w)
                screen.blit(text, (10, 30 + channel_idx * CHANNEL_HEIGHT))
        
    
    if Pestania.confirm_close == False and Pestania.sequencer_1 == True:

        # Draw Steps status (Active or Inactive), Channel Volumes and Panning
        for channel_idx, pattern in enumerate(Patt.mtx_p[Seq.patt - 1]): # Seq.apt - 1 
            for step_idx, value in enumerate(pattern):
                if channel_idx < 24:
                    x = DRAW_X + step_idx * (STEP_WIDTH + STEP_MARGIN)
                    y = 30 + channel_idx * CHANNEL_HEIGHT
                    color = Color.r if value == 1 else Color.g # Evalua el color del step
                    pygame.draw.rect(screen, color, (x, y, STEP_WIDTH, STEP_HEIGHT))
                
                    vol_x = DRAW_X + 16 * (STEP_WIDTH + STEP_MARGIN) + 10
                    vol_y = 30 + channel_idx * CHANNEL_HEIGHT + (STEP_HEIGHT - VOL_HEIGHT) // 2
                    pygame.draw.rect(screen, Color.g, (vol_x, vol_y, VOL_WIDTH, VOL_HEIGHT))
                    vol_text = font_small.render(f"{int(Seq.channel_volumes[channel_idx] * 100)}%", True, Color.bg)
                    screen.blit(vol_text, (vol_x + 5, vol_y + 2))
                    
                    pan_x = vol_x + VOL_WIDTH + 10
                    pan_y = vol_y
                    pygame.draw.rect(screen, Color.g, (pan_x, pan_y, PAN_WIDTH, PAN_HEIGHT))
                    pan_text = font_small.render(f"P: {int(Seq.pan_volumes[channel_idx] * 100)}", True, Color.r)
                    screen.blit(pan_text, (pan_x + 5, pan_y + 2))

                    ton_x = DRAW_X - 50
                    ton_y = vol_y
                    pygame.draw.rect(screen, Color.g, (ton_x, ton_y, TON_WIDTH, TON_HEIGHT))
                    pitch_text = font_small.render(f"T: {int(Seq.tones[channel_idx] * 100)}", True, Color.r)
                    screen.blit(pitch_text, (ton_x + 5, ton_y + 2))

    if Pestania.confirm_close == False and Pestania.sequencer_2 == True and Pestania.sequencer_1 == False:

        for channel_idx_2 in range(4):
            idx = channel_idx_2 + 24   # Muestra los sonidos a partir del 24 por lo tanto mostrara 4 mas en el secuenciador secundario
            if Sound.bank == 0:
                wav_name = os.path.basename(Samples.wav_files[idx]).replace(".wav", "")
            elif Sound.bank == 1:
                wav_name = os.path.basename(Samples.T909[idx]).replace(".wav", "")
            elif Sound.bank == 2:
                wav_name = os.path.basename(Samples.C64[idx]).replace(".wav", "")
            else:
                wav_name = os.path.basename(Samples.wav_files[idx]).replace(".wav", "")
            
            text = font.render(wav_name, True, Color.w)
            screen.blit(text, (10, 180 + channel_idx_2 * CHANNEL_HEIGHT * 6))

        sum_text = font.render("+", True, Color.w)
        rest_txt = font.render("-", True, Color.w)
        

        # Draw Steps status (Active or Inactive), SEQUENCER 2
        for i in range(4):
            patt = 24 + i
            
            for step_idx in range(16):
                if patt < largo:
                    if Patt.mtx_p[Seq.patt - 1][patt][step_idx] == 1:   # Muesta el step activo del secuenciador 2
                        color = Color.r
                    else:
                        color = Color.g    

                    x = DRAW_X + step_idx * (STEP_WIDTH + STEP_MARGIN)
                    y = 180 + i * CHANNEL_HEIGHT * 6
                    pygame.draw.rect(screen, color, (x, y, STEP_WIDTH, STEP_HEIGHT))

                    text = Seq.txt2_note[Seq.patt - 1][i][step_idx]
                    note_txt = font_small.render(f"{text}", True, (0, 0, 0))                  
                    
                    print("Current note recibida baby es ", text)
                    #print("Esta es la magia baby la famosa nota de texto?  ", note_txt)
                    pygame.draw.rect(screen, Pestania.btn_color, (x, y - 67, STEP_WIDTH, STEP_HEIGHT / 2)) # Suma
                    pygame.draw.rect(screen, Color.w, (x, y - 50, STEP_WIDTH, STEP_HEIGHT))
                    pygame.draw.rect(screen, Pestania.btn_color, (x, y - 20, STEP_WIDTH, STEP_HEIGHT / 2)) # Resta
                    screen.blit(sum_text, (x + 6, y - 70,))
                    screen.blit(rest_txt, (x + 7, y - 26))
                    screen.blit(note_txt, (x + 1, y - 43))


                else:
                    print("Error Secuenciador 2 ", patt, " fuera de rango de " , largo)

                






def draw_ui():
       
          
    play_color = Color.gn if Seq.playing else Color.g
    pygame.draw.rect(screen, play_color, PLAY_BUTTON)
    
    pygame.draw.rect(screen, Color.w, TEMPO_BOX, 2)
    pygame.draw.rect(screen, Color.w, MASTER_VOL_BOX, 2)
    pygame.draw.rect(screen, Color.g, SAVE_BUTTON)
    pygame.draw.rect(screen, Color.g, LOAD_BUTTON)
    pygame.draw.rect(screen, Color.g, MENU_BUTTON)
    
    pygame.draw.rect(screen, Color.w, PATTERN_BOX, 1)
    pygame.draw.rect(screen, Color.w, PATTERN_TOTAL, 1)
    
    pygame.draw.rect(screen, Color.g, BNK_BUTTON)

    # Dibuja todos los elementos y botones de la pestaña    
    Pestania.draw()
    Pestania.text()
    Pestania.show()

    # Dibuja todos los elementos hasta la mayoria de los botones y textos
    Botones.draw()
    Botones.text()    
    Botones.show()

    Pestania.tab_selection()  # Dibuja el estado del led de la pestaña
           
    
    if Sound.bank == 0:
       bank_txt = font.render(f"Bank: 808", True, Color.w)
    if Sound.bank == 1:
       bank_txt = font.render(f"Bank: 909", True, Color.w)
    if Sound.bank == 2:
       bank_txt = font.render(f"Bank: C64", True, Color.w)
        
    
        
    
    pattern_text = font.render(f"{Seq.apt}", True, Color.w)
    total_text = font.render(f"Total: {Seq.tpt}", True, Color.w)
    play_text = font.render("Play", True, Color.bg)
    
    tempo_label = font.render(f"Tempo: {Seq.tpo_txt}", True, Color.w)
    master_vol_text = font.render(f"Master: {int(Seq.m_vol * 100)}%", True, Color.w)
    save_text = font.render("Save", True, Color.bg)
    load_text = font.render("Load", True, Color.bg)
    menu_text = font.render(f"Mem: {Seq.s_mem}", True, Color.bg)
    
    
    screen.blit(bank_txt, (BNK_BUTTON.x + 10, BNK_BUTTON.y + 10))
    screen.blit(pattern_text, (PATTERN_BOX.x + 50, PATTERN_BOX.y + 10))
    screen.blit(total_text, (PATTERN_TOTAL.x + 10, PATTERN_TOTAL.y + 10))
    screen.blit(play_text, (PLAY_BUTTON.x + 10, PLAY_BUTTON.y + 10))
    
    screen.blit(tempo_label, (TEMPO_BOX.x + 10, TEMPO_BOX.y + 10))
    screen.blit(master_vol_text, (MASTER_VOL_BOX.x + 10, MASTER_VOL_BOX.y + 10))
    screen.blit(save_text, (SAVE_BUTTON.x + 10, SAVE_BUTTON.y + 10))
    screen.blit(load_text, (LOAD_BUTTON.x + 10, LOAD_BUTTON.y + 10))
    screen.blit(menu_text, (MENU_BUTTON.x + 10, MENU_BUTTON.y + 10))
    
    # Draw menu items (Memory)
    if Seq.m_opn:
        for i in range(MENU_ITEMS):
            menu_item_rect = pygame.Rect(MENU_BUTTON.x, MENU_BUTTON.y - (i + 1) * MENU_ITEM_HEIGHT, MENU_WIDTH, MENU_ITEM_HEIGHT)
            pygame.draw.rect(screen, Color.g, menu_item_rect)
            menu_item_text = font.render(f"Mem: {i + 1}", True, Color.bg)
            screen.blit(menu_item_text, (menu_item_rect.x + 10, menu_item_rect.y + 5))

   
    def draw_about():
        if Pestania.about == True and Pestania.sequencer_1 == False and Pestania.sequencer_2 == False and Pestania.settings == False:
            # Fondo de la pestaña
            pygame.draw.rect(screen, (50, 50, 50), (50, 50, 500, 35))
            pygame.draw.rect(screen, (20, 20, 20), (50, 85, 500, 350))

             # Título
            title_about = font_bold.render("About Bottle Beats", True, (255, 255, 255))
            screen.blit(title_about, (60, 60))

            ver.mostrar_version_(60, 100)

    draw_about()

    def draw_settings():
        if not Pestania.settings or Pestania.confirm_close == True:
            return

        # Fondo de la pestaña
        pygame.draw.rect(screen, (50, 50, 50), (50, 50, 500, 35))
        
        pygame.draw.rect(screen, (20, 20, 20), (50, 85, 500, 350))

        # Título
        title = font_bold.render("Audio Settings - Select Sound Card and Buffer", True, (255, 255, 255))
        screen.blit(title, (60, 60))

        devices = [d for d in Sound.devices if d['max_output_channels'] > 0][:12]
        current_device = sd.default.device[1] if isinstance(sd.default.device, (list, tuple)) else sd.default.device
        print("Dispositivo en funcionamiento:", current_device)
        for i, device in enumerate(devices):
            idx = Sound.devices.index(device)
            color = (0, 255, 0) if current_device == 19 else (155, 155, 155)
            device_name = f"{idx}: {device['name']} ({device['max_output_channels']} out)"
            text = font.render(device_name, True, color)
            screen.blit(text, (60, 100 + i * 20))
            device_rects[idx] = pygame.Rect(60, 100 + i * 20, 600, 20)

        #print("Dispositivo en funcionamiento ", sd.default.device)

        # Opciones de blocksize (ajustar posición según la lista filtrada)
        buffer_options = [64, 128, 256, 512]
        buffer_title = font_bold.render("Buffer Size:", True, (255, 255, 255))
        screen.blit(buffer_title, (60, 120 + len(devices) * 20 + 20))
        for i, size in enumerate(buffer_options):
            color = (0, 255, 0) if Sound.blocksize == size else (155, 155, 155)
            text = font_bold.render(str(size), True, color)
            screen.blit(text, (60 + i * 60, 120 + len(devices) * 20 + 40))
            buffer_rects[i] = pygame.Rect(60 + i * 60, 100 + len(devices) * 20 + 40, 50, 20)

    
    draw_settings()            

           
