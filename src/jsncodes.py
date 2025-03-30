import json
from config.variables import Seq, Patt, Sound, Samples, Color


def load_settings():
    
    m_file = f"config/settings.json"
    try:
        with open(m_file, "r") as f:
            settings_data = json.load(f)
            Color.g = settings_data["Color.g"]
            Color.r = settings_data["Color.r"]
            Color.w = settings_data["Color.w"]
            Color.gn = settings_data["Color.gn"]
            Color.bg = settings_data["Color.bg"]
            print(f"Load settings ok")
    except FileNotFoundError:
        print(f"No find settings file")
        #device = None
        #buffer = 256
        Color.g = (150, 150, 150)
        Color.r = (255, 0, 0)
        Color.w = (255, 255, 255)
        Color.gn = (0, 255, 0)
        Color.bg = (0, 0, 0)
    except Exception as e:
        print(f"Error load settings file: {e}")
        Color.g = (150, 150, 150)
        Color.r = (255, 0, 0)
        Color.w = (255, 255, 255)
        Color.gn = (0, 255, 0)
        Color.bg = (0, 0, 0)

    

def save_settings():
   
    settings_data = {
        #"default_device": device_data,
        #"default_buffer": Sound.blocksize,
        "Color.g": Color.g,
        "Color.r": Color.r,
        "Color.w": Color.w,
        "Color.gn": Color.gn,
        "Color.bg": Color.bg,
    }
    m_file = f"config/settings.json"
    with open(m_file, "w") as f:
        json.dump(settings_data, f)
    print("Settings saved")



     

def save_preset():
    preset_data = {
        "Patt.mtx_p": Patt.mtx_p,
        "Seq.apt": Seq.apt,
        "Seq.tpt": Seq.tpt,
        "Seq.sq2_note": Seq.sq2_note,
        "Seq.txt2_note": Seq.txt2_note,
        "Seq.patt_state": Seq.patt_state,
        "Samples.wav_files": Samples.wav_files,
        "Seq.channel_volumes": Seq.channel_volumes,
        "Seq.tones": Seq.tones,
        "Seq.pan_volumes": Seq.pan_volumes,
        "Seq.m_vol": Seq.m_vol,
        "Seq.tempo": Seq.tempo,
        "Color.g": Color.g,
        "Color.r": Color.r,
        "Color.w": Color.w,
        "Color.gn": Color.gn,
        "Color.bg": Color.bg,
    }
    # Imprime los datos para encontrar el problema
    for clave, valor in preset_data.items():
        print(f"{clave}: {type(valor)} - {valor}")
    memory_file = f"presets/memory_{Seq.s_mem}.json"
    with open(memory_file, "w") as f:
        json.dump(preset_data, f)
    print(f"Preset guardado en memoria {Seq.s_mem} ({memory_file})")
    
def load_preset(Color=0):
    
    memory_file = f"presets/memory_{Seq.s_mem}.json"
    try:
        with open(memory_file, "r") as f:
            preset_data = json.load(f)
            Patt.mtx_p = preset_data["Patt.mtx_p"]
            Seq.apt = preset_data["Seq.apt"]
            Seq.tpt = preset_data["Seq.tpt"]
            Seq.sq2_note = preset_data["Seq.sq2_note"]
            Seq.txt2_note = preset_data["Seq.txt2_note"]
            Seq.patt_state = preset_data["Seq.patt_state"]
            Samples.wav_files = preset_data["Samples.wav_files"]
            Seq.channel_volumes = preset_data.get("Seq.channel_volumes", [1.0] * 24)
            Seq.tones = preset_data["Seq.tones"]
            Seq.pan_volumes = preset_data.get("Seq.pan_volumes", [0.0] * 24)
            Seq.m_vol = preset_data.get("Seq.m_vol", 1.0)
            Seq.tempo = preset_data["Seq.tempo"]
            Color.g = preset_data["Color.g"]
            Color.r = preset_data["Color.r"]
            Color.w = preset_data["Color.w"]
            Color.bg = preset_data["Color.bg"]
            select_bank = preset_data["select_bank"]
            Sound.load_samples_banks(select_bank)
            Seq.tpo_txt = str(Seq.tempo)

                        
            print(f"Preset cargado desde memoria {Seq.s_mem} ({memory_file})")
    except FileNotFoundError:
            print(f"No se encontró un preset en la memoria {Seq.s_mem}. Se creará uno al guardar.")
    except Exception as e:
            print(f"Error al cargar el preset desde memoria {Seq.s_mem}: {e}")



    