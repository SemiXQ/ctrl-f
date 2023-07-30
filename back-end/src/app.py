from .entities.entity import Session, engine, Base
from .entities.exam import Exam, ExamSchema
from .docdict.docdict import init_dict, searchText
from flask import Flask, jsonify, request
from flask_cors import CORS

# creating the flask app
app = Flask(__name__)
CORS(app)

# generate database schema
Base.metadata.create_all(engine)

@app.before_request
def before_request_handler():
    init_dict()

# @app.route('/init', methods=['GET'])
# def get_dictionary():
#     init_dict()
#     return jsonify({}), 200

@app.route('/test')
def get_test():
    data = {"message": "hello world"}
    return jsonify(data)

@app.route('/initial_text/<string:filename>')
def init_text(filename):
    try:
        with open(f'./doc/{filename}.txt', 'r') as file:
            content = file.read()
            return jsonify({"content": content}), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/search_text/<string:filename>/<string:searchContent>')
def search_text(filename, searchContent):
    try:
        response = searchText(filename, searchContent)
        return jsonify(response), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/exams')
def get_exams():
    # fetching from the database
    session = Session()
    exam_objects = session.query(Exam).all()

    # transforming into JSON-serializable objects
    schema = ExamSchema(many=True)
    exams = schema.dump(exam_objects)

    # serializing as JSON
    session.close()
    return jsonify(exams.data)

@app.route('/exams', methods=['POST'])
def add_exam():
    # mount exam object
    posted_exam = ExamSchema(only=('title', 'description'))\
        .load(request.get_json())

    exam = Exam(**posted_exam.data, created_by="HTTP post request")

    # persist exam
    session = Session()
    session.add(exam)
    session.commit()

    # return created exam
    new_exam = ExamSchema().dump(exam).data
    session.close()
    return jsonify(new_exam), 201

# # start session
# session = Session()

# # check for existing data
# exams = session.query(Exam).all()

# if len(exams) == 0:
#     # create and persist mock exam
#     python_exam = Exam("mysql check", "Check if mysql works correctly.", "script")
#     session.add(python_exam)
#     session.commit()
#     session.close()

#     # reload exams
#     exams = session.query(Exam).all()

# # show existing exams
# print('### Exams:')
# for exam in exams:
#     print(f'({exam.id}) {exam.title} - {exam.description}')