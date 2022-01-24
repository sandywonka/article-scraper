from models import Bisnis, Antaranews


class controller(object):
    def __init__(self):
        Bisnis.scrap()
        Antaranews.scrap()


if __name__ == "__main__":
    try:
        controller()
    except:
        pass
