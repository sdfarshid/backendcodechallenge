import logging
import sys
from pathlib import Path

log_dir = Path(__file__).parent.parent / "logs"

print(Path(__file__))
print(log_dir)

log_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

commit_logger = logging.getLogger("commit_logger")
commit_logger.setLevel(logging.INFO)


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)



if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

if not commit_logger.hasHandlers():
    commit_logger.addHandler(file_handler)


def DebugWaring(message: object) -> object:
    logger.debug(f" *** --  {message}  --*** ")


def DebugError(message):
    logger.debug(f" ****--  {message} --***")

