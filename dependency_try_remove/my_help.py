from webex_bot.models.command import Command

class Respuesta(Command):
    def __init__(self):
        super().__init__(          
            help_message="Mensaje inicial que me dara un mensaje solo en formato texto para decirme que no se encontro el mensaje",
            card=None
            
)
        
    def execute(self, message, attachment_actions, activity):
        return f"No se encontro el comando escrito, pruebe nuevamente o escriba 'help' para más información"