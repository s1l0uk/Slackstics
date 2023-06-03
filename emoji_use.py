import requests
import pandas

# GET TOKEN
TOKEN = 'xoxp-XXXXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXXXXX'
# APIs
channel_url = 'https://slack.com/api/conversations.list'
msg_url = 'https://slack.com/api/conversations.history'
reaction_url = 'https://slack.com/api/reactions.get'
headers = {'content-type': 'application/x-www-form-urlencoded'}

emj_data = []
channel_res = requests.get(
    url=channel_url, headers=headers, params={'token': TOKEN}
)
channel = [i for i in channel_res.json()['channels']]
for chan in channel:
    msg_params = {
        'token': TOKEN,
        'channel': chan['id']
    }
    msg_res = requests.get(url=msg_url, headers=headers, params=msg_params)
    msg = [i['ts'] for i in msg_res.json()['messages']]
    for m in msg:
        params = {
            'token': TOKEN,
            'channel': chan['id'],
            'timestamp': m
        }
        res = requests.get(url=reaction_url, headers=headers, params=params)
    try:
        for i in res.json()['message']['reactions']:
            emj_data.append(
                {'ts': msg, 'name': i['name'], 'count': i['count']}
            )
    except Exception as e:
        print(e)

emj_df = pandas.DataFrame(emj_data)
print(
    emj_df.groupby('name')['count'].sum().sort_values(ascending=False).head(30)
)
