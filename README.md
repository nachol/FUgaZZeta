# FUgaZZeta

Web socket proxy for fuzzing.

It connects to a web socket and loads a normal web site to be scanned with common tools

    python2 .\WebSocketFUZZER.py -u  wss://websocketserver -f 1 -m msg.txt -a auth.txt

    -u     The remote WebSocket URL to target
    -m      Message File
    -a      Auth File for websocket
    -p      Proxy server ej 127.0.0.1:8080
    -f      Number of fuzzing parameters


auth.txt Example:


    CONNECT
    version:1.1,1.0
    login:john
    passcode:doe
    heart-beat:16000,0
    host:/



msg.txt Example:

    SEND
    destination:/exchange/appin.request
    reply-to:/temp-queue/21cc7cac-69bc-4c37-9142-922f1bf62055
    correlation-id:16f9b4ff-0ffb-4145-820e-f66959fd58d3
    [SESSION]

    <Request><Header><Id>[FUZZ1]</Id></Header></Request>
_______________________________________________________________________

Running example:


    python2 .\WebSocketFUZZER.py -u  wss://websocketserver -f 1 -m msg.txt -a auth.txt


    sqlmap.exe -u "http://127.0.0.1:7000/?fuzz1=1&fuzz2=1&fuzz3=1" --level 5 --risk 3 --dbs


![](https://raw.githubusercontent.com/nachol/FUgaZZeta/master/img.jpg)
