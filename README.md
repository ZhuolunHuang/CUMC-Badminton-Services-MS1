# CUMC-Badminton-Services-MS2
Microservice2 for CUMC Badminton Services, which contains auth and booking sessions

# Notifications

Use [ms2_db.sql](ms2_db.sql) to init database before running application.py.

## Some post tests sample:
http://127.0.0.1:5010/api/userprofile/edit/1
{
    "username": "yk888" ,
    "sex":"female",
    "birthday":"2011-2-8",
    "preference":"Single",
    "credits":100,
    "userid":1
}
