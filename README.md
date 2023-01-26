# cyberpower_pdu
Control cyberpower PDU status using telnet (cyberpower pdu 41001)

# Setup
Python 3.7+

# Libraries

In commandline, install the following libraries

pip install telnetlib3

pip install asyncio

# Examples

## Turning socket 1 on
command = "on"
pdu_control = CyberpowerPDUControl()
pdu_control.set_socket(command,1) 


## Turning socket 1 off
command = "off"
pdu_control = CyberpowerPDUControl()
pdu_control.set_socket(command,1) 
