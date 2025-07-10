from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import sqlite3
from datetime import datetime
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ACT_servey')

# Database setup
def init_db():
    conn = sqlite3.connect('survey_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  age INTEGER,
                  gender TEXT,
                  phone TEXT,
                  q1_score INTEGER,
                  q2_score INTEGER,
                  q3_score INTEGER,
                  q4_score INTEGER,
                  q5_score INTEGER,
                  total_score INTEGER,
                  submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Sample questions configuration
QUESTIONS = {
    'q1': {
        'text': '在过去4周内，在工作、学习或家中，有多少时间小船妨碍您进行日常活动？',
        'options': {
            'A': {'text': '所有时间', 'score': 1},
            'B': {'text': '大多数时间', 'score': 2},
            'C': {'text': '有些时间', 'score': 3},
            'D': {'text': '很少时间', 'score': 4},
            'E': {'text': '没有', 'score': 5}
        }
    },
    'q2': {
        'text': '在过去4周内，您有多少次呼吸困难？',
        'options': {
            'A': {'text': '每天不止1次', 'score': 1},
            'B': {'text': '每天1次', 'score': 2},
            'C': {'text': '每周3-6次', 'score': 3},
            'D': {'text': '每周1-2次', 'score': 4},
            'E': {'text': '完全没有', 'score': 5}
        }
    },
    'q3': {
        'text': '在过去4周内，因为哮喘症状（喘息、咳嗽、呼吸困难、胸闷或疼痛），您有多少次在夜间醒来或早上比平时早醒？',
        'options': {
            'A': {'text': '每周4晚或更多', 'score': 1},
            'B': {'text': '每周2-3晚', 'score': 2},
            'C': {'text': '每周1次', 'score': 3},
            'D': {'text': '1-2次', 'score': 4},
            'E': {'text': '没有', 'score': 5}
        }
    },
    'q4': {
        'text': '在过去4周内，您有多少次用急救药物治疗（加沙丁胺醇）？',
        'options': {
            'A': {'text': '每天3次以上', 'score': 1},
            'B': {'text': '每天1-2次', 'score': 2},
            'C': {'text': '每周2-3次', 'score': 3},
            'D': {'text': '每周1次或更少', 'score': 4},
            'E': {'text': '没有', 'score': 5}
        }
    },
    'q5': {
        'text': '您如何评估过去4周内，您的哮喘控制情况？',
        'options': {
            'A': {'text': '没有控制', 'score': 1},
            'B': {'text': '控制很差', 'score': 2},
            'C': {'text': '有所控制', 'score': 3},
            'D': {'text': '控制很好', 'score': 4},
            'E': {'text': '完全控制', 'score': 5}
        }
    }
}

@app.route('/')
def index():
    return render_template('survey.html', questions=QUESTIONS)

@app.route('/submit', methods=['POST'])
def submit_survey():
    try:
        # Get form data
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        
        # Validate required fields
        if not name:
            flash('Name is required!')
            return redirect(url_for('index'))
        
        # Calculate scores
        scores = {}
        total_score = 0
        
        for q_id in QUESTIONS.keys():
            answer = request.form.get(q_id)
            if answer:
                score = QUESTIONS[q_id]['options'][answer]['score']
                scores[f'{q_id}_score'] = score
                total_score += score
            else:
                flash(f'Please answer all questions!')
                return redirect(url_for('index'))
        
        # Save to database
        conn = sqlite3.connect('survey_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO responses 
                     (name, age, gender, phone, q1_score, q2_score, q3_score, q4_score, q5_score, total_score)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (name, age, gender, phone, scores['q1_score'], scores['q2_score'], 
                   scores['q3_score'], scores['q4_score'], scores['q5_score'], total_score))
        conn.commit()
        conn.close()
        
        return render_template('results.html', 
                             name=name, 
                             total_score=total_score, 
                             max_score=25)
    
    except Exception as e:
        flash(f'Error processing form: {str(e)}')
        return redirect(url_for('index'))
    

from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == 'admin' and auth.password == 'huxizhimeng'):
            return ('Authentication required', 401, {
                'WWW-Authenticate': 'Basic realm="Admin Access"'})
        return f(*args, **kwargs)
    return decorated

@app.route('/admin')
@require_auth
def admin_dashboard():
    """Simple admin dashboard to view collected data"""
    conn = sqlite3.connect('survey_data.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM responses ORDER BY submission_date DESC''')
    responses = c.fetchall()
    conn.close()
    
    return render_template('admin.html', responses=responses)

@app.route('/api/stats')
def get_stats():
    """API endpoint to get basic statistics"""
    conn = sqlite3.connect('survey_data.db')
    c = conn.cursor()
    
    # Get total responses
    c.execute('SELECT COUNT(*) FROM responses')
    total_responses = c.fetchone()[0]
    
    # Get average score
    c.execute('SELECT AVG(total_score) FROM responses')
    avg_score = c.fetchone()[0] or 0
    

    conn.close()
    
    return jsonify({
        'total_responses': total_responses,
        'average_score': round(avg_score, 2)
        })
   
@app.route('/download-db')
def download_db():
    """Export survey data to Excel file"""
    try:
        # Connect to database
        conn = sqlite3.connect('survey_data.db')
        
        # Read data into pandas DataFrame
        df = pd.read_sql_query('''
            SELECT 
                id,
                name,
                age,
                gender,
                phone,
                q1_score,
                q2_score,
                q3_score,
                q4_score,
                q5_score,
                total_score,
                submission_date
            FROM responses 
            ORDER BY submission_date DESC
        ''', conn)
        
        conn.close()
        
        # Add score interpretation column
        def interpret_score(score):
            if score >= 20:
                return "Good control"
            elif score >= 15:
                return "Moderate control"
            else:
                return "Poor control"
        
        df['score_interpretation'] = df['total_score'].apply(interpret_score)
        
        # Create Excel file
        excel_filename = 'survey_responses_export.xlsx'
        df.to_excel(excel_filename, index=False, sheet_name='Survey Responses')
        
        return send_file(excel_filename, 
                        as_attachment=True, 
                        download_name=f'ACT_Survey_Data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
    
    except Exception as e:
        flash(f'Error exporting data: {str(e)}')
        return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)