from init import get_token, get_updater


def main():
    token = get_token()  # Getting Bot Token from a file
    updater = get_updater(token)  # Bot Updater (Function for initiation)
    updater.start_polling()  # Bot Start Function


def debug():
    ...


if __name__ == '__main__':
    main()
