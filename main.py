import requests
import json
from datetime import datetime

from config import url, rules
from setting import template
from mail import send_smtp_mail
from notification import send_sms


def get_data():
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)

    return None


def archive_rates(filename, rates):
    with open(file=f'archive/{filename}.json', mode='w') as file_handler:
        file_handler.write(json.dumps(rates))


def get_preferred_rates(rates):
    if rules['mail']['preferred'] is not None:
        preferred_rates = dict()
        for rate in rules['mail']['preferred']:
            preferred_rates[rate] = rates[rate]
        rates = preferred_rates

    return rates


def send_mail(subject, rates):
    now = datetime.now().strftime('%Y-%b-%d  %a  %H:%M')
    subject = f'{subject} - {now} rates'

    rates = get_preferred_rates(rates)

    render = template.render(
        currency=rates
    )

    send_smtp_mail(subject, render)


def check_notify(rates):
    preferred_rates = rules['notification']['preferred']

    msg = ''
    for rate in preferred_rates.keys():
        if rates[rate] <= preferred_rates[rate]['min']:
            msg += f'{rate} reached min : {rates[rate]} \n'

        if rates[rate] >= preferred_rates[rate]['max']:
            msg += f'{rate} reached max : {rates[rate]} \n'

    return msg


def send_notification(msg):
    now = datetime.now().strftime('%Y-%b-%d  %a  %H:%M')
    msg = f'{now}\n\n{msg}'
    send_sms(msg)


if __name__ == '__main__':
    data = get_data()

    get_timestamp = data['timestamp']
    get_rates = data['rates']

    if rules['archive']['enable']:
        archive_rates(get_timestamp, get_rates)

    if rules['mail']['enable']:
        send_mail(get_timestamp, get_rates)

    if rules['notification']['enable']:
        notification_message = check_notify(get_rates)

        if notification_message:
            send_notification(notification_message)
