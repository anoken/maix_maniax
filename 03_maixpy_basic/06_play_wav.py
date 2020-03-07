## Copyright (c) 2019 aNoken

from fpioa_manager import *
from Maix import I2S, GPIO
import audio

##Speaker I2S Initialize
AUDIO_PA_EN_PIN = 2     # Maixduino
fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
spk_sd=GPIO(GPIO.GPIO1, GPIO.OUT)
spk_sd.value(1)

# register i2s(i2s0) pin
fm.register(34,fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35,fm.fpioa.I2S0_SCLK, force=True)
fm.register(33,fm.fpioa.I2S0_WS, force=True)

wav_dev = I2S(I2S.DEVICE_0)

##wav file play
def play_wav(fname):
    player = audio.Audio(path = fname)
    player.volume(1)
    wav_info = player.play_process(wav_dev)
    wav_dev.channel_config(wav_dev.CHANNEL_1,
        I2S.TRANSMITTER,resolution = I2S.RESOLUTION_16_BIT,
        align_mode = I2S.STANDARD_MODE)
    wav_dev.set_sample_rate(wav_info[1])
    while True:
        ret = player.play()
        if ret == None:
            break
        elif ret==0:
            break
    player.finish()


play_wav("test.wav")
player.finish()