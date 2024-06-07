try:
  import usocket as socket
except:
  import socket
from machine import Pin, UART
import network
import time
import gc
gc.collect()



uart1 = UART(1, baudrate=9600, bits = 8, parity=None, stop=1, tx=39, rx=37)


ssid = 'MONSTERS_LED'
password = 'PASSWORD'

##################################################################################################################
# WebPage

def web_page(led_state):
    html = """<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.5.1/css/all.css"
    <script src="https://kit.fontawesome.com/27b11a1a08.js" crossorigin="anonymous"></script>
    <style>
        html {
            font-family: Arial;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            width: 110px;
            border: none;
            color: white;
            padding: 16px 20px;
            text-align: center;
            text-decoration: none;

            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 20px;
        }

        .button1 {
            background-color: #000000;
        }

        .button3{
            background-color: #4207f2; 
            width: 100px;
        }
        #icon{
            margin: 4px 2px;
        }
    </style>
</head>

<body>
    <h2>Monsters Inc. Light Control</h2>
    <p>LED state: <strong>""" + f"{led_state}" + """</strong></p>
    <p>
        <i class="fa-solid fa-lightbulb fa-2x" data-fa-transform="down-6" id="icon" style="color:#c81919;"></i>
        <a href=\"led_on\"><button class="button">LED ON</button></a>
    </p>
    <p>
        <i class="fa-regular fa-lightbulb fa-2x" data-fa-transform="down-6" id="icon" style="color:#000000;"></i>
        <a href=\"led_off\"><button class="button button1">LED OFF</button></a>
    </p>
    <p>
        <i class="fa-solid fa-rotate-right fa-2x" data-fa-transform="down-6" id="icon" style="color: #0420f2;"></i>
        <a href=\"loop_demo\"><button class="button button3">DEMO</button></a>
    </p>

</body>

</html>"""
    
    return html


############################################################################################

# Main Connect

def ap_mode(ssid, password):
    
    # Just making our internet connection
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.config(max_clients=5)
    ap.active(True)
    
    while ap.active() == False:
        pass

    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
#     addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
# 
#     s = socket.socket()
#     s.bind(addr)
    s.bind(('', 80))
    s.listen(5)

    led_state = "OFF"
    global position
    
   

    while True:
        
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))
        conn.settimeout(None)
        request = str(request)
        led_on = request.find('/led_on')
        led_off = request.find('/led_off')
        led_demo = request.find('/loop_demo')
        if led_on == 6:
            print('LED ON -> GPIO15')
            led_state = "ON"
            uart1.write('LED ON')
            
        if led_off == 6:
            print('LED OFF -> GPIO15')
            led_state = "OFF"
            uart1.write('LED OFF')


           

#         if led_demo == 6:
#             print('LED DEMO -> GPIO15 && GPIO6')
#             led_state = "Demo Finished"
#             for i in range(5):
#                 loop_all()
#                 i += 1
#                 time.sleep_ms(1)
#             
#             
#             for i in range(num_leds):
#                 neoRing[i] = (0,0,0)
#                 neoRing.write()
        
        response = web_page(led_state)
        conn.send(response)
        conn.close()
      
ap_mode('MONSTERS_LED', 
        'PASSWORD')




