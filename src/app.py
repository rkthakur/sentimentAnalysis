import os
import sys
import json
import time
import pprint
import traceback

import jwt_helper
#import predictionVisionAPI
import predictionSentiment
import token_generator

import pandas
from textblob import TextBlob
from Crypto.PublicKey import RSA

#Replace all comma from that single coulumn CSV file
def cleandata(file_name):
    from pathlib2 import Path
    path = Path(file_name)
    text = path.read_text()
    text = text.replace(',', ' ')
    path.write_text(text)
    
def textStatistics(file_name):
    df = pandas.read_csv(file_name)
    df['word_count'] = df['citation'].apply(lambda x: len(str(x).split(" ")))
    df['sentiment_local'] = df['citation'].apply(lambda x: TextBlob(x).sentiment[0])
    #df=df[['citation','word_count']].head()
    df.to_csv(file_name, index=False)


def main():
    try:       
        account_id='rthakur@sapient.com' 
        private_key = open("einstein_platform.pem","r").read()
                
        # Set expiry time
        expiry = int(time.time()) + (15*60)

        # Generate an assertion using RSA private key
        assertion = jwt_helper.generate_assertion(account_id, private_key, expiry)

        # Obtain oauth token
        token = token_generator.generate_token(assertion)
        response = token.json()

        # If there is no token print the response
        if 'access_token' not in response:
            raise ValueError("Access token generation failed. Received reply: \"{}\"".format(response))
        else:
        # Collect the access token from response
            access_token = response['access_token']
            
            
        #data_file='Rakesh_Sample.csv' #SFCC_Q1_2019_Recognition_Data.csv'
        data_file='SFCC_Q1_2019_Recognition_Data1.csv'
        data_file_with_sentiment="Sentiment_of_"+data_file
        cleandata(data_file)
        df = pandas.read_csv(data_file)

        #Add three additional column to update sentiment value for the text
        df.insert(1,'positive','')
        df.insert(2,'neutral','')
        df.insert(3,'negative','')
        #df.insert(4,'word_count','')
                
        for index, row in df.iterrows():
                # Make a Sentiment prediction call
                
                print('Submited request for sentiment analysis of of text index #', index)
                prediction_url_response = predictionSentiment.predict(access_token,row['citation'])
                print('Recieved sentiment for text index #',index)
                # Print prediction response
                resp=prediction_url_response.json()
                probabilities=resp['probabilities']

                for sentiment in probabilities:
                    #pprint.pprint(sentiment)
                    if sentiment['label'] == 'positive':
                         row['positive'] = sentiment['probability']
                    elif sentiment['label'] == 'neutral':
                         row['neutral'] = sentiment['probability']
                    elif sentiment['label'] == 'negative':
                         row['negative'] = sentiment['probability']

        df.to_csv(data_file_with_sentiment)
        textStatistics(data_file_with_sentiment)
       
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
