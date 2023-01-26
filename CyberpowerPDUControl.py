import asyncio, telnetlib3
import time

class CyberpowerPDUControl:
    def __init__(self):
        # Constructor
        self.username = "cyber"
        self.password = "cyber"
        self.host = "10.3.230.88" # Example PDU IP only
        self.socket_number = "1"
        self.command = "on"
        
    def set_socket(self, state, socket_number):
        # Set socket state
        # state (string) is either "on" or "off"
        # socket_number is an integer between 1~8 corresponding to the socket of the PDU
        
        self.socket_number = str(socket_number)
        self.command = str(state)
        asyncio.set_event_loop(asyncio.SelectorEventLoop()) # Workaround for connection error in telnetlib3
        loop = asyncio.get_event_loop() 
        coro = telnetlib3.open_connection(self.host, 23, shell=self.shell)
        print("Running telnet loop until complete")
        reader, writer = loop.run_until_complete(coro)
        print("Running loop")
        loop.run_until_complete(writer.protocol.waiter_closed)
        print("Finished asyncio loop")

    async def shell(self, reader, writer):
        # Async function used to telnet into the PDU controller
        initial_time = time.time()
        while True:
            if (time.time() - initial_time) > 30:
                break # Make sure telnet not entered for too long
            # read stream until '?' mark is found
            outp = await reader.read(1024)
            print(outp)

            if not outp:
                # End of File
                print("Invalid input")
            elif 'Login Name:' in outp:
                print("Detected login")
                writer.write(f"\n{self.username}\n\r")
                time.sleep(0.1)
            elif 'Login Password:' in outp:
                print("Detected password")
                writer.write(f"\n{self.password}\n\r")
                time.sleep(0.1)
            elif 'CyberPower >' in outp:
                print("Toggling outlet")
                print(f"oltctrl index {self.socket_number} act {self.command}")
                time.sleep(0.1)
                writer.write(f"\noltctrl index {self.socket_number} act {self.command}\n\r")
                time.sleep(0.1)
                writer.write(f"\nexit\n\r")
                break

        print("Exiting telnet")

if __name__ == "__main__":
    print("Unit Testing")
    
    command = input("Enter status:")
    pdu_control = CyberpowerPDUControl()
    pdu_control.set_socket(command,1)    
    
    print("Done!")
