from datetime import datetime


def log_message(message):
    # Combine the timestamp with the message
    log_entry = f"{message}"

    # Print the message to the console
    print(log_entry)

    # Append the log entry to the log file
    with open('log_data.log', 'a') as log_file:
        log_file.write(log_entry + '\n')
