from pathlib import Path
import logging

def get_logger(source):
    project_dir = Path(__file__).parents[1]  
    log_dir = project_dir/"logs"

    log_file = log_dir/f"{source}.log"

    if not log_dir.exists():
        log_dir.mkdir()

    logger = logging.getLogger(source)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file)
    formater = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    handler.setFormatter(formater)
    logger.addHandler(handler)

    return logger
