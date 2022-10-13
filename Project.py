import os
import sys
from time import sleep
from subprocess import run, PIPE, STDOUT
from IPython.display import clear_output
from yachalk import chalk


docs_path = "/home/sabyr/Desktop/Docs"
correct_path = "/home/sabyr/Desktop/Correct"
incorrect_path = "/home/sabyr/Desktop/Incorrect"


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
		
		
clear_output()
clear()

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
    
    variant, fio, iin, summ = options()
    
    if variant in "login success":
        print("NEXT IS FIND DOCS")
    
    elif variant in "login invalid":
        print("INVALID LOGIN")
    
    elif variant in "signup":
        print("NEXT IS FIND DOCS FOR NEW USER")
    
    check, docs = check_docs(docs_path)

    if check == True:
        
        while(len(docs) > 0):
            doc, docs = get_one_doc(docs)
            
            print("============================")
            print("SLEEP 5 SECONDS")
            sleep(5)
            clear_output()
            clear()
            
            text = read_text(f'{docs_path}/{doc}')
            
            try:
                if "FIO" in text[0]:
                    if fio in text[0] and iin in text[1] and summ in text[2]:
                        print("DATA IS CORRECT \n\n\n")
                        os.system(f"mv {docs_path}/{doc} {correct_path}")
                        
                        print("SLEEP 5 SECONDS")
                        sleep(5)
                        clear_output()
                        clear()
                        
                    else:
                        print(chalk.bold.red("DATA IS INCORRECT \n\n\n"))
                        os.system(f"mv {docs_path}/{doc} {incorrect_path}")
                        
                        print("SLEEP 5 SECONDS")
                        sleep(5)
                        clear_output()
                        clear()
                        
                else:
                    print(chalk.bold.red("False \n\n\n"))
                    os.system(f"mv {docs_path}/{doc} {incorrect_path}")
                    
                    print("SLEEP 5 SECONDS")
                    sleep(5)
                    clear_output()
                    clear()
                          
            except Exception as err:
                print(chalk.bold.red(f"INCORRECT FORMAT DOC FOR CLIENT: {err} \n\n\n"))
                print("SLEEP 5 SECONDS")
                sleep(5)
                clear_output()
                clear()

main()
