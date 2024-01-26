'''
Aluno: Scheilla Giasson Artifon
Disciplina: Raciocínio Computacional
'''

import json

# Funções Json
def read_list_json(archive_name):
    try:
        with open(archive_name, "r", encoding="utf-8") as archive:
            list = json.load(archive)
        return list
    except:
        print("Não foi possível encontrar nenhum item na lista!\n")
        return []

def save_list_json(list, archive_name):
    with open(archive_name, "w", encoding="utf-8") as archive:
        json.dump(list, archive, ensure_ascii=False)

# Funções Submenu
def operation_submenu(option_menu, group_name, archive_name):
    print(f"\nVocê selecionou a opção {option_menu} ({group_name})\n\n")

    while True:
        submenu(group_name)

        option_submenu = check_integer_value("Informe o número da opção desejada: ")
        if option_submenu == "ValueError":
            continue
        elif option_submenu == "Error":
            break

        if option_submenu == 1:
            add_data(archive_name, group_name)
        elif option_submenu == 2:
            list_data(archive_name, group_name)
        elif option_submenu == 3:
            update_data(archive_name, group_name)
        elif option_submenu == 4:
            delete_data(archive_name, group_name)
        elif option_submenu == 9:  # Volta ao menu anterior
            break
        else:
            print("Opção Inválida")

def submenu(group_name):
    print(f"- - - - - Menu de {group_name} - - - - -\n")
    print("Selecione a opção abaixo: ")
    print("(1) Incluir")
    print("(2) Listar")
    print("(3) Atualizar")
    print("(4) Excluir")
    print("(9) Voltar ao menu principal")

# Funções do CRUD
def add_data(archive_name, group_name):
    print(f"\n= = = = = Incluir {group_name} = = = = =\n")

    list = read_list_json(archive_name)

    while True:
        cod = check_integer_value("Digite o código que deseja incluir: ")
        if cod == "ValueError" or cod == "Error":
            return None

        for item in list:
            if item["cod"] == cod:
                print("\nCódigo já está sendo utilizado!\n")
                return None

        if group_name == "Estudantes" or group_name == "Professores":
            newList = users_form(cod)
        elif group_name == "Disciplinas":
            newList = courses_form(cod)
        elif group_name == "Turmas":
            newList = classes_form(cod)
        elif group_name == "Matrículas":
            newList = registrations_form(cod)

        if newList is not None:
            list.append(newList)
            save_list_json(list, archive_name)
            print(f"Cadastrado com sucesso!\n")

        if input("Continuar cadastrando? (s/n) ") == "n":
            break

def list_data(archive_name, group_name):
    print(f"\n= = = = = Listar {group_name} = = = = =\n")

    list = read_list_json(archive_name)

    if not list:
        return

    print(f"Lista de {group_name} cadastrados:\n")

    for item in list:
        if group_name == "Estudantes" or group_name == "Professores":
            print(f"{item['name']} - Código: {item['cod']} - CPF: {item['cpf']}")
        elif group_name == "Disciplinas":
            print(f"{item['name']} - Código: {item['cod']}")
        elif group_name == "Turmas":
            print(f"Código da Turma: {item['cod']} - Código do Professor: {item['cod_professors']} - Código da Disciplina: {item['cod_disciplina']}")
        elif group_name == "Matrículas":
            print(f"Código da Matrícula: {item['cod']} - Código da Turma: {item['cod_classes']} - Código do Estudante: {item['cod_student']} - ")

    print("\n")
    return

def update_data(archive_name, group_name):
    print(f"\n= = = = = Atualizar {group_name} = = = = =\n")

    cod = check_integer_value("Digite o código que deseja atualizar: ")
    if cod == "ValueError" or cod == "Error":
        return None

    list = read_list_json(archive_name)
    for item in list:
        if item["cod"] == cod:
            if group_name == "Estudantes" or group_name == "Professores":
                updateList = users_form(cod, "update", item)
            elif group_name == "Disciplinas":
                updateList = courses_form(cod, "update", item)
            elif group_name == "Turmas":
                updateList = classes_form(cod, "update", item)
            elif group_name == "Matrículas":
                updateList = registrations_form(cod, "update", item)

            if updateList is not None:
                save_list_json(list, archive_name)
                print("\nAtualizado com sucesso!\n")
                return

    print("Não foi possível encontrar a opção digitada!\n")

def delete_data(archive_name, group_name):
    print(f"\n= = = = = Excluir {group_name} = = = = =\n")

    cod = check_integer_value("Digite o código que deseja excluir: ")
    if cod == "ValueError" or cod == "Error":
        return None

    list = read_list_json(archive_name)
    for item in list:
        # Verifica se o código digitado é igual o código já cadastrado
        if item["cod"] == cod:
            if group_name == "Estudantes" or group_name == "Professores" or group_name == "Disciplinas":
                print(f"\n{item['name']} está cadastrado com esse código.")

            # Pergunta se o usuario quer mesmo excluir
            deletion_confirmation = input(f"Tem certeza que deseja exluir? (s/n): ")
            if (deletion_confirmation == 's'):
                list.remove(item)
                save_list_json(list, archive_name)
                print("\nExcluído com sucesso!\n")
                return

    print("Não foi possível encontrar a opção digitada!\n")

