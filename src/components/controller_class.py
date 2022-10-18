

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
            self.properties = ['setTexto', 'setMarcada', 'setAlineacion','setColorFondo']
        elif self.control == 'AreaTexto':
            self.properties = ['setTexto']
        elif self.control == 'Clave':
            self.properties = ['setTexto', 'setAlineacion']
        elif self.control == 'Contenedor':
            self.properties = ['setColorFondo', 'setAncho', 'setAlto']
