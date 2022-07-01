from movie import app
import config
from movie import smptyserver

if __name__ == "__main__":
    app.run(port=config.PORT, debug=True)
    smptyserver.quit()

