from app import create_app, db
from app.models import User, Course, Assignment, Exam, Video

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Course': Course, 
        'Assignment': Assignment,
        'Exam': Exam,
        'Video': Video,
    }

if __name__ == '__main__':
    app.run(debug=True)