from flask_frozen import Freezer
from project import main


if __name__ == '__main__':
    main.freezer.freeze()
