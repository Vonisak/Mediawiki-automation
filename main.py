import csv
import mwclient

site = mwclient.Site('localhost:81', path='/wiki/', scheme='http', force_login=False)


def addPage(pageName):
    page = site.Pages[pageName]
    page_text = '<strong>Таблица действующих сотрудников</strong>\n{| id = addtable class="wikitable"\n|-\n!| Отдел\n!|' \
                'Подразделение\n!| ФИО\n!| Должность\n!| Доп. Информация\n|-\n|}\n\n<strong>Таблица уволенных сотрудников' \
                '</strong>\n\n{| id = firetable class="wikitable"\n|-\n!| Отдел\n!| Подразделение\n!| ФИО\n!| Должность' \
                '\n!| Доп. Информация\n|-\n|}'
    page.save(page_text)

    # Добавление ссылки новой страницы на главную страницу
    page = site.Pages['Заглавная_страница']
    page_text = page.text()
    new_link = '\n* [http://localhost:81/wiki/index.php/' + pageName.replace(' ', '_') + ' ' + pageName + '];'

    page.save(page_text + new_link)


def checkEmployer(row):
    page = site.Pages[row[0]+'_'+row[1]]

    page_text = page.text()
    start = page_text.find('|-', page_text.find('|-', page_text.find('id = addtable')) + 1)
    end = page_text.find('|-', start + 1)
    end_table = page_text.find('|}', page_text.find('id = addtable'))

    while end < end_table:
        argument = ''
        argument_end = 0
        start = page_text.find('|', start + 1, end)

        while page_text[argument_end - 1] != '-':
            argument_end = page_text.find('\n', start, end)
            argument += page_text[start + 1:argument_end] + '\t'
            start = page_text.find('|', start + 1, end)
            if start == -1:
                break

        argument = argument.split('\t')
        for i in argument:
            if i == '':
                argument.remove(i)

        if (argument[0] == row[0]) & (argument[1] == row[1]) & (argument[2] == row[2]):
            return True

        start = end
        end = page_text.find('|-', start + 1)
    return False


def addEmployer(row, table_type):
    if not site.Pages[row[0]+'_'+row[1]].exists:
        addPage(row[0]+'_'+row[1])
    page = site.Pages[row[0]+'_'+row[1]]
    page_text = page.text()
    if len(row) < 5:
        insert_data = '|' + row[0] + '\n|' + row[1] + '\n|' + row[2] + '\n|' + row[3] + '\n' + '|-\n'
    else:
        insert_data = '|' + row[0] + '\n|' + row[1] + '\n|' + row[2] + '\n|' + row[3] + '\n|' + row[4] + '\n|-\n'

    start = page_text.find('id = ' + table_type + 'table')
    end = page_text.find('|}', start)

    page_begin = page_text[:end]
    page_end = page_text[end:]

    page.save(page_begin + insert_data + page_end)


def deleteEmployer(row, departament):
    if len(row) == 5:
        row_text = '|'+row[0]+'\n|'+row[1]+'\n|'+row[2]+'\n|'+row[3]+'\n|'+row[4]+'\n'
    else:
        row_text = '|' + row[0] + '\n|' + row[1] + '\n|' + row[2] + '\n|' + row[3] + '\n'
    page = site.Pages[departament]
    page_text = page.text()
    start = page_text.find('|-', page_text.find('|-', page_text.find('id = addtable')) + 1)
    end = page_text.find('|-', start)
    end_table = page_text.find('|}', page_text.find('id = addtable'))

    while end < end_table:
        if page_text.find(row_text, start, end) != -1:
            break

        start = end
        end = page_text.find('|-', start + 1)

    page_begin = page_text[:start]
    page_end = page_text[end:]

    page.save(page_begin + page_end)


def editEmployer(row):
    if len(row) == 5:
        row_text = '|'+row[0]+'\n|'+row[1]+'\n|'+row[2]+'\n'
    else:
        row_text = '|' + row[0] + '\n|' + row[1] + '\n|' + row[2] + '\n'
    page = site.Pages[row[0]+'_'+row[1]]
    page_text = page.text()
    start = page_text.find('|-', page_text.find('|-', page_text.find('id = addtable')) + 1)
    end = page_text.find('|-', start + 1)
    end_table = page_text.find('|}', page_text.find('id = addtable'))

    while end < end_table:
        if page_text.find(row_text, start, end) != -1:
            break
        start = end
        end = page_text.find('|-', start + 1)

    i = 0
    while i <= 3:
        start = page_text.find('|', start + 1, end)
        i += 1

    if len(row) == 5:
        # Если доп. информация заполнена
        insert_data = '|' + row[3] + '\n|' + row[4] + '\n'
        page_begin = page_text[:start]
        page_end = page_text[end:]
        page.save(page_begin+insert_data+page_end)
    else:
        # Если доп. информация не заполнена
        insert_data = '|' + row[3] + '\n'
        page_begin = page_text[:start]
        page_end = page_text[end:]
        page.save(page_begin+insert_data+page_end)


def checkTable(departament):
    page = site.Pages[departament]
    page_text = page.text()
    start = page_text.find('|-', page_text.find('|-', page_text.find('id = addtable')) + 1)
    end = page_text.find('|-', start+1)
    end_table = page_text.find('|}', page_text.find('id = addtable'))

    while end < end_table:
        flag = False
        argument = ''
        argument_end = 0
        start = page_text.find('|', start+1, end)

        while page_text[argument_end-1] != '-':
            argument_end = page_text.find('\n', start, end)
            argument += page_text[start + 1:argument_end] + '\t'
            start = page_text.find('|', start+1, end)
            if start == -1:
                break

        argument = argument.split('\t')
        for i in argument:
            if i == '':
                argument.remove(i)

        employees_file = open("employees.tsv", encoding='utf-8')
        read_tsv = csv.reader(employees_file, delimiter="\t")
        for row in read_tsv:
            if (row[2] == argument[2]) & (row[0] == argument[0]) & (row[1] == argument[1]):
                flag = True
                break

        if not flag:
            deleteEmployer(argument, departament)
            addEmployer(argument, 'fire')

        start = end
        end = page_text.find('|-', start + 1)

    return False


employees_file = open("employees.tsv", encoding='utf-8')
read_tsv = csv.reader(employees_file, delimiter="\t")

for row in read_tsv:
    if not checkEmployer(row):
        addEmployer(row, 'add')

    if checkEmployer(row):
        editEmployer(row)

for page in site.Pages:
    checkTable(page.name)

employees_file.close()
