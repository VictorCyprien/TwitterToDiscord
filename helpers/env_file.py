from environs import Env, EnvError

def get_env_config():
    env = Env()
    env.read_env()

    try:
        env("TWIITER_LOGIN_EMAIL")
    except EnvError:
        print("TWIITER_LOGIN_EMAIL is not set !")
        exit(0)

    try:
        env("TWITTER_LOGIN_USERNAME")
    except EnvError:
        print("TWITTER_LOGIN_USERNAME is not set !")
        exit(0)

    try:
        env("TWITTER_LOGIN_PASSWORD")
    except EnvError:
        print("TWITTER_LOGIN_PASSWORD is not set !")
        exit(0)

    try:
        env("TWITTER_BEARER_AUTH")
    except EnvError:
        print("TWITTER_BEARER_AUTH is not set !")
        exit(0)

    try:
        env("DISCORD_BOT_TOKEN")
    except EnvError:
        print("DISCORD_BOT_TOKEN is not set !")
        exit(0)

    return env
