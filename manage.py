from app import create_app
from core.database import db
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