# Funções formularios (criar e modificar)
def users_form(cod, action = "create", list = {}):
    if action == "create":
        name = input(f"Digite o nome: ")
        cpf = input(f"Digite o CPF: ")

        newUser = {"cod": cod, "name": name, "cpf": cpf}
        return newUser
    else:
        print("\nCódigo atual é: ", list["cod"])
        list["cod"] = check_integer_value("Digite o novo código: ")
        if list["cod"] == "ValueError" or list["cod"] == "Error":
            return None

        print("\nNome atual é: ", list["name"])
        list["name"] = input(f"Digite o novo nome: ")

        print("\nCPF atual é: ", list["cpf"])
        list["cpf"] = input(f"Digite o novo CPF: ")
        return True

def courses_form(cod, action = "create", list = {}):
    if action == "create":
        name = input(f"Digite o nome da disciplina: ")
        newCourse = {"cod": cod, "name": name}

        return newCourse
    else:
        print("\nCódigo atual da disciplina é: ", list["cod"])
        list["cod"] = check_integer_value("Digite o novo código da disciplina: ")
        if list["cod"] == "ValueError" or list["cod"] == "Error":
            return None

        print("\nDisciplina atual é: ", list["name"])
        list["name"] = input("Digite a nova disciplina: ")
        return True

def classes_form(cod, action = "create", list = {}):
    if action == "create":
        cod_professors = check_integer_value("Digite o código do professor: ")
        if cod_professors == "ValueError" or cod_professors == "Error":
            return None

        cod_disciplina = check_integer_value("Digite o código da disciplina: ")
        if cod_disciplina == "ValueError" or cod_disciplina == "Error":
            return None

        newClass = {"cod": cod, "cod_professors": cod_professors, "cod_disciplina": cod_disciplina}

        return newClass
    else:
        print("\nCódigo atual da turma é: ", list["cod"])
        list["cod"] = check_integer_value("Digite o novo código da turma: ")
        if list["cod"] == "ValueError" or list["cod"] == "Error":
            return None

        print("\nCódigo atual do professor é: ", list["cod_professors"])
        list["cod_professors"] = check_integer_value("Digite o novo código do professor: ")
        if list["cod_professors"] == "ValueError" or list["cod_professors"] == "Error":
            return None

        print("\nCódigo atual da disciplina é: ", list["cod_disciplina"])
        list["cod_disciplina"] = check_integer_value("Digite o novo código da disciplina: ")
        if list["cod_disciplina"] == "ValueError" or list["cod_disciplina"] == "Error":
            return None

        return True

def registrations_form(cod, action = "create", list = {}):
    if action == "create":
        cod_classes = check_integer_value("Digite o código da turma: ")
        if cod_classes == "ValueError" or cod_classes == "Error":
            return None

        cod_student = check_integer_value("Digite o código do estudante: ")
        if cod_student == "ValueError" or cod_student == "Error":
            return None

        newRegistration = {"cod": cod, "cod_classes": cod_classes, "cod_student": cod_student}
        return newRegistration
    else:
        print("\nCódigo atual do Registro é: ", list["cod"])
        list["cod"] = check_integer_value("Digite o novo código da turma: ")
        if list["cod"] == "ValueError" or list["cod"] == "Error":
            return None

        print("\nCódigo atual da turma é: ", list["cod_classes"])
        list["cod_classes"] = check_integer_value("Digite o novo código da turma: ")
        if list["cod_classes"] == "ValueError" or list["cod_classes"] == "Error":
            return None

        print("\nCódigo atual do estudante é: ", list["cod_student"])
        list["cod_student"] = check_integer_value("Digite o novo código do estudante: ")
        if list["cod_student"] == "ValueError" or list["cod_student"] == "Error":
            return None

        return True

# Verifica se valor é inteiro (Tratamento de erro)
def check_integer_value(message):
    try:
        value = int(input(message))
        return value
    except ValueError:
        print("Valor inválido\n")
        return "ValueError"
    except:
        print("\nOcorreu um erro inesperado!\n")
        return "Error"

print("\n- - - - - Menu Principal - - - - -")

# Menu principal
while True:
    print("\nSelecione uma das opções abaixo:")
    print("(1) Gerenciar estudantes")
    print("(2) Gerenciar professores")
    print("(3) Gerenciar disciplinas")
    print("(4) Gerenciar turmas")
    print("(5) Gerenciar matrículas")
    print("(9) Sair\n")

    option_menu = check_integer_value("Informe o número da opção desejada: ")
    if option_menu == "ValueError":
        continue
    elif option_menu == "Error":
        break

    # Bloco de estudantes
    if option_menu == 1:
        operation_submenu(option_menu, "Estudantes", "student.json")
    elif option_menu == 2:
        operation_submenu(option_menu, "Professores", "professor.json")
    elif option_menu == 3:
        operation_submenu(option_menu, "Disciplinas", "courses.json")
    elif option_menu == 4:
        operation_submenu(option_menu, "Turmas", "classes.json")
    elif option_menu == 5:
        operation_submenu(option_menu, "Matrículas", "registrations.json")
    elif option_menu == 9:
        break
    else:
        print("Opção Inválida")
        continue

print("\nAté a próxima!")