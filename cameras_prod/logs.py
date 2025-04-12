from datetime import datetime


def log_message(message):
    # Create a timestamp for the log
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Combine the timestamp with the message
    log_entry = f"{timestamp} - {message}"

    # Print the message to the console
    print(log_entry)

    # Append the log entry to the log file
    with open('log_data.log', 'a') as log_file:
        log_file.write(log_entry + '\n')