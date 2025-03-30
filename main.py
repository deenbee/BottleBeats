import pygame
#import wiringpi
import os
from config.variables import Pestania, Color, Sound, screen
from src.jsncodes import load_settings, save_settings
from src.handle import update_sequencer, handle_input, Botones
from src.draw_ui import draw_ui, draw_steps
from src.audio import save_audio



# Comando shell para ejecutar el código según el driver del sonido
# sudo SDL_AUDIODRIVER=alsa AUDIODEV=hw:1,0 python3 v2b.py

load_settings() # Load saved settings (Colors & Sound Card)


if not os.path.exists("presets"):
    os.makedirs("presets")

# Bucle principal
running = True
clock = pygame.time.Clock()

#print(f"Seq.Seq.tpo_txt inicial: {Seq.Seq.tpo_txt}")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Pestania.confirm_clse() # Muesta mensaje de confirmacion 
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Control del pulsacion de objeto
            Botones.copy_paste(event.pos)
            Botones.write_mode_button(event.pos)
            Botones.handle_pattern_numbers(event.pos)
            Botones.handle_patterns(event.pos)
            
            running = Pestania.close(event.pos, running) # Si se confirma el cierre manda False para cerrar

            handle_input(event.pos)
            
        elif event.type == pygame.KEYDOWN:
            print("Tecla presionada")
            """
            if Seq.tempo_BOX.collidepoint(pygame.mouse.get_pos()):
                if event.key == pygame.K_BACKSPACE:
                    print("")
                    #Seq.tpo_txt = Seq.tpo_txt[:-1]
                elif event.key == pygame.K_RETURN:
                    try:
                        print("")
                        #Seq.tempo = int(Seq.tpo_txt)
                    except ValueError:
                        print("")
                        #Seq.tempo = 100
                    #Seq.tpo_txt = str(Seq.tempo)
                elif event.unicode.isdigit():
                    print("")
                    #Seq.tpo_txt += event.unicode"""

    screen.fill(Color.bg)
    
    Botones.reset_colors_copy_paste()               # Resetea los colores de los botones copy y paste
    Botones.reset_colors_flechas_song_position()
    
    draw_steps()
    draw_ui()
    update_sequencer()

    #print("Song position (Seq.apt)", Seq.apt, "Seq.patt_state ", Seq.patt_state[Seq.apt - 1], " Seleccion(Seq.pattern_num)", Seq.pattern_num, " Seq.Patt ", Seq.patt)
        
    pygame.display.flip()
    clock.tick(60)
   # Apagar todos los LEDs al salir
   #for pin in led_pins:
   #wiringpi.digitalWrite(pin, 0)



save_settings()
save_audio(Sound.default_device, Sound.blocksize)
pygame.quit()