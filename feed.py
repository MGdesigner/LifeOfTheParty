import facebook


access_token = '201793946507565%7C2.GvNfZZBc6rRObaf2oGWadg__.3600.1301122800-100002268818038%7CZieF2kcaynYqHsPhWbNxo1OMigg' # LifeOf TheParty
event_id = '130842913653732'  # Hackathon

graph = facebook.GraphAPI(access_token)

print graph.get_connections(event_id, 'feed')

