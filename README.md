# Blockchain_SimpCoin
Blockchain project for a cryptocurrency. Has website running to access and add to elements of the chain. Working on database implementation.

Requirements: python3, flask, pip, etc...

***I recommend being inside a virtual environment. Here's a tutorial for pip and venv: https://packaging.python.org/guides/installing-using-pip-and-virtualenv/

In order to run the program, type: py app.py (if on windows) or python3 app.py(if on mac). This will run along with threads for server.py as well.
App.py acts as ledger for blockchain, server.py has UDP server and client functionality. Client sends udp broadcasts; UDP server receives broadcasts and sends
a POST request to the server ledger with its information (encrypted NONCE and peerlist) to which the ledger responds with the reincrypted information and peerlist.

Running the server through app.py also gives access to HTML online through several routes

Routes:
/peers route (for list of peers) or /peers?mode=json (returns JSON representation of peers)
/transactions (blockchain displayed) or /transactions?start=[insert number] (blockchain starting a specific index)
/transactions/<ID> (block at given ID)

Blockchain code is stored in mainfile.py
Encryption code is in EncryptUTIL.py
Key Generation code is in Keygen.py
