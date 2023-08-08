from dependency_try_remove.webex_bot import WebexBot
from service.commands.library import Library
from service.commands.admin import EchoCommand
from storage.api import get


import signal




from storage.db import knowledge_base_advance



class Bot:
    def __init__(self):
        self.bot_process = None
        self.url = {
        'conocimientos':'http://127.0.0.1:8000/api/v1/conocimientos/',
        'temasOld':'http://127.0.0.1:8000/api/v1/temas/',
        'cartas':'http://127.0.0.1:8000/api/v2/cartas',
        'temas':'http://127.0.0.1:8000/api/v2/temas',
        'seccion__tema':'http://localhost:8000/api/v2/info/?seccion__tema=',
        'tema':'http://localhost:8000/api/v2/info/secciones/?tema=',
        } 
        


    def run_bot(self,webex_token):
        bot = WebexBot(
            webex_token,        
            approved_domains=["arcor.com"], 
            bot_name="Ayudante Arcor", 
            include_demo_commands=False,
            bot_help_subtitle="Estos son los comandos que actualmente encuentro en mi base de datos")
        #insert_libraryCommands(bd=knowledge_base_advance, add_command=bot.add_command)     
        self.insert_libraryCommands_v2(add_command=bot.add_command) 
        

        bot.run()
        
    def stop_bot(self):
        # Detener el proceso del bot.
        if self.bot_process:
            self.bot_process.send_signal(signal.SIGINT)
            self.bot_process.wait()
            

        

    def insert_libraryCommands_v2(self,add_command):

     #TODO: implement this function to load commands from a database instead of hardcoded values
     lista_temas = get(self.url['temas'])

     for tema in lista_temas:   
         id = tema["id"]              
         secciones = get(self.url['tema'] + str(id))
         data = get(self.url['seccion__tema']+str(id))
         add_command(Library(get_api=data,reference=tema['nombre'],secciones=secciones))

    def insert_libraryCommands(self,bd, add_command):       
         """
             expresion 
             for elemento in secuencia 
             if condicion
         """

         [
             add_command(Library(bd=v, reference=[word for word in k.split()][0].lower() ))
             for k, v in bd.items() 
             if (command := (add_command(Library(bd=v, reference=[word for word in k.split()][0].lower() )))) is not None
         ]

