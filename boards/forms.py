import json

from django import forms
from django.conf import settings
import requests
import logging
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1


class DictionaryForm(forms.Form):

    word = forms.CharField(max_length=100)

    def search(self):
        result = {}
        word = self.cleaned_data['word']

        endpoint = 'https://od-api.oxforddictionaries.com/api/v2/entries/{source_lang}/{word_id}'
        url = endpoint.format(source_lang='en', word_id=word)
        headers = {'app_id': settings.OXFORD_APP_ID, 'app_key': settings.OXFORD_APP_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:  # SUCCESS
            result = response.json()

            result['success'] = True
            print(json.dumps(result,indent=4, sort_keys=True))
        else:
            result['success'] = False
            if response.status_code == 404:  # NOT FOUND
                result['message'] = 'No entry found for "%s"' % word
            else:
                result['message'] = 'The Oxford API is not available at the moment. Please try again later.'
        return result


class FindMyShiftForm(forms.Form):

    word = forms.CharField(max_length=100)

    def search(self):
        result = {}
        word = self.cleaned_data['word']
        #logging.basicConfig()
        #logging.getLogger().setLevel(logging.DEBUG)
        #requests_log = logging.getLogger("requests.packages.urllib3")
        #requests_log.setLevel(logging.DEBUG)
        #requests_log.propagate = True

        #endpoint ='https://www.findmyshift.com/api/1.1/reports/shifts -d apiKey={apiKey} -d teamId={teamId} -d from={fromdt} -d to={todt}'
        #url = endpoint.format(apiKey=settings.FINDMYSHIFT_APP_ID, teamId=settings.FIND_MY_SHIFT_TEAM_ID, fromdt=word, todt=word)
        #print(url)


        endpoint = 'https://www.findmyshift.com/api/1.1/reports/shifts'
        headers = {'apiKey': settings.FINDMYSHIFT_APP_ID, 'teamId': settings.FIND_MY_SHIFT_TEAM_ID, 'from':word,'to':word }
        response = requests.get(endpoint,headers)
        print(response.request.headers)
        print(response.status_code)



        if response.status_code == 200:  # SUCCESS
            result = response.json()

            result[0]['success']= True
            print(json.dumps(result, indent=4, sort_keys=True))
            #result['success'] = True
        else:
            result['success'] = False
            if response.status_code == 404:  # NOT FOUND
                result['message'] = 'No entry found for "%s "' % url
            else:
                result['message'] = 'The FindMyShift API is not available at the moment. Please try again later.'
        return result
