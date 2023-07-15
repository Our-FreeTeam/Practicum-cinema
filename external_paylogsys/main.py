from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
import datetime
import json

app = Flask(__name__)

# Setup the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs_db.db'  # Changed this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the model for the table
class WebhookEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ip_address = db.Column(db.String, nullable=False)  # New field for IP address
    data = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<WebhookEvent %r>' % self.id


def create_tables():
    with app.app_context():
        db.create_all()


@app.route('/webhook', methods=['POST'])
def respond():
    try:
        data = request.json
        ip_address = request.remote_addr  # Get client's IP address
        event = WebhookEvent(data=json.dumps(data),
                             ip_address=ip_address)  # Include IP address when creating event
        db.session.add(event)
        db.session.commit()

        return jsonify(status='OK')
    except Exception as e:
        print(e)
        return jsonify(status='ERROR', message=str(e)), 500


@app.route('/get_logs', methods=['GET'])
def get_logs():
    try:
        current_date = datetime.date.today()
        events = WebhookEvent.query.filter(func.date(WebhookEvent.timestamp) == current_date).all()

        return jsonify(logs=[
            {"id": event.id, "pay_data": json.loads(event.data)} for event in events])
    except Exception as e:
        print(e)
        return jsonify(status='ERROR', message=str(e)), 500


@app.route('/get_last_log', methods=['GET'])
def get_last_log():
    try:
        current_date = datetime.date.today()
        last_event = WebhookEvent.query.filter(
            func.date(WebhookEvent.timestamp) == current_date).order_by(
            desc(WebhookEvent.id)).first()

        if last_event:
            return jsonify(logs={"pay_data": json.loads(last_event.data)})
        else:
            return jsonify(logs={})
    except Exception as e:
        print(e)
        return jsonify(status='ERROR', message=str(e)), 500


if __name__ == "__main__":
    create_tables()
    app.run(host='0.0.0.0', port=5005, debug=True)
