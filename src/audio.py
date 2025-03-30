import json

def load_audio_settings():
    m_file = f"config/audio.json"
    try:
        with open(m_file, "r") as f:
            audio_data = json.load(f)
            value = audio_data["Output"]

            return value
    
    except FileNotFoundError:
        print("Audio device file not found")
        return 0
    
    except Exception as e:
        print("Error audio")

        return 0


def load_audio_buffer():
    m_file = f"config/audio.json"
    try:
        with open(m_file, "r") as f:
            audio_data = json.load(f)
            value = audio_data["Buffer"]
            print("Buffer cargado con exito ", value)
            return value
    
    except FileNotFoundError:
        print("Audio buffer file not found")
        return 512
    
    except Exception as e:
        print("Error audio buffer")

        return 512


def save_audio(default_value, buffer):
    audio_data = {
        "Output": default_value,
        "Buffer": buffer
    }
    m_file = f"config/audio.json"
    with open(m_file, "w") as f:
        json.dump(audio_data, f)
        print("Default audio device saved")
