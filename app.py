from flask import Flask, render_template, redirect, url_for, session, request, flash
import os
import re
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ADMIN_PASSWORD = "AxoBot005*"

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(500))
    description = db.Column(db.String(200))
    category = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

def is_authenticated():
    return session.get('authenticated', False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        if not is_authenticated():
            password = request.form.get('password')
            if password == ADMIN_PASSWORD:
                session['authenticated'] = True
            else:
                flash('Mot de passe incorrect', 'error')
                return redirect(url_for('settings'))

        # Si authentifié et modification de paramètre
        if setting_name := request.form.get('setting_name'):
            setting = Setting.query.filter_by(name=setting_name).first()
            if setting:
                setting.value = request.form.get('value')
                setting.updated_at = datetime.utcnow()
                db.session.commit()
                flash('Paramètre mis à jour avec succès', 'success')

    settings = Setting.query.order_by(Setting.category).all()
    return render_template('settings.html', 
                         settings=settings, 
                         is_authenticated=is_authenticated())

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('settings'))

@app.route('/leaderboard')
def leaderboard():
    # Simuler des données de classement
    users = [
        {"username": "User1", "axocoins": 1000},
        {"username": "User2", "axocoins": 800},
        {"username": "User3", "axocoins": 600},
    ]
    return render_template('leaderboard.html', users=users)

@app.route('/logs')
def logs():
    logs_data = []
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

    if os.path.exists(log_dir):
        latest_log = max([f for f in os.listdir(log_dir) if f.startswith('bot_')], 
                        key=lambda x: os.path.getctime(os.path.join(log_dir, x)))

        with open(os.path.join(log_dir, latest_log), 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}):(\w+):(.*)', line)
                if match:
                    logs_data.append({
                        'timestamp': match.group(1),
                        'level': match.group(2),
                        'message': match.group(3).strip()
                    })

    return render_template('logs.html', logs=logs_data)

def initialize_settings():
    default_settings = [
        {
            'name': 'welcome_message',
            'value': 'Bienvenue sur le serveur {user}!',
            'description': 'Message de bienvenue pour les nouveaux membres',
            'category': 'Messages'
        },
        {
            'name': 'prefix',
            'value': '!',
            'description': 'Préfixe pour les commandes du bot',
            'category': 'Commandes'
        },
        {
            'name': 'daily_coins',
            'value': '100',
            'description': 'Nombre d\'Axocoins donnés quotidiennement',
            'category': 'Économie'
        },
        {
            'name': 'language',
            'value': 'fr',
            'description': 'Langue du bot (fr/en)',
            'category': 'Général'
        },
        {
            'name': 'mod_role',
            'value': 'Moderator',
            'description': 'Nom du rôle modérateur',
            'category': 'Rôles'
        }
    ]

    for setting in default_settings:
        if not Setting.query.filter_by(name=setting['name']).first():
            new_setting = Setting(
                name=setting['name'],
                value=setting['value'],
                description=setting['description'],
                category=setting['category']
            )
            db.session.add(new_setting)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initialize_settings()
    app.run(host='0.0.0.0', port=5000)