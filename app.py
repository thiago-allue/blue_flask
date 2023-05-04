from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search_history.db'
db = SQLAlchemy(app)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(255), nullable=False)

@app.route('/search_history', methods=['GET', 'POST', 'DELETE'])
def search_history():
    if request.method == 'GET':
        history = db.session.query(SearchHistory).all()
        return jsonify([{'id': h.id, 'query': h.query} for h in history])
    elif request.method == 'POST':
        query = request.json['query']
        history = SearchHistory(query=query)
        db.session.add(history)
        db.session.commit()
        return jsonify({'message': 'Search query added to history.'})
    elif request.method == 'DELETE':
        db.session.query(SearchHistory).delete()
        db.session.commit()
        return jsonify({'message': 'Search history cleared.'})

if __name__ == '__main__':
    db.create_all() # create the table if it does not exist
    app.run(debug=True)