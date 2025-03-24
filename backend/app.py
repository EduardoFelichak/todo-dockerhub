from flask           import Flask
from config.database import db, init_db
from routes.task     import task_bp
from dotenv          import load_dotenv
from flask_cors      import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_db(app)

app.register_blueprint(task_bp, url_prefix = "/api/tasks")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000)
