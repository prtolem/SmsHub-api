import json

import aiohttp


class SMShub:
    def __init__(self, api_key, session: aiohttp.ClientSession):
        self.api_key = api_key
        self.session = session

    async def get_numbers_count(self, country: str, operator: str):
        params = {
            'api_key': self.api_key,
            'action': 'getNumbersStatus',
            'country': country,
            'operator': operator,
        }
        async with self.session.get(url='https://smshub.org/stubs/handler_api.php', params=params) as response:
            return await response.json()

    async def get_balance(self) -> float:
        params = {
            'api_key': self.api_key,
            'action': 'getBalance',
        }
        async with self.session.get(url='https://smshub.org/stubs/handler_api.php', params=params) as response:
            response = await response.text()
            if 'ACCESS_BALANCE' in response:
                return int(response.split(':')[1])
            elif response == 'BAD_KEY':
                raise SMShubBadKey('Bad API key {}'.format(self.api_key))
            elif response == 'ERROR_SQL':
                raise SMShubErrorSQL('SQL error')
            elif response == 'BAD_ACTION':
                raise SMShubBadAction('Bad action {}'.format(params['action']))

    async def get_number(self, country: str, operator: str, service: str) -> dict:
        params = {
            'api_key': self.api_key,
            'action': 'getNumber',
            'country': country,
            'operator': operator,
            'service': service,
        }
        async with self.session.get(url='https://smshub.org/stubs/handler_api.php', params=params) as response:
            response = await response.text()
            if 'ACCESS_NUMBER' in response:
                return {
                    'id': response.split(':')[1],
                    'number': response.split(':')[2],
                }
            elif response == 'NO_NUMBERS':
                raise SMShubNoNumbers('No numbers for country {} and service {}'.format(country, service))
            elif response == 'NO_BALANCE':
                raise SMShubNoBalance('No balance for {}'.format(self.api_key))
            elif response == 'WRONG_SERVICE':
                raise SMShubWrongService('Wrong service {}'.format(service))

    async def set_status(self, activation_id: str, new_status: str) -> bool:
        params = {
            'api_key': self.api_key,
            'action': 'setStatus',
            'id': activation_id,
            'status': new_status,
        }
        async with self.session.get(url='https://smshub.org/stubs/handler_api.php', params=params) as response:
            response = await response.text()
            if response == 'ACCESS_READY' or response == 'ACCESS_RETRY_GET' or response == 'ACCESS_ACTIVATION' or response == 'ACCESS_CANCEL':
                return True
            elif response == 'BAD_ACTION':
                raise SMShubBadAction('Bad action {}'.format(params['action']))
            elif response == 'BAD_SERVICE':
                raise SMShubWrongService('Wrong service')
            elif response == 'BAD_KEY':
                raise SMShubBadKey('Bad API key {}'.format(self.api_key))
            elif response == 'NO_ACTIVATION':
                raise SMShubNoActivation('No activation with id {}'.format(activation_id))
            elif response == 'ERROR_SQL':
                raise SMShubErrorSQL('SQL error')

    async def get_status(self, activation_id: str) -> str:
        params = {
            'api_key': self.api_key,
            'action': 'getStatus',
            'id': activation_id,
        }
        async with self.session.get(url='https://smshub.org/stubs/handler_api.php', params=params) as response:
            response = await response.text()
            if response == 'STATUS_WAIT_CODE':
                return 'STATUS_WAIT_CODE'
            elif response == 'STATUS_WAIT_RESEND':
                return 'STATUS_WAIT_RESEND'
            elif response == 'STATUS_CANCEL':
                return 'STATUS_CANCEL'
            elif response == 'STATUS_OK':
                return 'STATUS_OK'
            elif response == 'BAD_KEY':
                raise SMShubBadKey('Bad API key {}'.format(self.api_key))
            elif response == 'BAD_ACTION':
                raise SMShubBadAction('Bad action {}'.format(params['action']))
            elif response == 'NO_ACTIVATION':
                raise SMShubNoActivation('No activation with id {}'.format(activation_id))
            elif response == 'ERROR_SQL':
                raise SMShubErrorSQL('SQL error')

    async def get_all_prices(self, service, country) -> dict:
        params = {
            'api_key': self.api_key,
            'action': 'getPrices',
            'service': service,
            'country': country,
        }
        async with self.session.get(url='https://smshub.org/stubs/handler_api.php', params=params) as response:
            response = await response.text()
            return json.loads(response)


# Exceptions
class SMShubBadKey(Exception):
    pass


class SMShubErrorSQL(Exception):
    pass


class SMShubBadAction(Exception):
    pass


class SMShubNoNumbers(Exception):
    pass


class SMShubNoBalance(Exception):
    pass


class SMShubWrongService(Exception):
    pass


class SMShubNoActivation(Exception):
    pass
