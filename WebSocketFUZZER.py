#!/usr/bin/python
# 
# WebSocketFuzzer
# V.1.0
# 
# Ignacio Lizaso - Red Team
# python2 .\WebSocketFUZZER.py -u  wss://websocketserver -f 1 -m msg.txt -a auth.txt
#_______________________________________________________________________________________________________

# [SESSION] will be injected with the session header after authentication.
# [Fuzz1] Will be injected with /?fuzz1=VALUE

# Reemplace values in the msg.txt with [FUZZ#]
# and use the URL to fuzz them ej: http://127.0.0.1/fuzz1=foo&fuuz2=faa&fuzz3=fiii
# In this case use the flag -f 3 to indicate that there are 3 fuzzing possitions.

# You cloud use sqlmap like sqlmap -U "http://127.0.0.1/fuzz1=foo&fuuz2=faa&fuzz3=fiii" or even do a normal web scanning.

import socket,ssl
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from websocket import create_connection, WebSocket
from urlparse import parse_qs
import os
import re
import argparse

FUZZ = 1
LOOP_BACK_PORT_NUMBER = 7000
SC = None
WSM = None

def FuzzWebSocket(qs):
    global WSM
    global SC

    #print fuzz_value
    try:
        tmp = WSM
        for i in range(1, FUZZ+1, 1):
            tmp = tmp.replace("[FUZZ"+str(i)+"]", str(qs["fuzz"+str(i)][0]))
        
        SC.send(tmp)

        result =  SC.recv()
        print(result)
        return result
    except:
        print("Error fuzzeando este payload")
        generate_ws()
        

class myWebServer(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        #try:
        qs = parse_qs(self.path[2:])

        result = FuzzWebSocket(qs)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(result)
        return
        #except:
        #    print("")


def load_Server():
    global SC

    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', LOOP_BACK_PORT_NUMBER), myWebServer)
        print('Started httpserver on port ' , LOOP_BACK_PORT_NUMBER)
        
        #Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
        SC.close()

def generate_ws():
    if(args.proxy is not None):
        try:
            proxy = args.proxy.split(':')
        except Exception as e :
            print("[-] Error Setting Proxy({}): {}".format(e.__class__.__name__, e))
        ws = create_connection(args.url,sslopt={"cert_reqs": ssl.CERT_NONE},header={},http_proxy_host=proxy[0], http_proxy_port=proxy[1])
    else:
        ws = create_connection(args.url)

    if(args.msg_file is not None):
        print(args.msg_file)
        try:
            with open(args.msg_file, 'r') as msg_file:
                ws_message = msg_file.read()
                ws_message = (ws_message.encode('hex') + '00').decode('hex')
        except Exception as e:
                print("[-] Error Reading Message File({}): {}".format(e.__class__.__name__, e))


    if(args.auth_file is not None):
        try:
            with open(args.auth_file, 'r') as auth_file:
                auth_message = auth_file.read()
                auth_message = auth_message.encode('hex').replace("0a", "0d0a") + "00"
        except Exception as e:
                print("[-] Error Reading Auth File({}): {}".format(e.__class__.__name__, e))


        print("Autenticando...")
        try:
            ws.send(auth_message.decode("hex"))
            result =  ws.recv()
            print(result)
            session = re.findall("session:session-.*",result)[0]
            print("Sesion =  "+ session)
            ws_message = ws_message.replace("[SESSION]", session)

        except Exception as e:
            print("[-] Error Autenticando({}): {}".format(e.__class__.__name__, e))
    


    print("\n_________________________________\n"+ws_message+"\n_________________________________\n")

    global SC
    global WSM

    SC = ws
    WSM = ws_message

def main(args):

    generate_ws()
    
    load_Server()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'python .\WebSocketFUZZER.py -u  wss://bleble.com:8443/ws -f 1 -m msg.txt -a auth.txt')
    parser.add_argument('-u','--url', help='The remote WebSocket URL to target.  wss://bleble.com:8443/ws',required=True)
    parser.add_argument('-m','--msg_file', help='Message file', required=True)
    parser.add_argument('-a','--auth_file', help='Auth file')
    parser.add_argument('-p','--proxy', help='Proxy host:port')
    parser.add_argument('-f','--fuzz', help='Number of Fuzz Parameters', required=True, type=int)

    args = parser.parse_args()

    FUZZ = args.fuzz


    main(args)