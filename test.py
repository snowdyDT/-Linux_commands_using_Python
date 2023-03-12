from PyPDF2 import PdfReader


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''

    for page in reader.pages:
        text += page.extract_text() + "\n"

    text_from_pdf = text
    print("Прочитал документ")
    return text_from_pdf


print(read_pdf('files/Резюме СПМ.pdf'))
