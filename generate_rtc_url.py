from secrets import choice


def gen_token():
    valid_token_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    token = ""
    for i in range(16):
        token += choice(valid_token_chars)
    return token


def gen_url():
    return f"wss://blokegaming.com/robitcontrol/webrtcsignal/{gen_token()}/"


if __name__ == "__main__":
    print(gen_url())
