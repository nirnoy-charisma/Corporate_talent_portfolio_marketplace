import os
from flask import Flask
from dotenv import load_dotenv
from models import db
from models.user import User
from models import db
from models.user import User
from models.individual_profile import IndividualProfile
from models.company_profile import CompanyProfile
from models.portfolio_attachment import PortfolioAttachment
from routes.auth import auth_bp
from flask import render_template
from routes.portfolio import portfolio_bp
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.register_blueprint(auth_bp)
    from routes.portfolio import portfolio_bp

    app.register_blueprint(portfolio_bp)
    db.init_app(app)

    with app.app_context():
        db.create_all()  # creates tables based on models that exist so far

    return app

app = create_app()



@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)