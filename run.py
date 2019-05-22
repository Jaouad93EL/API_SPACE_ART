from src.app import create_app
import numbers
import random

if __name__ == '__main__':
    letters = numbers.ABCMeta
    ok = random.choice(letters)
    print(ok)
    app = create_app()
    app.run()