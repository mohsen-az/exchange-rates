BASE_URL = 'http://data.fixer.io/api/latest?access_key='
API_KEY = 'FIXER_API_KEY'

url = BASE_URL + API_KEY

rules = {

    'archive': {
        'enable': True
    },

    'mail': {
        'enable': True,
        'preferred': ['BTC', 'USD', 'IRR']
    },

    'notification': {
        'enable': True,
        'receiver': 'PHONE_NUMBER',
        'preferred': {
            'USD': {'min': 1.00, 'max': 1.30},
            'IRR': {'min': 45000, 'max': 55000},
        }
    }

}
