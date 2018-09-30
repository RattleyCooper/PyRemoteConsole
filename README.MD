# PyRemoteConsole

PyRemoteConsole contains hooks for connecting to running
python scripts remotely.  It contains a pure-python 
"encryption" scheme that is used to *obfuscate* 
communication between the client and the server.

### Install

    pip install PyRemoteConsole


### Setup & Usage

The key file that comes with PyRemoteConsole will work
but you should generate a new key by running the 
`obfuscation.py` file.  You should see the following 
text:

    Generating key...
    Key generated.
    Validating key for prosperity...
    Key is valid.  Encryptor working successfully!

A key should never fail, but it's validated anyway.

Even repeating words and patterns will generate unique
cipher-text:

    hello hello hello hello hello hello hello hello
    ̬ĮʀÀ
    (ŬǊɢʷMfǱċǚϺ-éȼ˭̕ȿïɐǅƹ{əʺʙΦΑțϾɚɛ͜ǙʡƽǛť
    
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    ΧϬʸΟϫ«͚ǣϱȐ˩ȍ3͜p̚ĺ̒bĘʇɅ͋Ƚďɏ͛ʬƥƏƼʌˢ͊ǝͅ#ȇƄƩŨ϶Ǖ³¾

Anything sent and received while using the built-in 
encryption should be considered un-readable, but not 
necessarily secure.

### Client & Server

If you have `script_A.py` and want to be able to connect
to it while it's running you need to include code from
the `client.py` file.

```python
from PyRemoteConsole.client import Client, run_command_client
```

`run_command_client` should be launched in an additional
thread.

```python
from threading import Thread
from time import sleep

host = '10.0.0.2'
port = 12347
includes = {'a': 'Some object'}
t = Thread(target=run_command_client, args=[host, port], kwargs={'includes': includes})
t.start()
```

use the `includes` kwarg to pass whatever objects you want to
have access to remotely. i.e. `includes = {'some_obj': 'obj_val'}`

`Client` tracks events that happen in the `run_command_client` 
thread and also allows you to shut down the `run_command_client`
loop safely.

```python
Client.restart = True
Client.shutdown = True
while Client.alive:
    sleep(0.05)
t.join()
```

To connect to the script running the `run_command_client` thread
you need to import `run_server` from the `server.py` file.

```python
from PyRemoteConsole.server import run_server

host = 10.0.0.2
port = 12347
run_server(host, port)
```


