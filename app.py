from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, User, Team, Match

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournament.db'
db.init_app(app)

def seed_database():
    with app.app_context():
        if not Team.query.first():
            team1 = Team(name="Team Alpha", sport="ASL", captain="Virat")
            team2 = Team(name="Team Beta", sport="ASL", captain="Sanjay")
            team3 = Team(name="Team Delta", sport="APL", captain="Nazna")
            team4 = Team(name="Team Gamma", sport="APL", captain="Riya")
            db.session.add_all([team1, team2, team3, team4])
            db.session.commit()

            match1 = Match(team1_id=team1.id, team2_id=team2.id, date="March 15, 2025", time="3:00 PM", location="Central Stadium", sport="ASL", status="Scheduled")
            match2 = Match(team1_id=team3.id, team2_id=team4.id, date="March 16, 2025", time="2:30 PM", location="Cricket Ground", sport="APL", status="Scheduled")
            db.session.add_all([match1, match2])
            db.session.commit()

with app.app_context():
    db.drop_all()  
    db.create_all()  
    seed_database()  

@app.route('/')
def index():
    upcoming_matches = Match.query.filter_by(status='Scheduled').all()
    return render_template('index.html', matches=upcoming_matches)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/register_team', methods=['GET', 'POST'])
def register_team():
    if request.method == 'POST':
        name = request.form['name']
        sport = request.form['sport']
        captain = request.form['captain']
        team = Team(name=name, sport=sport, captain=captain)
        db.session.add(team)
        db.session.commit()
        flash('Team registered successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('team_registration.html')

@app.route('/schedule')
def schedule():
    matches = Match.query.all()
    return render_template('schedule.html', matches=matches)

@app.route('/update_score/<int:match_id>', methods=['GET', 'POST'])
def update_score(match_id):
    match = Match.query.get_or_404(match_id)
    if request.method == 'POST':
        match.score_team1 = int(request.form['score_team1'])
        match.score_team2 = int(request.form['score_team2'])
        match.status = 'Completed'
        db.session.commit()
        flash('Score updated successfully!', 'success')
        return redirect(url_for('schedule'))
    return render_template('update_score.html', match=match)


if __name__ == '__main__':
    app.run(debug=True)