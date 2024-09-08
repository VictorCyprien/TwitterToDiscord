class ErrorHandler():
    NO_COOKIES_IN_DATABASE = "No cookies found, please push new cookies data to the database"
    COOKIES_EXPIRED = "Unable to get the latest data, please refresh cookies"
    ENV_NOT_SET = "Please set an environement in .env file"
    REQUESTS_ERROR = "Something wrong with requests, please refresh cookies"
    USER_ERROR = "User not found because of cookies, please refresh cookies"
    DATABASE_ERROR_CONNECT = "Unable to connect to MongoDB, please check the url"
    DISCORD_MSG_ERROR = "Quelque chose s'est mal passé"
    
