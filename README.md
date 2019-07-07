# monzo-data-ingest
Ingesting relevant data from the Monzo API

To grab another copy of the access tokens, go to this link

https://auth.monzo.com/?client_id=oauth2client_00009jNbjw1TBhb75yrnlZ&redirect_uri=http://localhost:2020&response_type=code

Grab access key that comes back in the token and add to the bootstrap key in SSM. Then run the bootstrap lambda.