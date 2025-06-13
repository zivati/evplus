import logging

def setup_logger():
    logging.basicConfig(
        filename="bot.log",
        format="%(asctime)s %(levelname)s %(message)s",
        level=logging.INFO
    )

def backup_data(data):
    import json
    with open("backup.json", "w") as f:
        json.dump(data, f)
