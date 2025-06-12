# TwitterToDiscord Bot

A powerful Discord bot that monitors Twitter (X) accounts for new followings and provides comprehensive Twitter analytics directly in your Discord server.

## 🚀 Features

### Core Functionality

- **Real-time Following Monitoring**: Automatically tracks when monitored Twitter accounts follow new users
- **Discord Notifications**: Sends rich embed notifications to specified Discord channels when new followings are detected
- **Multi-account Support**: Monitor multiple Twitter accounts simultaneously
- **Periodic Checks**: Runs automated checks every 15 minutes for new followings

### Analytics & Data Export

- **Follower Analysis**: Export complete follower lists for any Twitter account to Excel
- **Following Analysis**: Export complete following lists for any Twitter account to Excel
- **User Management**: Add/remove Twitter profiles from monitoring list
- **Data Visualization**: Rich Discord embeds with user information, follower counts, and profile details

### Discord Slash Commands

- `/add_twitter_profile <username> <channel>` - Add a Twitter profile to monitor
- `/remove_twitter_profile <username>` - Remove a Twitter profile from monitoring
- `/get_list` - Get Excel file with all monitored users
- `/get_followers <username>` - Export follower list for a specific user
- `/get_followings <username>` - Export following list for a specific user
- `/talk` - Simple bot health check

## 🛠️ Technology Stack

- **Python 3.x** - Core programming language
- **discord.py** - Discord bot framework
- **MongoDB** - Database for storing user data and configurations
- **aiohttp** - Asynchronous HTTP client for Twitter API calls
- **Playwright** - Browser automation for cookie extraction
- **pandas & openpyxl** - Data processing and Excel file generation
- **Docker** - Containerization and deployment

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB instance
- Discord Bot Token
- Twitter Bearer Token and valid cookies
- Docker (optional, for containerized deployment)

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TwitterToDiscord
```

### 2. Environment Setup

#### Option A: Virtual Environment (Recommended)

```bash
make install
```

#### Option B: Manual Setup

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file with the following variables:

```env
# Twitter Configuration
TWITTER_BEARER_AUTH=your_twitter_bearer_token
TWITTER_LOGIN_EMAIL=your_twitter_email
TWITTER_LOGIN_USERNAME=your_twitter_username
TWITTER_LOGIN_PASSWORD=your_twitter_password
TWITTER_LOGIN_PHONE=your_twitter_phone

# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_BOT_TOKEN_DEV=your_development_bot_token

# Database Configuration
MONGODB_URL=mongodb://localhost:27017

# Environment
ENVIRONMENT=PROD  # or DEV
```

### 4. Twitter Cookies Setup

The bot requires valid Twitter session cookies. Use the `export_cookies.py` script to extract cookies from your browser:

```bash
python export_cookies.py
```

This will generate a `cookies.json` file required for Twitter API authentication.

### 5. Database Setup

#### Option A: Using Docker (Recommended)

```bash
make build_db
```

#### Option B: Local MongoDB

Ensure MongoDB is running on your system and accessible via the configured URL.

## 🚀 Running the Bot

### Development Mode

```bash
make run
```

### Production Mode with Docker

#### Build and Run Application

```bash
make build_image
make build_container
```

#### Using Docker Compose

```bash
docker-compose up -d
```

### View Logs

```bash
make logs
```

## 📁 Project Structure

```bash
TwitterToDiscord/
├── main.py                 # Main Discord bot application
├── twitter.py              # Twitter API interaction functions
├── export_cookies.py       # Cookie extraction utility
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── makefile              # Build and deployment commands
├── helpers/              # Utility functions
│   ├── __init__.py
│   ├── pandas_file.py    # Excel file operations
│   ├── mongo_file.py     # MongoDB operations
│   ├── logging_file.py   # Logging utilities
│   ├── env_file.py       # Environment configuration
│   ├── futures_file.py   # Async task handling
│   ├── errors_file.py    # Error handling
│   └── cleaning_file.py  # File cleanup utilities
├── discord_helpers/      # Discord-specific utilities
│   ├── __init__.py
│   ├── build_msg.py      # Message building functions
│   └── set_activity.py   # Bot activity management
└── extract_helpers/      # Data extraction utilities
    ├── __init__.py
    ├── entities.py       # Entity extraction
    └── extract_users_infos.py  # User information extraction
```

## 🔧 Configuration Details

### MongoDB Collections

The bot uses the following MongoDB collections:

- **users**: Stores monitored Twitter profiles and their configuration

  ```json
  {
    "_id": "twitter_user_id",
    "username": "twitter_username",
    "latest_following": "last_followed_user",
    "notifying_discord_channel": "discord_channel_id",
    "last_check": "timestamp"
  }
  ```

- **cookies**: Stores Twitter authentication cookies

  ```json
  {
    "name": "cookie_name",
    "value": "cookie_value",
    "domain": ".twitter.com"
  }
  ```

### Bot Permissions

Ensure your Discord bot has the following permissions:

- Send Messages
- Use Slash Commands
- Attach Files
- Embed Links
- Read Message History

## 🔄 How It Works

1. **Initialization**: Bot connects to Discord and MongoDB, syncs slash commands
2. **Monitoring Setup**: Users add Twitter profiles via `/add_twitter_profile` command
3. **Periodic Checks**: Every 15 minutes, the bot checks for new followings on monitored accounts
4. **Notification System**: When new followings are detected, rich embed notifications are sent to configured Discord channels
5. **Data Export**: Users can request follower/following data exports via slash commands
6. **Async Processing**: Large data exports are processed asynchronously with progress notifications

## 🛡️ Security Considerations

- **Sensitive Data**: Never commit `.env` files or `cookies.json` to version control
- **Token Management**: Regularly rotate Discord bot tokens and Twitter bearer tokens
- **Database Security**: Ensure MongoDB is properly secured in production environments
- **Rate Limiting**: The bot respects Twitter API rate limits to avoid suspension

## 🚨 Troubleshooting

### Common Issues

1. **Authentication Errors (403)**
   - Check Twitter cookies validity
   - Verify bearer token is correct
   - Ensure CSRF token is properly extracted

2. **Database Connection Issues**
   - Verify MongoDB is running
   - Check connection string in `.env`
   - Ensure network connectivity

3. **Discord Bot Not Responding**
   - Verify bot token is valid
   - Check bot permissions in Discord server
   - Review logs for error messages

### Debugging

Enable detailed logging by checking the logs:

```bash
make logs  # For Docker deployment
# or check console output for local deployment
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚖️ License

This project is intended for educational and personal use. Please ensure compliance with Twitter's Terms of Service and API usage policies.

## 🤝 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the logs for error details
3. Create an issue in the repository with detailed information about your problem

## 📊 Performance Notes

- **Memory Usage**: Approximately 2GB RAM recommended for optimal performance
- **CPU**: 1 CPU core sufficient for typical usage
- **Storage**: Minimal storage requirements, mainly for temporary Excel files
- **Network**: Requires stable internet connection for Twitter API calls

---

**Note**: This bot requires valid Twitter authentication and respects Twitter's rate limiting. Ensure you have proper authorization to monitor the Twitter accounts you configure.
