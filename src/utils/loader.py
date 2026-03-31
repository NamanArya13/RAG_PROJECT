from .parser import parse_pdf, parse_docx, parse_web

class DocumentLoader:

    @staticmethod
    def load(source: str, file_type: str):
        if file_type == "pdf":
            return parse_pdf(source)
        elif file_type == "docx":
            return parse_docx(source)
        elif file_type == "url":
            return parse_web(source)
        else:
            raise ValueError("Unsupported file type")