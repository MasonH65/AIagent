#from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
print('-------------main.py-------------')
print(get_file_content("calculator", "main.py"))
print('--------pkg/calculator.py--------')
print(get_file_content("calculator", "pkg/calculator.py"))
print('------------/bin/cat-------------')
print(get_file_content("calculator", "/bin/cat"))


