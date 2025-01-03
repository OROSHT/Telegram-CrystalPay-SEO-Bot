# SEO BOT Setup

This guide will walk you through the installation and configuration of the CrystalPAY SEO BOT. Follow these steps to get your bot up and running.

## Installation

### 1. Install Python
- Download and install Python from the [official Python website](https://www.python.org/downloads/).
- During installation, make sure to check the box that says "Add Python to PATH".

### 2. Clone the Repository

## Configuration

### 1. Edit `config.py`
Open `config.py` and configure the following settings:

![11e6347b6f008a3482590](https://github.com/user-attachments/assets/f2eb07e4-ab1b-4f24-8219-f501c6a1c38b)

- **bot_token**: Enter the token of your bot obtained from [BotFather](https://t.me/botfather). Put it between quotes.
  
- **admin_ids**: List the Telegram ID(s) of the bot admin(s). If you are the only admin, enter your ID between brackets. For multiple admins, separate IDs with commas. Example: `[29083490, 2340389]`.

- **Crystalpay**:
  - **secret_1**: Enter the Secret 1 token from [CrystalPAY Bot](https://t.me/CrystalPAY_bot).
  - **secret_2**: Enter the Secret 2 token from CrystalPAY Bot.
  - **login**: Enter the login name for your CrystalPAY account between quotes.

- **price**: Set the price for one SEO boost.

- **worker_percent**: Define the percentage that each worker will receive from each SEO boost.

- **Lolz**:
  - **lolz_token**: Obtain your API token from Lolz by creating an application. Set the application name, description, and redirect URI to any value. Click "Get Token", select your application, grant all permissions, and copy the token. Paste it between quotes.
  - **user_id**: Your Lolz profile user ID. Find this in the profile settings under "Page Permanent Link" and enter the numbers.
    ![95710efa42238f4240299](https://github.com/user-attachments/assets/a279de47-c46a-401b-adac-6ab3e8838d15)
  - **secret_answer**: Enter the secret answer from your market.

### 2. Install Dependencies
Upload your files to a server or local machine, then open a command prompt (cmd). Navigate to the directory containing `main.py` using the `cd` command. For example:
```bash
cd C:\Users\username\Desktop\seo_bot\
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Bot
Start the bot by executing:
```bash
python main.py
```

The bot is now up and running!

## Contribution

If you would like to contribute to this project, please leave a star in the repo.

## License

This project is licensed under the MIT. For more information, see the [License](LICENSE).