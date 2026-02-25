import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import socket

#we transmit the description of the qubit
def prepare_qubit(state_type="1"):
    """
    state type we'll have: 
        0  -> |0>
        1  -> |1>
        +  -> |+>
        -  -> |->
    """ 
    # create a 1 qubit circuit
    qc = QuantumCircuit(1)

    if state_type=='0':
        #default case, on fait rien
        qc.id(0)
    if state_type=='1':
        #x gate=> |0> -> |1>
        qc.x(0)
    elif state_type=='+':
        #hadamard gate to make superposition :(+ = (0+1)/sqrt(2))
        qc.h(0)
    elif state_type== '-':
        #z gate 
        qc.h(0)
        qc.z(0)

    """statevector : used to simulate les mesures d'états quantiques
    if + it gives: [0.70.., 0.70..] 
    if - it gives: [0.70.., -0.70..]
"""
    state=Statevector.from_instruction(qc)
    return state


def client_send(state_type):
    #transmission using sockets
    host=socket.gethostname()
    port=5000
    c=socket.socket()
    c.connect((host,port))
    
    state=prepare_qubit(state_type)
    print("Client sending statevector: ", state.data)
    c.send(str(list(state.data)).encode())
    
    result=c.recv(4096).decode()
    print("Server measured: ", result)

    c.close()


if __name__=='__main__':
    state_to_send='1'
    client_send(state_type=state_to_send)