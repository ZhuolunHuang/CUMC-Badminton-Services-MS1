# CUMC-Badminton-Services-MS2
Microservice2 for CUMC Badminton Services, which contains auth and booking sessions

# Notifications

Use [ms2_db.sql](ms2_db.sql) and [db_ms1_create](db_ms1_create.sql) to init database before running application.py.

Step 1：cmd pip install requirements.txt 
if error like 'X509_V_FLAG_CB_ISSUER_CHECK' please use：pip install pyopenssl --upgrade(you can see it in the link: 
'https://stackoverflow.com/questions/73830524/attributeerror-module-lib-has-no-attribute-x509-v-flag-cb-issuer-check')

Step 2: use run edit configuration to set up environment
SQL part please use localhost or RDS; MS2_URL please check another git:
'https://github.com/Keviant/CUMC-Badminton-Services-MS2'
Topic ARN is used when SNS service activated, and key_id, region and sccess key will be reterived by AWS IAM  

Step 3: use AWS EC2 and RDS to reload as cloud service.
 

