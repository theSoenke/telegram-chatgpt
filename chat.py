# from pychatgpt import Chat
from pyChatGPT import ChatGPT


class Chat():
    def __init__(self) -> None:
        session_token = 'abc123'  # `__Secure-next-auth.session-token` cookie from https://chat.openai.com/chat
        api1 = ChatGPT(session_token)  # auth with session token
        api2 = ChatGPT(session_token, proxy='http://proxy.example.com:8080')  # specify proxy
        api3 = ChatGPT(auth_type='google', email='example@gmail.com', password='password') # auth with google login
        api4 = ChatGPT(session_token, verbose=True)  # verbose mode (print debug messages)


        resp = api1.send_message('Hello, world!')
        print(resp['message'])

        # api1.reset_conversation()  # reset the conversation
        # api1.close()  # close the session
