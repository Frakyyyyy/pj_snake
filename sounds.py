import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        """Загрузка звуков"""
        try:
            # Создаем простые звуки (в реальном проекте загружайте файлы)
            self.sounds['eat'] = self.create_beep_sound(800, 100)
            self.sounds['crash'] = self.create_beep_sound(200, 400)
            self.sounds['menu'] = self.create_beep_sound(500, 50)
        except:
            print("Не удалось создать звуки")
            
    def create_beep_sound(self, frequency, duration):
        """Создание простого звукового сигнала"""
        import numpy as np
        
        sample_rate = 44100
        n_samples = int(round(duration * 0.001 * sample_rate))
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(16 - 1) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            buf[i][0] = int(round(max_sample * 0.5 * np.sin(2 * np.pi * frequency * t)))
            buf[i][1] = int(round(max_sample * 0.5 * np.sin(2 * np.pi * frequency * t)))
            
        return pygame.sndarray.make_sound(buf)
    
    def play_eat(self):
        """Звук съедания еды"""
        if 'eat' in self.sounds:
            self.sounds['eat'].play()
            
    def play_crash(self):
        """Звук столкновения"""
        if 'crash' in self.sounds:
            self.sounds['crash'].play()
            
    def play_menu(self):
        """Звук меню"""
        if 'menu' in self.sounds:
            self.sounds['menu'].play()
            
    def create_background_music(self):
        """Создание простой фоновой музыки"""
        import numpy as np
        from io import BytesIO
        
        sample_rate = 44100
        duration = 2.0  # секунды
        n_samples = int(duration * sample_rate)
        
        t = np.linspace(0, duration, n_samples)
        
        # Простая мелодия
        wave1 = 0.3 * np.sin(2 * np.pi * 262 * t)  # C
        wave2 = 0.3 * np.sin(2 * np.pi * 330 * t)  # E
        wave3 = 0.3 * np.sin(2 * np.pi * 392 * t)  # G
        
        wave = wave1 + wave2 + wave3
        wave = np.int16(wave * 32767)
        
        stereo_wave = np.column_stack((wave, wave))
        
        # Сохраняем в буфер
        buffer = BytesIO()
        import wave as wave_module
        with wave_module.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(stereo_wave.tobytes())
            
        buffer.seek(0)
        return buffer
            
    def stop_music(self):
        """Остановка музыки"""
        pygame.mixer.music.stop()