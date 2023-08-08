import logging
from webexteamssdk.models.cards import  TextBlock, FontWeight,HorizontalAlignment, FontSize,Spacing, Column, AdaptiveCard, ColumnSet, Image
from webexteamssdk.models.cards.actions import Submit
from webex_bot.models.command import Command
from webex_bot.models.response import response_from_adaptive_card
from service.utils.clean_function import list_showCard, create_url
from service.utils.validators import generar_texto_centralizado


log = logging.getLogger(__name__)

class Library(Command):

    def __init__(self, get_api ,reference,secciones):
        self.reference = generar_texto_centralizado(reference.lower(),20)
        self.get_api = get_api   
        self.secciones = secciones 
        super().__init__(
            command_keyword=self.reference,
            help_message=f"{self.reference}",
            chained_commands=[LibraryCallback(callback_reference=self.reference)],
            card_callback_keyword=self.reference)            
        

    def execute(self, message, attachment_actions, activity):
        titulo = TextBlock(f"Información sobre {self.reference}", weight=FontWeight.DEFAULT, size=FontSize.MEDIUM)
        actionList = list_showCard(self.get_api,type='final',reference=self.reference,secciones=self.secciones)
        card = AdaptiveCard(
            body=[titulo ],
            actions=actionList
            )
        return response_from_adaptive_card(card)
    
    
    
class LibraryCallback(Command):

    def __init__(self,callback_reference):
        self.reference = callback_reference
        super().__init__(
            card_callback_keyword=f"{self.reference}_callback",            
            delete_previous_message=True)


    def execute(self, message, attachment_actions, activity):
        
        items = []
        actions = []
        pregunta = attachment_actions.inputs['value']['pregunta']        
        respuesta = attachment_actions.inputs['value']['respuesta']
        get_api = attachment_actions.inputs['value']     

        
        text1 = TextBlock(pregunta, weight=FontWeight.DEFAULT, size=FontSize.LARGE,horizontalAlignment=HorizontalAlignment.CENTER,wrap=True)
        text2 = TextBlock(respuesta,
                          wrap=True,horizontalAlignment=HorizontalAlignment.LEFT,weight=FontWeight.DEFAULT,size=FontSize.MEDIUM,spacing=Spacing.PADDING)        
        items.append(text1)
        items.append(text2)
        """if "url" in get_api:
            if "url_name" in get_api:
                title = get_api['url_name']
            else:
                title = "Más Información"
            
            url = create_url(url=get_api['url'],title=title)
            actions.append(url)
        if "img" in get_api:
            img = Image(url=get_api['img'], size=ImageSize.AUTO)
            items.append(img)"""

        submit = Submit(title="Preguntar otra vez",
                        data={
                            "callback_keyword": self.reference
                            })
        actions.append(submit)
        card = AdaptiveCard(
            body=[ColumnSet(columns=[Column(items=items, width=2)])
                  ], actions=actions)

        return response_from_adaptive_card(card)
