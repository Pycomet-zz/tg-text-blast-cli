from curses import reset_shell_mode
from telethon import client
from config import *

class TelegramApi:

    def __init__(self) -> None:
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.receivers = []
        self.client = None
    
    @property
    def get_proxy(self):
        proxy = {
            'proxy_type': socks.SOCKS5,
            'addr': '127.0.0.1',
            'port': 8100,
            'username': 'username',
            'password': 'password',
            'rdns': False
        }
        return proxy

    
    @property
    def start(self):
        self.loop = asyncio.new_event_loop()
        self.client = TelegramClient(StringSession(), API_ID, API_HASH, loop=self.loop)
        
        # self.client = TelegramClient(
        #     StringSession(),
        #     self.api_id,
        #     self.api_hash,
        #     connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
        #     proxy=('127.0.0.1', 3000, '00000000000000000000000000000000')
        # )

    def sign_in(self, session:str):
        "Sign In A Session ID"
        if self.client is not None:
            self.stop
        self.loop = asyncio.new_event_loop()

        # print(session)
        self.client = TelegramClient(StringSession(session), API_ID, API_HASH, loop=self.loop).start()
        user = self.client.loop.run_until_complete(self.client.get_me())
        print(f"Signed In As {user.first_name} ({user.id}) ({user.phone})")

    @property
    def session(self):
        return self.client.session.save()

    @property
    def stop(self):
        self.client.disconnect()

    def write_to_json(self, session:str):
        "Write Session to Database"
        file = open(f'{cwd}/data.json')
        data = json.load(file)

        # add session
        data['sessions'].append(session)
        with open(f'{cwd}/data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def check_receiver(self, user_id:int) -> bool:
        "Checks the receivers file if user_id exists"
        file = open(f'{cwd}/users.json')
        data = json.load(file)

        #check user_id
        for user in data["users"]:
            if user == user_id:
                return True
            else:
                pass
        return False

    def update_receivers(self):
        "Update the users.json file with newly sent message user Ids"
        file = open(f'{cwd}/users.json')
        data = json.load(file)

        for each in self.receivers:
            data["users"].append(each)

        with open(f'{cwd}/users.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)



    def add_about(self):
        "Add Bio & User Picture to new Account"
        # Add proxy
        # import pdb; pdb.set_trace()
        self.client.set_proxy(self.get_proxy)
        self.client.loop.run_until_complete(
            self.client(UpdateProfileRequest(
                about="Crypto Investment Expert - www.archoptions.com"
            ))
        )

        group = self.client.loop.run_until_complete(
            self.client.get_entity('@teleescrowtest')
        )
        self.client.loop.run_until_complete(
            self.client(JoinChannelRequest(group))
        )

        # self.client.loop.run_until_complete(
        #     self.client(UploadProfilePhotoRequest(
        #         file=self.client.upload_file(f"{cwd}/photo.jpeg")
        #     ))
        # )

        # self.client.loop.run_until_complete(
        #     self.client(UploadProfilePhotoRequest(
        #         f"{cwd}/photo.jpeg"
        #     )
        # )

        # self.client.lo
        return

    def get_user_data(self):
        "Return user object"
        data = self.client.loop.run_until_complete(
            self.client.get_me()
        )
        return data



    def add_account(self):
        "Verifies A New User Account"
        session = self.session
        self.write_to_json(session)

        return {
            "session" : session
        }

    


    async def send_messages(self, target:str, start:int):
        "Fetch Participants from group to an array"
        try:
            group = await self.client.get_entity(target)
            # entity = [ print(e) async for e in self.client.iter_participants(target) ]
            # print(len(entity))
            # self.client.loop.run_until_complete(
            #     asyncio.sleep(0.5)
            # )
            await asyncio.sleep(2)
            await self.client(JoinChannelRequest(group))

            index = 0

            async for each in self.client.iter_participants(target):

                # await asyncio.sleep(2)
                if start > index:
                    index += 1
                    pass
                else:

                    user = await self.client.get_entity(each.id)

                    isExisting = self.check_receiver(each.id)

                    if each.id not in self.receivers and isExisting == False:
                        self.receivers.append(each.id)
                        
                        # # import pdb; pdb.set_trace()
                        # await self.client.send_file(each.id, f"{cwd}/nyoki.jpg")
                        
                        
                        
                        for msg in data['message']:

                            # Write User Filter In Condition
                            status = str(each.status).split('(')[0]
                            if each.bot == False and status in ["UserStatusRecently", "UserStatusOnline"]:

                                if each.username != None:
                                    text = msg.replace("$USERNAME", each.username)
                                else:
                                    text = msg.replace("$USERNAME", "")
                                

                                await self.client.send_message(user.id, text)
                                print(f"Sent To - {user.first_name}")
                                await asyncio.sleep(0.5)

                            else:
                                pass
                        else:
                            pass

            self.update_receivers()
            return True
                    
        except Exception as e:
            print(e)
            print("Failed attempt! You inputed invalid data for this script.")
            self.update_receivers()
            return False

    async def text_spambot(self):
        try:
            await self.client.send_message(
                '@SpamBot',
                "/start"
            )
        except Exception as e:
            print(e)
            print("No Messaging")
    
    async def request_handler(self, event):
        print(event)
        try:
            sender = event.message.peer_id
            message = event.message
            print(f"New Message Alert - {message}")

            # if event.out == False and sender in self.receivers:
            if event.message.out == False:
                # import pdb; pdb.set_trace()

                
                    await self.client.forward_messages(
                        'crytoexpert',
                        message.id,
                        sender
                    )


                
                # await self.client.send_message(
                #     sender,
                #     "Please contact @codefred for more details and resources to help you get started."
                # )
                # self.receivers.remove(sender)
            else:
                pass
        except AttributeError:
            try:
                print(event.message.message)
            except AttributeError:
                pass
        except Exception as e:
            print(e)


    def run(self):
        "Runs The Listening Handler"
        self.client.add_event_handler(self.request_handler)
        print(".....")
        self.client.run_until_disconnected()

