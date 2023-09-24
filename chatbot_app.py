import redis
import random
import time

class Chatbot:
    def __init__(self, host='redis', port=6379):
        self.client = redis.StrictRedis(host=host, port=port)
        self.pubsub = self.client.pubsub()
        self.username = None

    def introduce(self):
        # Provide an introduction and list of commands
        intro = """
        Hello! I'm a friendly Redis chatbot.
        Here are some commands you can use:
        !help: List of commands
        !weather <city>: Weather update
        !fact: Random fun fact
        !whoami: Your user information
        !channels: list all the channels
        """
        print(intro)

    def add_user(self, username):
        # Store user details in Redis
        search_key = f"user:{username}"
        actions = ["create", "update"]
        if self.client.sismember("username_set", search_key): 
            print(f"\n-- Lets {actions[1]} {username}'s profile. Press enter to skip the information you prefer not to provide.")
        else:
            self.client.sadd("username_set", search_key)   # Set a simple key for fast existence check using set
            print(f"\n-- Lets {actions[0]} {username}'s profile. Press enter to skip the information you prefer not to provide.")
        
        self.username = username
        age = input("Enter your age please (Press enter to skip): ").strip()
        if not age.isdigit():
            age = False
        gender = input("Enter your gender [Female/Male/Other/Press enter to skip]: ").strip()
        location = input("Enter your location (Press enter to skip): ").strip()
        
        user_info = {
            "username": username,
            "age": age or -1,
            "gender": gender or "Not provided",
            "location": location or "Not provided"
        }

        self.client.hset(search_key, mapping=user_info) 
        print(f"Successfully managed {username}'s profile!")

    def identify(self, username):
        # user login
        search_key = f"user:{username}"
        if self.client.sismember("username_set", search_key):
            self.username = username
            print(f"Welcome back {username}!")
        else:
            self.add_user(username)
            
    
    def join_channel(self, channel):
        # Join a channel
        self.pubsub.subscribe(channel)
        print(f'Successfully join the {channel} channel!')

    def leave_channel(self, channel):
        # Leave a channel
        self.pubsub.unsubscribe(channel)
        print(f'Successfully Leave the {channel} channel!')

    def send_message(self, channel, message):
        # subscribe to a channel if haven't
        all_channels = set([chs.decode('utf-8') for chs in bot.client.pubsub_channels()])
        if channel not in all_channels:
            self.join_channel(channel)
        
        # Send a message to a channel
        print(f"Send message to {channel} channel.")
        self.client.publish(channel, message)

    def read_message(self, channel, wait_time=60):
        end_time = time.time() + wait_time
        while time.time() < end_time:
            # Try to get a message with a timeout (using a short interval here like 1 second)
            msg = self.pubsub.get_message(timeout=1)
            if msg and msg['type'] == 'message':
                print(f"[{channel}] {msg['data'].decode('utf-8')}")



    def process_commands(self, message):
        # Handle special chatbot commands
        # !help: List of commands
        # !weather <city>: Weather update
        # !fact: Random fun fact
        # !whoami: Your user information
        # !channels: list all the channels
        message = message.lower()
        if message.startswith("!help"):
            self.introduce()
        elif message.startswith("!weather"):
            city = " ".join(message.split(" ")[1:]).title()
            weather = self.client.hgetall(city)
            print(f"Weather in {city}: ")
            for k, v in weather.items():
                print(f"{k.decode('utf-8')}: {v.decode('utf-8')}")

        elif message.startswith("!fact"):
            # randomly select number from 1 tp 47
            random_num = random.randint(1, 47)
            fun_fact_to_get = f"Fact {random_num}"
            random_fact = self.client.get(fun_fact_to_get)
            print(f"A random fun fact: {random_fact.decode('utf-8')}")
        elif message.startswith("!whoami"):
            if self.username is None:
                print("Sorry, you haven't logged in yet.")
            else:
                search_key = f"user:{self.username}"
                get_usr_info = self.client.hgetall(search_key)
                print(f"Your user information:")
                for k, v in get_usr_info.items():
                    print(f"{k.decode('utf-8')}: {v.decode('utf-8')}")
        elif message.startswith("!channels"):
            print("List of channels: ")
            for channel in self.client.pubsub_channels():
                print(channel.decode('utf-8'))
        else:
            print("Sorry, I don't understand this command. Please try again.")
            self.introduce()


    def direct_message(self, message):
        # Send a direct message to the chatbot
        pass

if __name__ == "__main__":
    bot = Chatbot()
    bot.introduce()
    option_msg = """
    
------------------------------------
    Options:
    1. Identify yourself
    2. Update your profile
    3. Get info about a user
    4. Join a channel
    5. Leave a channel
    6. Send a message to a channel 
    7. Read messages from a channel
    8. Exit
    """  

    while True:
        try:
            print(option_msg) 
            interaction = input("Enter your choice/command: ").strip()
            if interaction.isdigit():
                interaction = int(interaction)

                if interaction == 1:
                    username = input("Enter your username please: ")
                    if not username.strip():
                        print("Sorry, username is required.")
                    bot.identify(username)
                elif interaction == 2:
                    username = input("Enter your username please: ")
                    if not username.strip():
                        print("Sorry, username is required.")
                    bot.add_user(username)
                elif interaction == 3:
                    username = input("Enter the username you want to get info about: ").strip()
                    search_key = f"user:{username}"
                    user_info = bot.client.hgetall(search_key)
                    if not user_info:
                        print("Sorry, this user does not exist.")
                    else:
                        print(f"Info for {username}: ")
                        for k, v in user_info.items():
                            if k.decode('utf-8') == "username":
                                continue
                            print(f"{k.decode('utf-8')}: {v.decode('utf-8')}")
                elif interaction == 4:
                    channel = input("Enter the channel you want to join: ").strip()
                    bot.join_channel(channel)
                elif interaction == 5:
                    channel = input("Enter the channel you want to leave: ").strip()
                    bot.leave_channel(channel)   
                elif interaction == 6:
                    channel = input("Enter the channel you want to send message to: ").strip()
                    message = input("Enter the message you want to send: ").strip()
                    bot.send_message(channel, message)
                elif interaction == 7:
                    channel = input("Enter the channel you want to read messages from: ").strip()
                    all_channels = set([chs.decode('utf-8') for chs in bot.client.pubsub_channels()])
                    if channel not in all_channels:
                        print(f"Sorry, please join the {channel} channel first. Only the messages published after you join will be shown.")
                    else:
                        bot.read_message(channel)
                    
                elif interaction == 8:
                    print("Bye!")
                    break
                else:
                    print("Sorry this is a invalid input. Please try again or enter 8 to exit.")
            elif interaction.startswith("!"):
                bot.process_commands(interaction)
            else:
                print("Sorry I cannot understand. Please try again or enter 8 to exit.")
                

        except Exception as e:
            print(f"Error: {e}")
            print("Sorry there is something wrong. Please try again or enter 8 to exit.")


    
