import logging

# Create a global logger
logger = logging.getLogger("global_logger")
logger.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Optional: create a file handler if you want logs in a file too
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)

# Create formatter and add to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
