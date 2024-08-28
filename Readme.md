# Documentation
## Server side
Server is just an API constructed using well-known flask liberary  

### Server management 
copy data to server via ssh
```
scp -p ./server-side/ root@servername:/home/user/
ssh -p root@servername
cd /home/user/server-side
python api-server.py &&
```


## raspberrypi side
raspberrypi will connected to the meter using Modbus TCP through the ethernet using modebus liberary to get the voltage and frequency readings and send it to the server end point using requests liberaries via HTTP protocole.
### Raspberrypi Manaement
copy data to raspberry pi via ssh


```
scp -p ./client-side/ pi@paspberrypi-ip:/home/pi/
ssh -p root@raspberrypi-ip
cd /home/pi/client-side
python client1.py &&
```

