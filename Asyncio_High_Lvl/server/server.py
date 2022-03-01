import asyncio
import async_input as ai
from asyncio import streams


# all operations that are done on the register of the different clients
# TODO: implement register
class register():
    pass

# class for creating servers with asyncio libary


class Server():
    # takes IP,port,loop and register to create a server object
    def __init__(self, bind_ip, bind_port):
        self.Loop = asyncio.get_event_loop()
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.register = []
        self.start_up()

    # starts up a asyncio task with the function _run_server and the name server
    # adds it to the loop of the Server class and runs it for ever
    def start_up(self):
        self.Server_Task = self.Loop.create_task(
            self._run_server(), name='server')
        self.Loop.run_forever

    # starts a asyncio server with the method start_server
    # takes the handle_recv method,ip and port,
    # every time the server gets a input from this port he starts a new couroutine with handle_recv
    async def _run_server(self):
        self.Server = await asyncio.start_server(self.handle_recv, host=self.bind_ip, port=self.bind_port)
        async with self.Server:
            print(f'listing on {self.bind_ip},{self.bind_port}')
            await self.Server.serve_forever()

    # streams the data that has been send to the ip and port ans saves it in the variable data
    # gets the information form which adress the data has been send and saves it in register
    # searchs for the keywords con,dis or sen to start the next action.
    async def handle_recv(self, reader, writer):
        data = await reader.read(100)
        register = writer.get_extra_info('peername')
        print(register)  # test
        message = data.decode()
        print(message)  # test
        message_start = message[0:3]

        if message_start == "con":  # message = “con,portnumber”
            await self.register_client(message[4:])
        elif message_start == "dis":  # message = “dis,portnumber”
            await self.unregister_client(message[4:])
        elif message_start == "sen":  # message = "sen,source portnumber,destiny portnumber,message"
            await self.send_message(message[4:])
        elif message_start == "add":  # message = add,source port,destiny port
            await self.add_client(message[4:])

    # takes a ip and port to create with open_conncetion a connection,
    # message gets encoded to bytecode and send via writer.write
    # after that the connection gets closed
    async def handle_send(self, message, port):
        reader, writer = await asyncio.open_connection('127.0.0.1', port)
        writer.write(message.encode())
        print('Close the connection')
        writer.close()

    async def register_client(self, adress):
        self.register.append(adress)
        print(f"{adress} is added to register")
        print(self.register)

    async def unregister_client(self, adress):
        self.register.remove(adress)
        print(f"{adress}, is removed")

    # gets the message from a client and splits it into source port, destiny port and payload.
    # if both port in the registry the server will send the payload to the destiny port.
    async def send_message(self, message):
        send_port = message[0:4]
        receive_port = message[5:9]
        payload = message[10:]
        if send_port in self.register:
            if receive_port in self.register:  # optimierbar
                # sen,source portnumber,destiny portnumber,message"
                await self.handle_send(f"sen,{send_port},{receive_port},{payload}", receive_port)

    # gets the add requests and sends this to the destiny port

    async def add_client(self, message):
        send_port = message[0:4]
        receive_port = message[5:9]
        if send_port in self.register:
            if receive_port in self.register:
                await self.handle_send(f"add,{send_port},{receive_port}")


async def main():
    server = Server("127.0.0.1", 8000)
    while True:
        i = await ai.loop_for_input()
        if i == "1":
            exit()

asyncio.run(main())
