import socket
import numpy as np
from qiskit.quantum_info import Statevector

def server_receive():
    #binding to recv data
    host=socket.gethostname()
    port=5000

    s=socket.socket()
    s.bind((host, port))
    s.listen(2)

    print('Server waiting')
    conn, addr=s.accept()
    print('Connected from: ', addr)
    while True:
        data=conn.recv(4096).decode()
        if not data:
            break
        #reconstruct statevector
        state_array=np.array(eval(data), dtype=complex)
        state=Statevector(state_array)
        # measure in Z basis, outcome bit
        outcome, collapsed = state.measure([0])

        print("Measured:", outcome)
        #print("collapsed ", collapsed)
        conn.send(str(outcome).encode())

    conn.close()
if __name__=='__main__':
        server_receive()