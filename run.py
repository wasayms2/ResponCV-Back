from app import app
import os

FLASK_ENV = os.getenv("FLASK_ENV")


# Checking if we are running using docker
# Sets the port accordingly
# Needed to deploy to Azure
if(FLASK_ENV=="docker"):
	PORT = 80
else:
	PORT = 5000


if __name__ == "__main__":
    app.run(port=PORT, host="0.0.0.0")