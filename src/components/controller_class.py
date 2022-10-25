class ControlersClass:

    def __init__(self, control, id):
        self.control = control
        self.id = id
        self.properties = None
        self.setProperties()

    def setProperties(self):
        if self.control == 'Etiqueta':
            self.properties = ['setColorLetra', 'setTexto', 'setColorFondo', 'setAncho', 'setAlto']
        elif self.control == 'Boton':
            self.properties = ['setTexto', 'setAlineacion']
        elif self.control == 'Check':
            self.properties = ['setTexto', 'setMarcada', 'setGrupo']
        elif self.control == 'RadioBoton':
            self.properties = ['setTexto', 'setMarcada', 'setGrupo']
        elif self.control == 'Texto':
            self.properties = ['setTexto', 'setMarcada', 'setAlineacion', 'setColorFondo']
        elif self.control == 'AreaTexto':
            self.properties = ['setTexto']
        elif self.control == 'Clave':
            self.properties = ['setTexto', 'setAlineacion']
        elif self.control == 'Contenedor':
            self.properties = ['setColorFondo', 'setAncho', 'setAlto']

    # this functions received some parameters to build the html
    def label_control(self, text=""):
        return f'''
    <label id="{self.id}">{text.replace('"','')}</label>'''

    def button_control(self, text="", align='left'):
        return f'''
    <input type="submit" id="{self.id}" value={text.replace('"','')} style="text-align:{align}"/> '''

    def check_control(self, check=False, text=""):
        checked = ''
        if check:
            checked = 'checked'
        return f'''
    <input type="checkbox" id={self.id} {checked} />{text.replace('"','')} '''

    def radioButton_control(self, check=False, group="", text=""):
        checked = ''
        if check:
            checked = 'checked'
        return f'''
    <input type="radio" name="{group}" id="{self.id}" {checked} />{text.replace('"','')} '''

    def textArea_control(self, text=""):
        return f'''
    <textarea id="{self.id}"> {text.replace('"','')} </textarea>'''

    def key_control(self, text='', align="left"):
        return f'''
    <input type="password" id="{self.id}" value={text} style="text-align:{align}" /> '''

    def container_control(self, control=""):
        return f'''
    <div id="{self.id}"> 
        {control}
    </div> '''

    def text_control(self, text="", align="left"):
        return f'''
    <input type="text" id="{self.id}" value={text} style="text-align:{align}" /> '''
