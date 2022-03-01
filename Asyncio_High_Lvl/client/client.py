import asyncio
import async_input as ai
import async_input_control as aic


class Client():
    def __init__(self, bind_ip, bind_port):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.Loop = asyncio.get_event_loop()
        self.start_up()

    def start_up(self):
        self.Server_Task = self.Loop.create_task(
            self._run_client(), name='client')
        self.Loop.run_forever

    async def _run_client(self):
        self.client = await asyncio.start_server(self.handle_recv, host=self.bind_ip, port=self.bind_port)
        async with self.client:
            print(f'listing on {self.bind_ip},{self.bind_port}')
            await self.client.serve_forever()

    async def handle_recv(self, reader, writer):
        data = await reader.read(100)
        register = writer.get_extra_info('peername')
        print(register)
        message = data.decode()
        print(message)
        message_start = message[0:3]

        if message_start == "sen":  # message = "sen,source portnumber,destiny portnumber,message"
            self.print_message(message[4:])
        elif message_start == "add":  # message = add,source port,destiny port
            await self.add_client(message[4:])

    def print_message(self, messager):
        source_port = messager[0:3]
        print(f"{source_port}: {messager}")

    async def add_client(self, message):
        source_port = message[0:3]
        print(f"do you wanna add{source_port}?")
        i = await asyncio.create_task(ai.loop_for_input())
        while True:
            if i == "1":
                print("accept")
                break
                # TODO: Function to send this feedback back to the server
            elif i == "2":
                print("reject")
                break
            else:
                "wrong input try again"

    async def get_send_input(self):
        print("please enter destiny port")
        p = await aic.input_control()  # Ungetestet
        print("please enter message")
        i = await asyncio.create_task(ai.loop_for_input())
        return p, i

    async def tcp_send_client(self):

        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8000)
        print("1 for connection to the server, 2 for disconnection from the server, 3 for sending a message, 4 for adding a client")
        while True:
            input = await asyncio.create_task(ai.loop_for_input())
            if input == "1":
                message = f"con,{self.bind_port}"
                break
            elif input == "2":
                message = f"dis,{self.bind_port}"
                break
            elif input == "3":
                p, i = await self.get_send_input()
                # message = "sen,source portnumber,destiny portnumber,message"
                message = f"sen,{self.bind_port},{p},{i}"
                break
            elif input == "4":
                print("please give port for adding")
                i = await asyncio.create_task(ai.loop_for_input())
                # message = add,source port,destiny port
                message = f"add,{self.bind_port},{i}"
                break
            elif input == "5":
                exit()
            else:
                print("Wrong input please try again")

        print(f'Send: {message!r}')
        writer.write(message.encode())
        writer.close()


async def main():
    print("what port do you wanna use?")

    while True:
        try:
            i = await asyncio.create_task(ai.loop_for_input())
            p = int(i)
        except ValueError:
            print('Valid number, please')
            continue
        if 5000 <= p <= 8000:
            break
        else:
            print("please choose a number between 5000 and 8000")
            continue

    print("1 for exit, 2 for sending a message")
    inputTask = await asyncio.create_task(ai.loop_for_input())
    client = Client("127.0.0.1", p)

    while True:

        if inputTask == "1":
            exit()
        elif inputTask == "2":
            await client.tcp_send_client()


asyncio.run(main())
