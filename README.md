# monzo-data-ingest
Ingesting relevant data from the Monzo API

To grab another copy of the access tokens, go to this link

https://auth.monzo.com/?client_id=oauth2client_00009jNbjw1TBhb75yrnlZ&redirect_uri=http://localhost:2020&response_type=code

Grab access key that comes back in the token

Then POST to
"https://api.monzo.com/oauth2/token" \
    "grant_type=authorization_code" \
    "client_id=oauth2client_00009jNbjw1TBhb75yrnlZ" \
    "client_secret=$client_secret" \
    "redirect_uri=http://localhost:2020" \
    "code=$authorization_code"

Then POST to
https://api.monzo.com/oauth2/token/?grant_type=authorization_code&client_id=oauth2client_00009jNbjw1TBhb75yrnlZ&client_secret=*************&redirect_uri=http://localhost:2020&code=**********************


"https://api.monzo.com/oauth2/token" \
    "grant_type=authorization_code" \
    "client_id=oauth2client_00009jNbjw1TBhb75yrnlZ" \
    "client_secret=$client_secret" \
    "redirect_uri=http://localhost:2020" \
    "code=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6InNucFV2QnRsWmZtRytpQXdYenpZIiwianRpIjoiYXV0aHpjb2RlXzAwMDA5a2MwMFZ4T1c3QVQ2UkNIajciLCJ0eXAiOiJhemMiLCJ2IjoiNSJ9.oVXEuR1bUX9sFfsNzJFHWLb7dRk9ESBozMHZeEIdM4Vyr6CKsPEUpWkU4w1RhHt7iHkmoAjEpoK_TAunv7FNuw"

eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6InNucFV2QnRsWmZtRytpQXdYenpZIiwianRpIjoiYXV0aHpjb2RlXzAwMDA5a2MwMFZ4T1c3QVQ2UkNIajciLCJ0eXAiOiJhemMiLCJ2IjoiNSJ9.oVXEuR1bUX9sFfsNzJFHWLb7dRk9ESBozMHZeEIdM4Vyr6CKsPEUpWkU4w1RhHt7iHkmoAjEpoK_TAunv7FNuw

