from machine import Pin, UART
import network
import espnow
import time
import neopixel

num_leds = 32
pin_num = 6

neoRing = neopixel.NeoPixel(Pin(pin_num), num_leds)

uart1 = UART(1, baudrate=9600, bits = 8, parity=None, stop=1, tx=39, rx=37)

#A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

peer = b'\x80\x65\x99\xe2\x6F\x78'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()

############################################################################################ 
# NeoPixel Ring/strip    

# 
# def fade_in():
#     
#     for n in range(0,255, 4):
#         for i in range(num_leds):
#             neoRing[i] = (n,0,0)
#             neoRing.write()
#            
# 
#         
# 
# def loop_all():
#         fade_in()
#         for i in range(num_leds):
#             neoRing[i] = (255,0,0)
#         neoRing.write()
#         
#         
#    

############################################################################################


while True:
    
    sender = uart1.read()
    print(sender)
    time.sleep(1)
    
    if sender == b'LED ON':
        e.send(peer, "LED ON")
    elif sender == b'LED OFF':    
        e.send(peer, "LED OFF")
        
#  for i in range(num_leds):
#                 neoRing[i] = (0,0,0)
#             neoRing.write()


    