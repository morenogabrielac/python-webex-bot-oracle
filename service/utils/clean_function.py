
from webexteamssdk.models.cards import TextBlock, AdaptiveCard
from webexteamssdk.models.cards.actions import Submit, ShowCard,OpenUrl
from service.utils.validators import generar_texto_centralizado



def list_showCard(api_info,type = None,reference = None, secciones= None):
    
        """
        A list of showCards.

        Args:
            api_info (dictionary): Repository where the information will be stored.
            type (String): type of action to do.
                Choices: 'subtema', 'quest'

        Returns:
            type: List[]
        """
        lista = []
        for seccion in secciones:
            id_seccion_a_filtrar = seccion['id']
            btn_name = generar_texto_centralizado(seccion['nombre'],20)
            
            diccionarios_filtrados = [diccionario for diccionario in api_info if diccionario.get('seccion',{}).get('id') == id_seccion_a_filtrar]
            unit_showCard = create_showCard( btn_name=btn_name,api = diccionarios_filtrados, type=type, reference=reference)
              
                

            lista.append(unit_showCard)            
        return lista


def create_showCard(btn_name,api,type,reference):
        actions = []
        body = []            
        if(type == "final"):
            actions.extend( list_submit(api=api,reference=reference))                
        if(type == "recursivo"):            
            lista_subtemas = list_showCard(api,type="final")
            actions.extend(lista_subtemas)  
        adaptativeCard = AdaptiveCard(body=body,actions=actions)
        showcard = ShowCard(card=adaptativeCard, title=btn_name)
        return  showcard
    
def list_submit(api,reference):
        actions = []        
        for element in api:
        #----------------------------
            pregunta =  element['pregunta'] 
        #---------------------------        
            submit = create_submit(title=pregunta, callback_keyword=f"{reference}_callback", value=element)
            actions.append(submit) 
        return actions   
    
def create_submit(title="submit", callback_keyword = None, **kwargs):
        submit = Submit(title=f'{title}',
                data={
                    "callback_keyword": callback_keyword,
                    **kwargs
                    })        
        return submit
    
def create_url(url,title):
    url = OpenUrl(url,title)
    
    return url


def list_text( api):
    respuesta = 'Información disponible hasta el momento:\n '
    for key, value in api.items():
        respuesta = respuesta + str(key)  + ': ' + value['pregunta'] + '\n' 
    text = TextBlock(text= respuesta,
                        wrap=True)        
    return text


