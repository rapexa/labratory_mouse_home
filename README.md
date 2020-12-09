# title : labratory_mouse_home

[![LICENSE](https://img.shields.io/badge/LICENSE-GPL--3.0-green)](https://github.com/jadijadi/sms_serial_verification/blob/master/LICENSE) 
[![Requirements](https://img.shields.io/badge/Requirements-See%20Here-orange)](https://github.com/jadijadi/sms_serial_verification/blob/master/requirements.txt)
[![Todo](https://img.shields.io/badge/Todo-See%20Here-success)](https://github.com/jadijadi/sms_serial_verification/blob/master/TODO.md)

assay subject : effect of electro magnetic fields on human and live creaters
authors : mohammad gharehbagh && sohil shoravarzi

## Todolist :
- [x] make comment and introduction in both code sites
- [x] write readme.mi and make TODOS on it
- [x] add this project on git 
- [x] make aparat link for project and add it to bottom aparat link
- [x] add my sql service to it and sava all of data on it and write the help for this in readme.md <{[id , {info}, timestamp , ... ]}>
- [x] add servo motor + ir distance sensor to all thing as shematic + code >> arduino and python and mysql service and ...
- [x] make data sheet for all ellectrical part of the work <(servo motor and ir distance sensor)>
- [x] add functions in both side arduino and python codes to get all datas at one time in one json file and store them into mysql database
- [x] make pre layout balsamic design for gui its the end of it just continue it.
- [x] make graphical user interface for showing results and charts desktop app or website web service
- [x] add four top pre designed pages in balsamic mokup to flask then work on backend of project
- [x] adding more professional persons to te project :: mr.hoseini and mr.khaderyan
- [x] work on python getsdata function for how to get all datas from that single one function from arduino and save it and show it ...
- [ ] continue work on gui (frontend and backend) and codeing in both arduino and python codes and coninue makeing the electrical parts and mechanical parts (electrival kits and case for all project + mouse holders)
- [ ] recording all (test) and (on way makeing and ...) for this project
- [ ] recordeing the voice of meets that i have with (sohil) for all parts of project
- [ ] writeing assay for result of electromagnetic fields on human and live creaters
- [ ] all works must be text and haveing some things from them
- [ ] write the book for it
- [ ] getting invention certificate for handmade animalkepping dvice that i make it
- [ ] send assay for ISI and so many other diferrent places
- [ ] getting help from mr.hosseini and mr.khaderian
- [ ] engining the all work and make the main pattern for all work
- [ ] makeing graphical pattern for done the project

This project is in way for writing assay for top subject. 

<div dir="rtl"> 
 در این پروژه از تکنولوژی های زیر استفاده می شه:

- opencv
- پایتون
- فلسک
- هسته وای فای esp8266
- مای اسکوئل
- الکترونیک
- میکروکنترلر ها و میکرو پرسسور ها

کل ویدئوها رو می تونین از لینک های زیر ببینین.
</div>

Every single step of this project is screen captures and you can follow them [On Aparat](https://www.aparat.com/assaysohil). 

## How to run
1. Install python3, pip3, virtualenv, arduino+complete(librarys and bourds), MySQL in your system.
2. Clone the project `git clone https://github.com/mgmgst/labratory_mouse_home.git && cd labratory_mouse_home`
5. Create a virtualenv named venv using `virtualenv -p python3 venv`
6. Connect to virtualenv using `source venv/bin/activate`
7. From the project folder, install packages using `pip install -r requirements.txt`
8. Now environment is ready. 
9. edit `app/config.py` as your choice then :
10. run this command `mv app/config.py.sample app/config.py` in project Directory
11. تمام شما الان میتونید رو پروژه کار کنین

### make mysql server for project
1. run this comand in MYSQL database : `CREATE DATABASE alldatas;`

2. run this comand in MYSQL database : `CREATE USER 'nativeuserme'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';`

3. run this comand in MYSQL database : `GRANT ALL PRIVILEGES ON alldatas* TO 'nativeuserme'@'localhost';`

4. run this comand in MYSQL database : `DROP TABLE IF EXISTS ledstatus;`

5. run this comand in MYSQL database : `CREATE TABLE ledstatus (redled VARCHAR(30), yellowled VARCHAR(30) , timestamp  TIMESTAMP);`

6. run this comand in MYSQL database : `DROP TABLE IF EXISTS relaystatus;`

7. run this comand in MYSQL database : `CREATE TABLE relaystatus (light VARCHAR(30),fans VARCHAR(30) ,timestamp  TIMESTAMP);`

8. run this comand in MYSQL database : `DROP TABLE IF EXISTS pirstatus;`

9. run this comand in MYSQL database : `CREATE TABLE pirstatus (motion VARCHAR(30), timestamp  TIMESTAMP);`

10. run this comand in MYSQL database : `DROP TABLE IF EXISTS irstatus;`

11. run this comand in MYSQL database : `CREATE TABLE irstatus (switch VARCHAR(30), timestamp  TIMESTAMP);`

12. run this comand in MYSQL database : `DROP TABLE IF EXISTS dhtstatus;`

13. run this comand in MYSQL database : `CREATE TABLE dhtstatus (hum VARCHAR(30),temp VARCHAR(30) , timestamp  TIMESTAMP);`

14. run this comand in MYSQL database : `DROP TABLE IF EXISTS servostatus;`

15. run this comand in MYSQL database : `CREATE TABLE servostatus (servostatus VARCHAR(30),timestamp  TIMESTAMP);`

16. run this comand in MYSQL database : `DROP TABLE IF EXISTS alldatasstatus;`

17. run this comand in MYSQL database : `CREATE TABLE alldatasstatus (hum VARCHAR(30),temp VARCHAR(30),motion VARCHAR(30),switch VARCHAR(30),redled VARCHAR(30),yellowled VARCHAR(30),light VARCHAR(30),fans VARCHAR(30),servostatus VARCHAR(30),timestamp  TIMESTAMP);`

18. run this comand in MYSQL database : `DROP TABLE IF EXISTS allwritedatasstatus;`

19. run this comand in MYSQL database : `CREATE TABLE allwritedatasstatus (title VARCHAR(60),name VARCHAR(30),weight VARCHAR(30),hight VARCHAR(30),temp VARCHAR(30),Score VARCHAR(30),discr VARCHAR(256),time  TIMESTAMP);`