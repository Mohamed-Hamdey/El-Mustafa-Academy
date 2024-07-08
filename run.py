from app import create_app, db
from app.models import User, Course, Enrollment, Assignment, Exam, Video, EnvironmentTopic, Schedule, Notification, ParentStudent, StudentProgress

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Course': Course, 
        'Enrollment': Enrollment,
        'Assignment': Assignment,
        'Exam': Exam,
        'Video': Video,
        'EnvironmentTopic': EnvironmentTopic,
        'Schedule': Schedule,
        'Notification': Notification,
        'ParentStudent': ParentStudent,
        'StudentProgress': StudentProgress
    }

if __name__ == '__main__':
    app.run(debug=True)