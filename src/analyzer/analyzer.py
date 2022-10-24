# imports
import string
from tkinter import messagebox

from src.components.ColocationClass import ColocationClass
from src.components.PropertyClass import PropertyClass
from src.components.Tokens import Tokens
from src.components.controller_class import ControlersClass

letters = list(string.ascii_letters)


# Our brain
# static functions that don't use class attributes
def remove(string: str, token: str):
    new_string = ""
    count = 0
    # verified token and return a string without the token
    list_string = string.split(token)  # delete read token
    for j in list_string:
        if count == len(list_string) - 1:
            new_string += j
        elif count > 0:
            new_string += j + token
        count += 1
    return new_string


# In this function we verified the first part, the variables
def verified_alfabet(string: str):
    count = 0
    key = False
    # write all the characters
    alfabet = letters
    for i in string:
        key = False
        for j in alfabet:
            if i == j:
                key = True
                break
        if not key:
            return {'result': None, 'count': count}
        count += 1
    return {'result': True, 'count': count}


# verified numbers
def verified_numbers(string: str):
    count = 0
    key = False
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in string:
        key = False
        for j in numbers:
            if i == j:
                key = True
                break
        if not key:
            return {'result': None, 'count': count}
        count += 1
    return {'result': True, 'count': count}


class Analyzer:
    def __init__(self):
        self.state = False
        self.line = 0
        self.col = 0
        self.tmp_string = ""
        self.string_list = []
        self.initialState = 0
        # save controller options
        self.control = None
        self.controlers_list = []
        # managed properties
        self.property = None
        self.property_value = None
        self.values_prop = []
        self.properties_list = []
        # managed colocation
        self.colocation = None
        self.values_colocation = []
        self.colocations_list = []
        # save tokens
        self.token_list = []

    def show_error(self, token, type ):
        messagebox.showerror(message=f'{self.line} | {self.col} | {token} | {type}', title='ERROR!')
    def multiLinealComents(self, string: str):
        try:
            tmp = ""
            count = 0
            key = False
            if string[0] == "/" and string[1] == "*":
                for i in string:
                    if key:
                        tmp += i
                    if string[count-1] == "*" and string[count] == "/":
                        key = True
                    count += 1
                print(f'{self.line} | {self.col} | "Comentario multilinea" ')
                self.next_line()
                return tmp
            return string
        except:
            return string

    def next_line(self):
        tmp = self.string_list[self.line]
        if tmp == self.tmp_string:
            self.line += 1
            self.tmp_string = ''
            self.col = 0

    def verified_token(self, string: str, token: str):
        count = 0
        for i in range(0, len(token)):  # verified if there are any error
            if count >= len(string):
                return {'result': None, 'count': count}
            if string[i] != token[i]:
                return {'result': None, 'count': count}
            count += 1

        new_string = ""
        count_1 = 0
        # verified token and return a string without the token
        list_string = string.split(token)  # delete read token
        for j in list_string:
            if count_1 == len(list_string) - 1:
                new_string += j
            elif count_1 > 0:
                new_string += j + token
            count_1 += 1
        self.tmp_string += token

        return {'result': new_string, 'count': count}

    def analyze_state(self, token_value, string, next_state):
        token = token_value
        res = self.verified_token(string, token)
        # verified an error
        if res['result'] is None:
            return {'Error': res['result']}
        # print
        print(f'{self.line} | {self.col} | {token}')
        # change data
        string = res['result']
        self.col += res['count']
        self.initialState = next_state
        # increment line
        self.next_line()
        # add token
        token = Tokens(token, string)
        self.token_list.append(token)
        return string

    def read_states(self, string):
        self.initialState = 'S0'
        while string != "":  # while the string ins´t empty
            if self.initialState == "S0":  # If initial state is the state, define the token
                string = self.multiLinealComents(string)
                string = self.analyze_state('<', string, 'S1')

            elif self.initialState == "S1":
                string = self.multiLinealComents(string)
                string = self.analyze_state('!', string, 'S2')

            elif self.initialState == "S2":
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 'S3')

            elif self.initialState == "S3":
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 'S4')

            elif self.initialState == "S4":
                string = self.multiLinealComents(string)
                string = self.analyze_state('Controles', string, 'S5')

            elif self.initialState == "S5":
                string = self.multiLinealComents(string)
                token = 'Controles'
                res = self.verified_token(string, token)
                # verified an error
                if res['result'] is None:
                    tokens = ['Etiqueta', 'Boton', 'Check', 'RadioBoton', 'Texto', ' AreaTexto', 'Clave', 'Contenedor']
                    for i in tokens:
                        res = self.verified_token(string, i)
                        if res['result'] is not None:
                            token = i
                            self.control = token
                            self.initialState = 'S6'
                            break
                else:
                    self.initialState = 'S9'

                # verified an error
                if res['result'] is None:
                    self.show_error(token, 'ERROR LÉXICO')
                    break
                # print
                print(f'{self.line} | {self.col} | {token}')
                # change data
                string = res['result']
                self.col += res['count']
                # increment line
                self.next_line()
                # add token
                token_obj = Tokens(token, string)
                self.token_list.append(token_obj)

            elif self.initialState == 'S6':
                string = self.multiLinealComents(string)
                tmp = string.split(";")
                id = tmp[0]
                verified_alfabet(id)

                # Create a object of controlers
                controler = ControlersClass(self.control, id)
                self.controlers_list.append(controler)

                print(f'{self.line} | {self.col} | {id}')
                # add token
                token_obj = Tokens(id, string)
                self.token_list.append(token_obj)

                self.tmp_string += id
                string = remove(string, id)
                self.initialState = 'S7'


            elif self.initialState == 'S7':
                string = self.multiLinealComents(string)
                string = self.analyze_state(';', string, 'S8')

            elif self.initialState == 'S8':
                string = self.multiLinealComents(string)
                separate = string.split(';')
                if separate[0] != 'Controles':
                    self.initialState = 'S5'
                else:
                    string = self.analyze_state('Controles', string, 'S9')

            elif self.initialState == 'S9':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 'S10')

            elif self.initialState == 'S10':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 'S11')

            elif self.initialState == 'S11':
                string = self.multiLinealComents(string)
                string = self.analyze_state('>', string, 'q0')
                print('Fin del primer arbol')

            # now read the second part
            elif self.initialState == 'q0':
                string = self.multiLinealComents(string)
                string = self.analyze_state('<', string, 'q1')

            elif self.initialState == 'q1':
                string = self.multiLinealComents(string)
                string = self.analyze_state('!', string, 'q2')

            elif self.initialState == 'q2':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 'q3')

            elif self.initialState == 'q3':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 'q4')

            elif self.initialState == 'q4':
                string = self.multiLinealComents(string)
                string = self.analyze_state('propiedades', string, 'q5')

            elif self.initialState == 'q5':
                string = self.multiLinealComents(string)
                token = 'propiedades'
                res = self.verified_token(string, token)
                # verified an error
                if res['result'] is None:
                    for i in self.controlers_list:
                        value = i.id
                        res = self.verified_token(string, value)
                        if res['result'] is not None:
                            token = value
                            self.property = token
                            self.initialState = 'q6'
                            break
                else:
                    self.initialState = 'q15'

                # verified an error
                if res['result'] is None:
                    self.show_error(token, 'ERROR - SINTATICO- La variable no esta declarada')
                    break
                # print
                print(f'{self.line} | {self.col} | {token}')
                # change data
                string = res['result']
                self.col += res['count']
                # increment line
                self.next_line()
                # add token
                token_obj = Tokens(token, string)
                self.token_list.append(token_obj)

            elif self.initialState == 'q6':
                string = self.multiLinealComents(string)
                string = self.analyze_state('.', string, 'q7')

            elif self.initialState == 'q7':
                string = self.multiLinealComents(string)
                value = None
                values = None
                tmp = string.split('(')
                for i in self.controlers_list:
                    if i.id == self.property:
                        values = i.properties
                        break
                if tmp[0] in values:
                    value = tmp[0]
                    self.property_value = value
                    string = self.analyze_state(value, string, 'q8')
                else:
                    self.show_error(token, 'ERROR - SINTACTICO - LA PROPIERDAD NO CORRESPONDE')
                    break

            elif self.initialState == 'q8':
                string = self.multiLinealComents(string)
                string = self.analyze_state('(', string, 'q9')

            elif self.initialState == 'q9':
                string = self.multiLinealComents(string)
                tmp = string.split(')')
                value = tmp[0].split(',')
                verified_numbers(value[0])
                # Save the property with their value
                self.values_prop.append(value[0])

                print(f'{self.line} | {self.col} | {value[0]}')
                # add token
                token_obj = Tokens(value[0], string)
                self.token_list.append(token_obj)

                self.tmp_string += value[0]
                string = remove(string, value[0])
                self.initialState = 'q10'
                self.next_line()

            elif self.initialState == 'q10':
                string = self.multiLinealComents(string)
                tmp = string.split(')')
                if self.property_value == 'setTexto' or self.property_value == 'setAlineacion' or self.property_value == 'setMarcada' or \
                        self.property_value == 'setGrupo' or self.property_value == 'setAncho' or self.property_value == 'setAlto':
                    if tmp[0] == '':
                        string = self.analyze_state(')', string, 'q13')
                    else:
                        self.show_error(tmp[0], f'ERROR - Propiedad -> {self.property_value} solo acepta un valor')
                        break

                elif self.property_value == 'setColorLetra' or self.property_value == 'setColorFondo':
                    if tmp[0] != '':
                        string = self.analyze_state(',', string, 'q11')
                    else:
                        print(f'')
                        self.show_error(tmp[0], f'ERROR -Propiedad -> {self.property_value} necesita 3 valores')
                        break
                else:
                    self.show_error(tmp[0], f'ERROR -Tiene más valores')
                    break

            elif self.initialState == 'q11':
                string = self.multiLinealComents(string)
                tmp = string.split(')')
                value = tmp[0].split(',')
                verified_numbers(value[0])
                # Save the property with their value
                self.values_prop.append(value[0])
                print(f'{self.line} | {self.col} | {value[0]}')
                # add token
                token_obj = Tokens(value[0], string)
                self.token_list.append(token_obj)

                self.tmp_string += value[0]
                string = remove(string, value[0])
                self.initialState = 'q12'
                self.next_line()

            elif self.initialState == 'q12':
                string = self.multiLinealComents(string)
                token = ')'
                res = self.verified_token(string, token)
                # verified an error
                if res['result'] is None:
                    tmp = string.split(')')
                    value = tmp[0]
                    if value[0] == ',':
                        string = self.analyze_state(value[0], string, 'q11')
                else:
                    string = self.analyze_state(')', string, 'q13')

            elif self.initialState == 'q13':
                string = self.multiLinealComents(string)
                # create the object or find the property already created
                property_obj = PropertyClass(self.property, self.property_value, self.values_prop)
                self.properties_list.append(property_obj)
                print(self.property, self.property_value, self.values_prop)
                string = self.analyze_state(';', string, 'q14')

            elif self.initialState == 'q14':
                string = self.multiLinealComents(string)
                separate = string.split(';')
                if separate[0] != 'propiedades':
                    self.initialState = 'q5'
                    self.values_prop = []
                else:
                    string = self.analyze_state('propiedades', string, 'q15')

            elif self.initialState == 'q15':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 'q16')

            elif self.initialState == 'q16':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 'q17')

            elif self.initialState == 'q17':
                string = self.multiLinealComents(string)
                string = self.analyze_state('>', string, 't0')
                print('Fin del segundo arbol')

            # now read the last part
            elif self.initialState == 't0':
                string = self.multiLinealComents(string)
                string = self.analyze_state('<', string, 't1')

            elif self.initialState == 't1':
                string = self.multiLinealComents(string)
                string = self.analyze_state('!', string, 't2')

            elif self.initialState == 't2':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 't3')

            elif self.initialState == 't3':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 't4')

            elif self.initialState == 't4':
                string = self.multiLinealComents(string)
                string = self.analyze_state('Colocacion', string, 't5')

            elif self.initialState == 't5':
                string = self.multiLinealComents(string)
                token = 'Colocacion'
                res = self.verified_token(string, token)
                # verified an error
                if res['result'] is None:
                    for i in self.controlers_list:
                        value = i.id
                        res = self.verified_token(string, value)
                        if res['result'] is not None:
                            token = value
                            self.property = token
                            self.initialState = 't6'
                            break
                        else:
                            value = 'this'
                            res = self.verified_token(string, value)
                            if res['result'] is not None:
                                token = value
                                self.property = token
                                self.initialState = 't6'
                                break
                else:
                    self.initialState = 't16'

                # verified an error
                if res['result'] is None:
                    self.show_error(token, 'ERROR - SINTATICO- La variable no esta declarada')
                    break
                # print
                print(f'{self.line} | {self.col} | {token}')
                # change data
                string = res['result']
                self.col += res['count']
                # increment line
                self.next_line()
                # add token
                token_obj = Tokens(token, string)
                self.token_list.append(token_obj)

            elif self.initialState == 't6':
                string = self.multiLinealComents(string)
                string = self.analyze_state('.', string, 't7')

            elif self.initialState == 't7':
                string = self.multiLinealComents(string)
                token = 'add'
                res = self.verified_token(string, token)
                # verified an error
                if res['result'] is None:
                    value = 'setPosicion'
                    res = self.verified_token(string, value)
                    if res['result'] is not None:
                        token = value
                        self.colocation = token
                        self.initialState = 't8'
                else:
                    self.colocation = token
                    self.initialState = 't9'

                # verified an error
                if res['result'] is None:
                    self.show_error(token, 'ERROR - SINTATICO- La propiedad no existe ')
                    break
                # print
                print(f'{self.line} | {self.col} | {token}')
                # change data
                string = res['result']
                self.col += res['count']
                # increment line
                self.next_line()
                # add token
                token_obj = Tokens(token, string)
                self.token_list.append(token_obj)

            elif self.initialState == 't8':
                string = self.multiLinealComents(string)
                string = self.analyze_state('(', string, 't10')

            elif self.initialState == 't9':
                string = self.multiLinealComents(string)
                string = self.analyze_state('(', string, 't11')

            elif self.initialState == 't10':
                string = self.multiLinealComents(string)
                tmp = string.split(")")
                value = tmp[0].split(',')
                verified_numbers(value[0])
                # append to the value list
                self.values_colocation.append(value[0])
                print(f'{self.line} | {self.col} | {value[0]}')
                # add token
                token_obj = Tokens(value[0], string)
                self.token_list.append(token_obj)

                self.tmp_string += value[0]
                string = remove(string, value[0])
                self.initialState = 't12'

            elif self.initialState == 't11':
                string = self.multiLinealComents(string)
                state = True
                tmp = string.split(")")
                value = tmp[0].split(',')
                verified_numbers(value[0])
                for i in self.controlers_list:
                    if value[0] == i.id:
                        state = False
                if state:
                    self.show_error(value[0], 'ERROR - SINTATICO- La variable no esta declarada')
                    break
                # append to the value list
                self.values_colocation.append(value[0])
                print(self.values_colocation)
                print(f'{self.line} | {self.col} | {value[0]}')
                # add token
                token_obj = Tokens(value[0], string)
                self.token_list.append(token_obj)

                self.tmp_string += value[0]
                string = remove(string, value[0])
                self.initialState = 't13'

            elif self.initialState == 't12':
                string = self.multiLinealComents(string)
                string = self.analyze_state(',', string, 't14')

            elif self.initialState == 't13':
                string = self.multiLinealComents(string)
                string = self.analyze_state(')', string, 't15')

            elif self.initialState == 't14':
                string = self.multiLinealComents(string)
                tmp = string.split(")")
                verified_numbers(tmp[0])
                # append to the value list
                self.values_colocation.append(tmp[0])
                print(f'{self.line} | {self.col} | {tmp[0]}')
                # add token
                token_obj = Tokens(tmp[0], string)
                self.token_list.append(token_obj)

                self.tmp_string += tmp[0]
                string = remove(string, tmp[0])
                self.initialState = 't13'

            elif self.initialState == 't15':
                string = self.multiLinealComents(string)
                # create the object or find the property already created
                print(self.property, self.colocation, self.values_colocation)
                if self.colocation == 'setPosicion':
                    property_obj = PropertyClass(self.property, self.colocation, self.values_colocation)
                    self.properties_list.append(property_obj)
                else:
                    colocation_obj = ColocationClass(self.property,self.colocation,self.values_colocation)
                    self.colocations_list.append(colocation_obj)
                string = self.analyze_state(';', string, 't5')
                self.values_colocation = []

            elif self.initialState == 't16':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 't17')

            elif self.initialState == 't17':
                string = self.multiLinealComents(string)
                string = self.analyze_state('-', string, 't18')

            elif self.initialState == 't18':
                string = self.multiLinealComents(string)
                string = self.analyze_state('>', string, 't19')
                self.state = True

        if self.state:
            # show mesage
            messagebox.showinfo(message='Se ha analizado el contenido', title='Analizador')
            # generate css
            #self.generate_css()
            self.generate_html()

    def generate_css(self):
        css = ''
        for i in self.controlers_list:
            controler_id = i.id
            css += f'''
#{controler_id}'''
            css += '''
{'''
            for j in self.properties_list:
                property_control = j
                if controler_id == property_control.control_id:
                    css += f'''
    {property_control.css_style()}
                    '''
            css += '''
}'''
        print(css)

    def generate_html(self):
        list_divs = []
        html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultado</title>
</head>
<body>'''

        for i in self.colocations_list:
            container = i
            print(f'{container.controler_id} - {container.add} - {container.value}')
            # -----
            # global divs
            if container.controler_id == 'this':
                for j in self.controlers_list:
                    controler = j

                    if container.value[0] == controler.id:
                        data = ''
                        for h in self.colocations_list:
                            if container.value[0] == h.controler_id:
                                print(f'Se repite {h.controler_id} en la parte antes de add y se le agrega -> {h.value[0]}')
                                for c in self.controlers_list:
                                    if h.value[0] == c.id:
                                        if c.control == 'Contenedor':
                                            value = c.container_control()
                                            data += value

                        html += f'''
{controler.container_control(data)}'''

        html += '''
</body>
</html>'''
        print(html)

    def compile(self, value):
        # read the file or the content
        content = value.split('\n')
        # Clean data
        new_string = ""
        string_list = []

        for i in content:
            i = i.replace(" ", "")
            i = i.replace("\n", "")
            if i != '':
                new_string += i
                string_list.append(i)

        # print values
        self.string_list = string_list
        # execute
        self.read_states(new_string)

