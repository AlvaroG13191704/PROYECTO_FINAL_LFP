class PropertyClass:
    def __init__(self, control_id, property, value):
        self.control_id = control_id
        self.property = property
        self.value = value


    # here the functions to return the css documentation
    def css_style(self):

        if self.property == 'setPosicion':
            css = f'''
    position: absolute; 
    left: {self.value[0]}px; 
    top: {self.value[1]}px;'''
            return css

        elif self.property == 'setAncho':
            css = f'''
    width:{self.value[0]}px;'''
            return css

        elif self.property == 'setAlto':
            css = f'''
    height:{self.value[0]}px;'''
            return css

        elif self.property == 'setColorFondo':
            css = f'''
    background-color:rgb{int(self.value[0]),int(self.value[1]),int(self.value[2])};'''
            return css

        elif self.property == 'setColorLetra':
            css = f'''
    color:rgb{int(self.value[0]),int(self.value[1]),int(self.value[2])};'''
            return css

        elif self.property == 'setTexto':
            return ''

        elif self.property == 'setMarcada':
            return ''

        elif self.property == 'setGrupo':
            return ''
        elif self.property == 'setAlineacion':
            return ''