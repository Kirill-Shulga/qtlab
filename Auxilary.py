import numpy as np
from playsound import playsound
import urllib, requests
from datetime import datetime as dt
import telegram
from time import sleep
from IPython.display import clear_output

#Sound library
def zero_sound():
    playsound(r'C:\\qtlab_replacement\\voise\\zero.mp3')
def complete_sound():
    playsound(r'C:\\qtlab_replacement\\voise\\complete.mp3')    
def stable_sound():
    playsound(r'C:\\qtlab_replacement\\voise\\stable.mp3')  
def lockin_complete_sound():
    playsound(r'C:\\qtlab_replacement\\voise\\lockin_complete.mp3')
def magnetic_stable_sound():
    playsound(r'C:\\qtlab_replacement\\voise\\magnetic_stable.mp3')    
    
#Telegram notification library    
def telegram_notification(message, token_id, chat_id):
    now = dt.now() # current date and time
    time = now.strftime("%d/%m/%Y, %H:%M:%S")
    l_msg = time +"\n" + message

    url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (
        token_id, chat_id, urllib.parse.quote_plus(l_msg))
    _ = requests.get(url, timeout=10)   
    
def telegram_photo_notification(message, path, token_id, chat_id):
    bot = telegram.Bot(token=token_id)
    bot.send_message(chat_id=chat_id, text=message)
    bot.send_photo(chat_id=chat_id, photo=open(path, 'rb'))
    
#unit transformation library
def freq_to_field(frequency):
    return frequency/28
def field_to_freq(field):
    return field*28
def kelvin_to_GHz(kelvin):
    return 20.8334*kelvin
def GHz_to_kelvin(GHz):
    return 0.048*GHz

def get_mult_freq(frequency):
    return frequency/12
def get_der_freq(frequency):
    return frequency*12

#Voltage sourse library
def ramp_3_sourses(BC,BM,BO, src_list, token_id, chat_id, sound = True, notification = True):
    BC_BM_BO = np.array([BC,BM,BO])                                   # Final values in [Volts]
    STEP = 0.03                                                       # Value of the step in [Volts]

    BC_BM_BO_now = np.array([src_list[0].get_voltage(),src_list[1].get_voltage(),src_list[2].get_voltage()])

    number_list = [abs(BC_BM_BO[0]-BC_BM_BO_now[0]),abs(BC_BM_BO[1]-BC_BM_BO_now[1]),abs(BC_BM_BO[2]-BC_BM_BO_now[2])]
    max_value = max(number_list)
    max_index = number_list.index(max_value)
    steps_BC = list(np.linspace(BC_BM_BO_now[0], BC_BM_BO[0], int(number_list[0]/STEP+1)))
    steps_BM = list(np.linspace(BC_BM_BO_now[1], BC_BM_BO[1], int(number_list[1]/STEP+1)))
    steps_BO = list(np.linspace(BC_BM_BO_now[2], BC_BM_BO[2], int(number_list[2]/STEP+1)))
    for i in np.linspace(BC_BM_BO_now[max_index], BC_BM_BO[max_index], int(number_list[max_index]/STEP+1)):
        clear_output(wait=True)
        if len(steps_BC):
            src_list[0].set_voltage(steps_BC[0])
            steps_BC.pop(0)
        if len(steps_BM):
            src_list[1].set_voltage(steps_BM[0])
            steps_BM.pop(0)
        if len(steps_BO):
            src_list[2].set_voltage(steps_BO[0])
            steps_BO.pop(0)
        sleep(0.1)
    if sound:
        stable_sound()
    if notification:
        telegram_notification('The Voltage is stable', token_id, chat_id)
    
#Magnet library
def status():
    magnet_state = int(magnet.get_rampingstate())
    if (magnet_state == 1):
        print('RAMPING to target field/current')
    if (magnet_state == 2):
        print('HOLDING at the target field/current')
    if (magnet_state == 3):
        print('PAUSED')
    if (magnet_state == 4):
        print('Ramping in MANUAL UP mode')
    if (magnet_state == 5):
        print('Ramping in MANUAL DOWN mode')
    if (magnet_state == 6):
        print('ZEROING CURRENT (in progress)')
    if (magnet_state == 7):
        print('Quench detected')
    if (magnet_state == 8):
        print('At ZERO current')
    if (magnet_state == 9):
        print('Heating persistent switch')
    if (magnet_state == 10):
        print('Cooling persistent switch')