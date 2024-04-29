# 📬 Instagram Auto Responder

Instagram Auto Responder is a tool that automatically responds to direct messages on Instagram using the mobile private API.

## ✨ Features

- 🚀 Auto respond to any direct threads of your Instagram account including spam inbox.
- 📩 Send custom text messages to users.
- 🕒 Adjustable wait time between responses.
- 📁 Save responded users to avoid sending multiple messages to the same user.
- 🔒 Creating lock file to prevent multiple usage of single account in the same time.


## 📋 Requirements

- Python 3.7+
- Installing libraries from `requirements.txt`

## 🚀 Getting Started

1. Clone this repository to your local machine.
2. Install the required Python modules with `pip install -r requirements.txt`.
3. Run `login.py` to start the login process. On the first run, it will guide you through the login process and create a configuration file in the `accounts` directory.
4. Run `main.py` to start the auto responder.
5. **Important:** If you force stop the script, you should delete the lock file yourself. The script won’t delete it in case of a forced stop.


## 📝 Usage

To use the Instagram Auto Responder, you need to provide your Instagram username and password. The `login.py` script will guide you through the login process and create a configuration file in the `accounts` directory. The configuration file will look like this:

```json
{
    "account": "your_instagram_username",
    "data": {
        "device_id": "your_device_id",
        "uuid": "your_uuid",
        "IG-Set-Authorization": "your_ig_set_authorization",
        "proxy": "your_proxy"
    },
    "num_replies": 5,
    "messages": ["Message 1", "Message 2", "Message 3"]
}

```

You can modify the `num_replies` field to change the number of replies the auto responder will send before stopping. The `messages` field is a list of messages that the auto responder will choose from when replying to a user. Adjust it as you need. By default the tool replies only for unread threads.



## 👥 Contributing

Hello! It's cool you are interested in contributing to this project. You are more than welcome to contribute. To ensure consistency and quality, please adhere to the following guidelines:

1. **Fork & Pull Request**: All changes must be made through a fork of the repository and a pull request. This allows to review and approve changes before they are merged into the main project.

2. **Pull Request Description**: Each pull request should include a detailed description of the changes being made. This should include the purpose of the changes, what issues they resolve, and any potential impacts.

3. **Code Review**: All pull requests must go through a code review process. You may require one or more team members to review and approve changes before they are merged.

4. **Tests**: All changes must pass tests before they are merged. You may require pull requests to include appropriate unit tests for the changes being made.

5. **Coding Standards Compliance**: All changes must comply with the project's coding standards. You may require pull requests to comply with specific coding style guidelines.


 
## ⚠️ Disclaimer
This tool is for educational purposes only. The use of this tool is your responsibility. Please respect the privacy of others and always follow terms of service.


## ⭐️ Show your support

Leave a star if that project helped you!

## 📝 License

Copyright © 2024 [Skuxblan](https://github.com/Skuxblan).
This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.
