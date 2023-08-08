import requests


    


url = ['http://127.0.0.1:8000/api/v1/conocimientos/','http://127.0.0.1:8000/api/v1/temas/','http://127.0.0.1:8000/api/v2/cartas'] 
    

def get(url):
    

    try:
        response = requests.get(url)

        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            data = response.json()  # Si la respuesta es JSON
            # Realiza las operaciones que necesites con los datos recibidos
           


        else:
            data = f'Error al hacer la solicitud: {response.status_code}'

    except requests.exceptions.RequestException as e:
        data=f'Error de conexión: {e}'           
        
    return data

    
