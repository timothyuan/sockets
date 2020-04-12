# CS176A Socket Project

## Project Summary

This python project implements client-server communication via TCP and UDP sockets.

## Installation Prerequisites

- Python (v3.7.3)
- Libraries/Frameworks: socket, sys, time, subprocess, os, unittest, mock

## Running the code
The following example is the TCP implementation. Running the UDP is the exact same, just substitute the respective scripts for client and server.3.
1. Open a terminal window and run the server with port number as a command line argument
<pre>
python server_python_tcp.py 65432
</pre>
2. Open another terminal window and start the client
<pre>
python client_python_tcp.py
</pre>
3. You will be prompted to enter a series of inputs by the clients, a completed prompt is shown below
<pre>
Enter server name or IP address: localhost
Enter port: 65432
Enter command: ls > output.txt
</pre>
Note: All commands must be in the form command > file.txt, where file.txt is the name of the file saved on the server. File saved on the client side is called client_output.txt.

## Running tests
You can run the test the exact same way you run the server and client scripts.
<pre>
python test_client_tcp.py
python test_server_tcp.py
python test_client_udp.py
python test_server_udp.py
</pre>

## References and Useful Links
[Python socket documentation](https://docs.python.org/3/library/socket.html)

[Python mock documentation](https://docs.python.org/3/library/unittest.mock.html#patch-object)

[UDP example](https://stackoverflow.com/questions/27893804/udp-client-server-socket-in-python)

[Set timeout across multiple socket operations](https://stackoverflow.com/questions/34371096/how-to-use-python-socket-settimeout-properly/54419091)
