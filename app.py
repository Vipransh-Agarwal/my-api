from docx import Document
import os
from pyresparser import ResumeParser
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

import nltk
nltk.download('stopwords')


app = Flask(__name__)
api = Api(app)

data = {}

resume_data_post_args = reqparse.RequestParser()
resume_data_post_args.add_argument(
    'info', type=str, help='resume path', required=True)


def myResumeParser(filed):
    try:
        doc = Document()
        with open(filed, 'r') as file:
            doc.add_paragraph(file.read())
        doc.save("text.docx")
        data = ResumeParser('text.docx').get_extracted_data()
        return data
    except:
        data = ResumeParser(filed).get_extracted_data()
        return data


class Resume_Data(Resource):
    def get(self):
        return data


class Resume(Resource):
    def get(self, data_id):
        return data[data_id]

    def post(self, data_id):
        args = resume_data_post_args.parse_args()
        if data_id in data:
            abort(409, message="ID already there")
        data[data_id] = {'info': myResumeParser(args['info'])}
        return data[data_id]


api.add_resource(Resume_Data, '/resume-data')
api.add_resource(Resume, '/resume-data/<int:data_id>')


if __name__ == '__main__':
    app.run(debug=True)
