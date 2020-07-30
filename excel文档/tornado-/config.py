import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings = {
    "template_path": os.path.join(BASE_DIR, "templates"),
    "static_path": os.path.join(BASE_DIR, "static"),
    "debug": True,
    "cookie_secret": "SBDHJKFBSIUEANSDOQINXZ"
}