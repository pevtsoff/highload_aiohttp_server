# Highload AIOHTTP Server

This small client/server application has been created for demonstration of the asyncio power. It can easily handle thousands concurrent http connections in just one asyncio thread. I tested it with 15000 connections and it was working fine. 

### Server Description:
Once connected, the server continuosly writes the response for each connection by small chunks (chunk_size param). For this purpose I have used StreamResponse class

### Client Descriptoin
The client is using response content streaming features and writes all the data coming from http connection to a separate file. The chunk_size param defines the size for each read.


## How to run:
1.Extend Open files limits on your system. On linux I have done it with this command:

```ulimit -Sn 65535```

2.Launch server:
```python3 fast_server.py```

3.Launch client:
```python3 fast_client.py```