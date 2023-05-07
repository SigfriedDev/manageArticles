# Import controllers
from .controllers import (
    main,
    article,
    category
)


# Import modules
from os import getenv
import coloredlogs, logging
from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from .connection import engine
import src.manage.model as models

# load configuration .env
load_dotenv()

# configuration
class Config:
    ENV = getenv("SERVER_ENV")
    TESTING = False
    JSON_SORT_KEYS = False
    API_VERSION = 0.1
    API_TITLE = "API Articles"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/api"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "Bearer Auth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "bearerFormat": "JWT",
                    "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
                }
            }
        },
        "info": {
            "description": "API to Articles",
            "contact": {"email": "guillermo.fr.del@gmail.com"},
            "license": {
                "name": "Development",
                "url": "",
            },
        },
    }

    SECRET_KEY = getenv("SECRET_KEY")


# Flask start
app = Flask(__name__)
app.debug = True

# logs configuration
logging.basicConfig(format="%(asctime)s %(message)s")
coloredlogs.install(level="WARNING", logger=logging.getLogger(), isatty=True)
coloredlogs.install(level="INFO", logger=logging.getLogger(), isatty=True)

# Add configuration
app.config.from_object(Config)

api = Api(app)

# register modules
api.register_blueprint(main)
api.register_blueprint(article)
api.register_blueprint(category)



# register cors
CORS(app, supports_credentials=True)
CORS(main, supports_credentials=True)
CORS(article, supports_credentials=True)

for path, items in api.spec._paths.items():
    for method in items.keys():
        try:
            if api.spec._paths[path][method].get("authorize", False):
                api.spec._paths[path][method]["security"] = [{"Bearer Auth": []}]
        except:
            pass

# try create all models
try:
    models.db.metadata.create_all(bind=engine)
    logging.info("The models were created correctly")
except Exception as error:
    print(error)
    logging.info("No models to load")