from docx import Document
from pyresparser import ResumeParser
from flask import Flask
from flask_restful import Resource, Api, reqparse
import urllib.request

import nltk
nltk.download('stopwords')


app = Flask(__name__)
api = Api(app)

resume_data_post_args = reqparse.RequestParser()
resume_data_post_args.add_argument(
    'link', type=str, help='file link', required=True)


def download_file(download_url, filename, extension):
    response = urllib.request.urlopen(download_url)
    if extension == 'docx':
        file = open(filename + ".docx", 'wb')
        file.write(response.read())
        file.close()
    if extension == 'pdf':
        file = open(filename + ".pdf", 'wb')
        file.write(response.read())
        file.close()


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


class Resume(Resource):
    def get(self, id, ext):
        name = f"./uploads/{ext}_file_{id}.{ext}"
        return myResumeParser(name)

    def post(self, id, ext):
        args = resume_data_post_args.parse_args()
        save_at = f"./uploads/{ext}_file_{id}"
        download_file(args['link'], save_at, ext)
        return(f"File Downloaded at {save_at}")

api.add_resource(Resume, '/resume-data/<int:id>/<string:ext>')


if __name__ == '__main__':
    app.run(debug=True)
