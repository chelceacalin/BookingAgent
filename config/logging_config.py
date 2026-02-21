import logging

class ColorLogFormatter(logging.Formatter):
    RESET  = "\x1b[0m"
    GREY   = "\x1b[38;5;245m"
    GREEN  = "\x1b[38;5;40m"
    YELLOW = "\x1b[38;5;220m"
    RED    = "\x1b[38;5;196m"
    CYAN   = "\x1b[38;5;51m"
    BLUE   = "\x1b[38;5;39m"

    LEVEL_COLORS = {
        logging.DEBUG:   GREY,
        logging.INFO:    GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR:   RED,
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, self.RESET)
        time     = f"{self.GREY}{self.formatTime(record, '%Y-%m-%d %H:%M:%S')}{self.RESET}"
        level    = f"{color}{record.levelname:<5}{self.RESET}"
        location = f"{self.CYAN}{record.name}{self.RESET}:{self.BLUE}{record.funcName}{self.RESET}:{self.GREY}{record.lineno}{self.RESET}"
        message  = f"{color}{record.getMessage()}{self.RESET}"
        return f"{time}  {level}  {location}  ---  {message}"


for noisy in ["httpx", "google_genai", "google_genai.models", "httpcore"]:
    logging.getLogger(noisy).setLevel(logging.CRITICAL)

handler = logging.StreamHandler()
handler.setFormatter(ColorLogFormatter())

root = logging.getLogger()
root.setLevel(logging.INFO)
root.handlers.clear()
root.addHandler(handler)

logger = logging.getLogger(__name__)