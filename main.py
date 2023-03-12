import os
import re
import sys
from IPython.display import clear_output
from yachalk import chalk
import flask
from PyPDF2 import PdfReader
import keyring

docs_path = "/home/sabyr/Desktop/Docs"
correct_path = "/home/sabyr/Desktop/Correct"
incorrect_path = "/home/sabyr/Desktop/Incorrect"
pdf_path = "files/Резюме СПМ.pdf"

app = flask.Flask(__name__)


def get_command(command):
    clear_command = {
        "linux": "clear"
    }
    pip_command = {
        "linux": "pip3"
    }
    python_command = {
        "linux": "python3"
    }
    if command == "clear":
        return clear_command[sys.platform]

    elif command == "pip":
        return pip_command[sys.platform]

    elif command == "python":
        return python_command[sys.platform]


def clear():
    os.system(get_command("clear"))

    print("""succesfully cleared \n\n""")


def install_python_library(library_name):
    print(f"TRY INSTALL LIBRARY: {library_name}")
    os.system(f"pip3 install {library_name}")


def check_docs(path):
    docs = os.listdir(path)
    print(f"documents in the folder 'Docs': {docs}")
    if docs == []:
        print("there is no any docs")
        return False, docs
    else:
        print(f"Found {len(docs)} many docs and returned")
        return True, docs


def get_one_doc(docs):
    doc = docs[0]
    print(f"GET DOC: {doc}")
    docs.remove(docs[0])
    print("REMOVED")
    print(f"DOCS AFTER REMOVED: {docs}")

    return doc, docs


def read_text(path):
    with open(path) as f:
        text = f.read()
        print(text)
        f.close()

    with open(path) as f:
        text_list = f.readlines()
        f.close()

        return text_list


def login(fio, iin, summ):
    if fio is None or iin is None or summ is None:
        print("PLEASE SIGN UP FULLY")
    else:
        fio_ = input("FIO:")
        iin_ = input("IIN:")
        summ_ = input("SUM OF TRANSFER:")

        if fio == fio_ and iin == iin_ and summ == summ_:
            print("SUCCESFULLY LOGED")
            return "login success", fio, iin, summ
        else:
            print(chalk.bold.red("ERROR LOGED"))
            return "login invalid", fio, iin, summ


def signup():
    fio = input("FIO:")
    iin = input("IIN:")
    summ = input("SUM OF TRANSFER:")
    print("SUCCESFULLY SIGN UP")

    return "signup", fio, iin, summ


def options(i=None):
    if i != None:
        option = input("> ")
    else:
        option = input("""
________________________
|  SIGN IN OR SIGN UP  |
|                      |
|     [1]: SIGN IN     |
|     [2]: SIGN UP     |
|______________________|
\n\n> """)
    if option == "1":
        return login()

    elif option == "2":
        return signup()

    else:
        print(chalk.bold.red("Invalid Option."))
        return options("i")


list_library = [
    'os',
    'sys',
    'time',
    'subprocess',
    'IPython',
    'yachalk'
]

fio = None
iin = None
summ = None


def main():
    for i in list_library:
        install_python_library(i)

    clear_output()
    clear()


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''

    for page in reader.pages:
        text += page.extract_text() + "\n"

    text_from_pdf = text
    print("Прочитал документ")
    return text_from_pdf


def filter_text(text):
    return text.replace('\n', '').replace(' ', '').replace(u'\xa0', u'').replace('Ə', 'Ә').replace('ə', 'ә').lower()


def find_between(start, end, text):
    return text.partition(start)[2].partition(end)[0]


@app.route('/data_service', methods=['POST'])
def data_service():
    request_data = flask.request.get_json()
    iin = None
    summ = None
    dbz = None
    error = ""

    if request_data:
        print("Получил данные с POST запроса")
        print(request_data)

        if 'iin' in request_data:
            iin = request_data['iin']
        if 'summ' in request_data:
            summ = request_data['summ']
        if 'dbz' in request_data:
            dbz = request_data['dbz']

        text_from_pdf = read_pdf(pdf_path)
        print(f"Текст:{text_from_pdf}")

        print("===============================")

        filtered_text = filter_text(text_from_pdf)
        print(f"Текст после фильтра: {filtered_text}")

        print("Проверка документа Резюме по параметрам ИИН, Сумма, Ставка, Срок, Номер договора")

        print("Проверка номер договора:")

        dbz = dbz.lower().strip()
        doc_dbz = find_between('№', '/r', filtered_text)
        print(f"Номер договора с запроса: {dbz}")
        print(f"Номер договора с документа: {doc_dbz}")
        if dbz != doc_dbz:
            print("не соответствует номер договора")
            error = error + " не соответствует номер договора "
        else:
            print("соответствует номер договора")
            error = error + " соответствует номер договора "

        iin = iin.lower().strip()
        doc_iin = find_between('иин:', 'дата', filtered_text)
        doc_iin = ''.join(re.findall(r'\d', doc_iin))
        print(f"ИИН с запроса: {iin}")
        print(f"ИИН с документа: {doc_iin}")
        if iin != doc_iin:
            print("не соответствует иин")
            error = error + ", не соответствует иин "
        else:
            print("соответствует иин")
            error = error + ", соответствует иин "

        summ = summ.lower().replace('.00', '').strip()
        doc_summ = find_between('предлагаемаясуммазайма', 'предлагаемыйсрок', filtered_text)
        doc_summ = ''.join(re.findall(r'\d', doc_summ))
        print(f"Сумма с запроса: {summ}")
        print(f"Сумма с документа: {doc_summ}")
        if summ != doc_summ:
            print("не соответствует сумма")
            error = error + ", не соответствует сумма "
        else:
            print("соответствует сумма")
            error = error + ", соответствует сумма "
        keyring.set_password("RPA", "RESULT", error)
        return f"Статус проверки: {error}"


if __name__ == '__main__':
    app.run(debug=True, port=8080)
