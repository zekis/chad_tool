
def run(parameters):
    try:
        # Load Parameters
        filename = parameters.get('filename', 'keys.pkl')
        url = parameters.get('url')
        
        # Logic Goes Here
        response = requests.get(url)
        data = json.loads(response.text)
        key_id = data['key_id']
        secret_key = data['secret_key']
        return key_id, secret_key
    except Exception as e:
        return str(e)