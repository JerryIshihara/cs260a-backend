from config import app
import os

if __name__ == "__main__":
    # app.run(host=os.environ["HOST"], port=int(os.environ["PORT"]), debug=True)
    app.run(host=os.environ["HOST"], port=3000, debug=True)
