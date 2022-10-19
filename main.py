from utils import *
import random

def get_session(session):
    file = open(f'{cwd}/data.json')
    data = json.load(file)
    sessions = data['sessions']
    
    if session != "": # Remove the current session from the list
        sessions.remove(session)

    return sessions[0] #picks the first recorded
    # return random.choice(sessions)\

def get_sessions():
    file = open(f'{cwd}/data.json')
    data = json.load(file)
    sessions = data['sessions']
    return sessions

def run():
    "Start The Script"

    api_client = TelegramApi()
    session = ""

    while True:
        print("Welcome, Let's get started for the day.")
        print("""
        Here are the commands;
        - Press (1) to add a new account to registry
        - Press (2) to send out messages and await response
        - Press (3) to exit the application
        - Press (4) to check SpamBot

        Watch the console closely, as any action would have an identifier here!
        """)

        response = input(">>")

        if response == "1":

            api_client.sign_in("")
            api_client.add_account()
            api_client.stop

            print("New Account Added Succcessfully 👍")


        elif response == "2":
            targetGroup = input("Input your target group invite link? ")

            used = 0

            all_sessions = get_sessions()
            for each in all_sessions:
                session = each


                print(f"Activating Account {used + 1}")

                api_client.sign_in(each)
                api_client.client.loop.run_until_complete(
                    api_client.send_messages(targetGroup, start=used*50)
                )
                api_client.stop
                used += 1

            # print("Waiting on response......")
            # api_client.run()
            print("Text Blast Done")

        elif response == "3":
            quit()

        elif response == "4":
            session = get_session(session)

            api_client.sign_in(session)

            # api_client.add_about()

            api_client.client.loop.run_until_complete(
                api_client.text_spambot()
            )

            print("Waiting on response......")
            api_client.run()


        else:
            print("You gave a wrong input. Start all over!")




if __name__ == "__main__":
    run()