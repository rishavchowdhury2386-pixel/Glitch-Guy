import wave
import struct
import math

def generate_retro_music(filename="theme.wav"):
    # Audio parameters
    sample_rate = 44100
    duration = 8.0 # seconds
    
    # Open wave file
    wav_file = wave.open(filename, 'w')
    wav_file.setnchannels(1) # Mono
    wav_file.setsampwidth(2) # 2 bytes per sample (16-bit)
    wav_file.setframerate(sample_rate)
    
    # Melody notes (frequencies in Hz)
    # Mario-ish / retro simple melody
    notes = [
        (659.25, 0.15), (659.25, 0.15), (0, 0.15), (659.25, 0.15), (0, 0.15),
        (523.25, 0.15), (659.25, 0.15), (0, 0.15), (783.99, 0.3),  (0, 0.3),
        (392.00, 0.3),  (0, 0.3)
    ]
    
    # Repeat melody to fill duration
    sequence = []
    while sum(d for f, d in sequence) < duration:
        sequence.extend(notes)
        
    for freq, dur in sequence:
        num_samples = int(sample_rate * dur)
        for i in range(num_samples):
            if freq == 0:
                sample = 0
            else:
                # Square wave for retro feel
                t = i / sample_rate
                val = math.sin(2.0 * math.pi * freq * t)
                sample = 8000 if val > 0 else -8000
                
            packed_sample = struct.pack('<h', int(sample))
            wav_file.writeframes(packed_sample)
            
    wav_file.close()

if __name__ == "__main__":
    generate_retro_music()
