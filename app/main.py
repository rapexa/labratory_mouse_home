# start includeing librarys that we need for work
import subprocess
import requests
import mysql.connector
import threading
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
from time import sleep
from flask import Flask , render_template,request , redirect,jsonify, flash, url_for, Response, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from singlemotiondetector  import SingleMotionDetector
from imutils.video import VideoStream
import collect, config, mysqlmanager
# end includeing librarys that we need for work

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()

vs = VideoStream(src=0).start()
time.sleep(2.0)

# start flask app
app = Flask(__name__)

# config flask secret key
app.config.update(
    SECRET_KEY = config.SECRET_KEY #"secretxxx"
)

# config flask limmiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "%d" % (self.id)


# create some users with ids 1 to 20       
user = User(0)

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')   
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)    

@app.route("/ok")
def sys_check():
    '''this function tell that falsk server is ok and running!!'''
    ret = {'status':'ok','message':'[+] flask server is running'}
    return jsonify(ret) , 200

@app.route('/time_feed')
def time_feed():
    '''tihs function make time to show in main page but i did'nt use it its for future plan'''
    def generate():
        while True:
            yield datetime.datetime.now().strftime("%Y.%m.%d|%H:%M:%S")
            time.sleep(1)
    return Response(generate(), mimetype='text')

# main route for flask server and url methods ar post and get
@app.route('/',methods=["GET", "POST"])
@login_required
def index():
    '''this function handle main page''' 

    latestwork = mysqlmanager.reading_latestwritedatas_to_database()
    latestworka=[]
    for last in latestwork:
        title, name, weight, hight, temp, Score, discr, time = last
        latestworka.append({"title":title,"name":name,"weight":weight,"hight":hight,"temp":temp,"Score":Score,"discr":discr,"time":time})
    
    latestdht = mysqlmanager.reading_latestdhtstatus_to_database()
    latestdhts =[]
    for dht in latestdht:
        hum, temp, timestamp = dht
        latestdhts.append({"hum":hum,"temp":temp,"timestamp":timestamp})

    latestdata = mysqlmanager.reading_alllatestdatas_to_database()
    datas = []
    for data in latestdata:
        hum, temp, motion, switch, redled, yellowled, light, fans, servostatus, timestamp = data
        datas.append({"hum":hum,"temp":temp,"motion":motion,"switch":switch,"redled":redled,"yellowled":yellowled,"light":light,"fans":fans,"servostatus":servostatus,"timestamp":timestamp})

    return render_template('dashboard.html', data = {"latestworks" : latestworka, "latestdhts":latestdhts, "datas" : datas})

# documentation route for flask server
@app.route('/doc')
@login_required
def doc(): 
    ''' this function handle documantation page for requests coming for route '''
    return render_template('documentation.html')

# all datas tables page route for flask server
@app.route('/table')
@login_required
def table(): 
    '''this function handle tables page for request comeing for this route'''

    all_work = mysqlmanager.reading_writedatas_to_database()
    works = []
    for work in all_work:
        title, name, weight, hight, temp, Score, discr, time = work
        works.append({"title":title,"name":name,"weight":weight,"hight":hight,"temp":temp,"Score":Score,"discr":discr,"time":time})

    latestwork = mysqlmanager.reading_latestwritedatas_to_database()
    latestworka=[]
    for last in latestwork:
        latesttitle, latestname, latestweight, latesthight, latesttemp, latestScore, latestdiscr, latesttime = last
        latestworka.append({"latesttitle":latesttitle,"latestname":latestname,"latestweight":latestweight,"latesthight":latesthight,"latesttemp":latesttemp,"latestScore":latestScore,"latestdiscr":latestdiscr,"latesttime":latesttime})

    alldatas = mysqlmanager.reading_alldatas_to_database()
    datas = []
    for data in alldatas:
        hum, temp, motion, switch, redled, yellowled, light, fans, servostatus, timestamp = data
        datas.append({"hum":hum,"temp":temp,"motion":motion,"switch":switch,"redled":redled,"yellowled":yellowled,"light":light,"fans":fans,"servostatus":servostatus,"timestamp":timestamp})


    latestdht = mysqlmanager.reading_latestdhtstatus_to_database()
    latestdhts =[]
    for dht in latestdht:
        hum, temp, timestamp = dht
        latestdhts.append({"hum":hum,"temp":temp,"timestamp":timestamp})

    return render_template('tables.html', data = {"works" : works, "latestworks" : latestworka, "datas" : datas, "latestdhts":latestdhts})

# control devices page route for flask server
@app.route('/control', methods=["GET", "POST"])
@login_required
def control_Page(): 
    '''this function handle control page for request comeing for this route'''

    if request.method == 'POST':

        REDLED = request.form["REDLED"]
        YELLOWLED = request.form["YELLOWLED"]
        FANS = request.form["FANS"]
        LIGHT = request.form["LIGHT"]
        DOOR = request.form["DOOR"]

        if REDLED == "RED_ON":

            ledcontrol("ledred","on")
            getalldatas()
            flash("DONE.")

        if REDLED == "RED_OFF":
    
            ledcontrol("ledred","off")
            getalldatas()
            flash("DONE.")

        if YELLOWLED == "YELLOW_ON":
    
            ledcontrol("ledyellow","on")
            getalldatas()
            flash("DONE.")

        if YELLOWLED == "YELLOW_OFF":
    
            ledcontrol("ledyellow","off")
            getalldatas()
            flash("DONE.")

        if FANS == "FANS_ON":
    
            relaycontrol("fans","on")
            getalldatas()
            flash("DONE.")

        if FANS == "FANS_OFF":
    
            relaycontrol("fans","off")
            getalldatas()
            flash("DONE.")

        if LIGHT == "LIGHT_ON":
    
            relaycontrol("light","on")
            getalldatas()
            flash("DONE.")

        if LIGHT == "LIGHT_OFF":
    
            relaycontrol("light","off")
            getalldatas()
            flash("DONE.")                                                                        

        if DOOR == "DOOR_OPEN":
        
            servocontrol("servo","open")
            getalldatas()
            flash("DONE.")

        if DOOR == "DOOR_CLOSE":
    
            servocontrol("servo","close")
            getalldatas()
            flash("DONE.")

        return redirect('/control')

    return render_template('control_Page.html')

# live camera page route for flask server
@app.route('/camera')
@login_required
def camera_Page(): 
    '''this function handle live camera page for request comeing for this route'''
    return render_template('live_camera.html') 

# add datas page route for flask server and url methods ar post and get
@app.route('/add',methods=["GET", "POST"])
@login_required
def add(): 
    '''this function handle add datas page for request comeing for this route'''

    if request.method == 'POST':

        title = request.form["title"]
        name = request.form["name"]
        weight = request.form["weight"]
        hight = request.form["hight"]
        temp = request.form["temp"]
        Score = request.form["Score"]
        discr = request.form["discr"]
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        mysqlmanager.writing_writedatas_to_database(title, name, weight, hight, temp, Score, discr, timestamp)

        flash('your information added seccussfully','info')

        return redirect('/')        

    else:
        return render_template('add.html')

# login route for flask server that have limmiter (10 times) for stop brute force attaks and have check and its methods are posta nd get           
@app.route('/login',methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():

    # subprocess.Popen(["python", "collect.py"])  TODO: uncomment this line when i wana deploy project done.

    '''this function return login page'''
    error = None
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["Password"]
        if check(username,password):
            login_user(user)
            flash('You were successfully logged in','info')
            return redirect(url_for('index'))
        else:
            error = '!!!invalid user!!!' 
               
    return render_template('login.html', error=error)

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped

def check(username,password):
    res = False
    if username == config.username and password == config.password:
        res = True
    return res               

def detect_motion(frameCount):
    	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock
	# initialize the motion detector and the total number of frames
	# read thus far
	md = SingleMotionDetector(accumWeight=0.1)
	total = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7, 7), 0)
		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		# if the total number of frames has reached a sufficient
		# number to construct a reasonable background model, then
		# continue to process the frame
		if total > frameCount:
			# detect motion in the image
			motion = md.detect(gray)
			# check to see if motion was found in the frame
			if motion is not None:
				# unpack the tuple and draw the box surrounding the
				# "motion area" on the output frame
				(thresh, (minX, minY, maxX, maxY)) = motion
				cv2.rectangle(frame, (minX, minY), (maxX, maxY),
					(0, 0, 255), 2)
		
		# update the background model and increment the total number
		# of frames read thus far
		md.update(gray)
		total += 1
		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

def getalldatas():
    '''this function get all datas by one json code and store them into mysql database in each seprate tables and in one great table'''

    url = 'http://10.10.10.1/jsond'
    respon = requests.get(url)
    
    hum = respon.json()['humadity']
    temp = respon.json()['temperature']
    motion = respon.json()['motion']
    switch = respon.json()['switch']
    redled = respon.json()['redled']
    yellowled = respon.json()['yellowled']
    light = respon.json()['light']
    fans = respon.json()['fans']
    servostatus = respon.json()["servo"]
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    mysqlmanager.writing_dhtstatus_to_database(hum, temp, timestamp)
    mysqlmanager.writing_pirstatus_to_database(motion, timestamp)
    mysqlmanager.writing_irstatus_to_database(switch, timestamp)
    mysqlmanager.writing_ledstatus_to_database(redled, yellowled, timestamp)
    mysqlmanager.writing_relaystatus_to_database(light, fans, timestamp)
    mysqlmanager.writing_servostatus_to_database(servostatus, timestamp)

    mysqlmanager.writing_alldatas_to_database(hum, temp, motion, switch, redled, yellowled, light, fans, servostatus, timestamp)

    return hum, temp, motion, switch, redled, yellowled, light, fans, servostatus

def getroomstatus():
    '''this function read room temperature and humadity'''

    url = 'http://10.10.10.1/readroomddata'
    respon = requests.get(url)
    hum = respon.json()['humadity']
    temp = respon.json()['temperature']

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    mysqlmanager.writing_dhtstatus_to_database(hum, temp, timestamp)

    return temp, hum

def getpirstatus():
    '''this function read human motion detect in work place'''

    url = 'http://10.10.10.1/readpirdata'
    respon = requests.get(url)
    motion = respon.json()['motion']
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    mysqlmanager.writing_pirstatus_to_database(motion,timestamp)

    return motion

def getirstatus():
    '''this function read food switch status in work place'''

    url = 'http://10.10.10.1/readirdata'
    respon = requests.get(url)
    switch = respon.json()['switch']
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    mysqlmanager.writing_irstatus_to_database(switch,timestamp)

    return switch

def ledcontrol(led,status):
    '''this function can control showing bar status leds'''

    if ledcheck(led,status):
        url = f'http://10.10.10.1/control_led?{led}={status}'
        respon = requests.get(url)
        redled = respon.json()['redled']
        yellowled = respon.json()['yellowled']
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        mysqlmanager.writing_ledstatus_to_database(redled,yellowled,timestamp)
        
        return redled, yellowled
    
    else:
        return 'your givin elements is not true'

def relaycontrol(relaypin, status):
    '''this function can control relays that control lights and fans'''
    
    if relaycheck(relaypin,status):
        url = f'http://10.10.10.1/control_relay?{relaypin}={status}'
        respon = requests.get(url)

        stuffs = {'light' : respon.json()['light'],
        'fans' : respon.json()['fans'],}
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        mysqlmanager.writing_relaystatus_to_database(stuffs['light'],stuffs['fans'],timestamp)

        return stuffs
    else:
        return 'your givin elements is not true'

def servocontrol(servo, status):
    '''this function can control servo that control food door'''
    
    if servocheck(servo,status):
        url = f'http://10.10.10.1/control_servo?{servo}={status}'
        respon = requests.get(url)

        servostatus = respon.json()["servo"]
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        mysqlmanager.writing_servostatus_to_database(servostatus,timestamp)

        return servostatus
    else:
        return 'your givin elements is not true'

def logoutarduino():
    '''this function logout from server'''

    url = "http://10.10.10.1/login?DISCONNECT=YES"    
    respon = requests.get(url)

    return respon
    
def loginarduino():
    '''this function login into server'''

    username = 'mgmgst'
    password = '1051154731'
    url = f'http://10.10.10.1/login?USERNAME={username}&PASSWORD={password}'
    session = requests.session()
    respon = session.get(url)
    
    if respon.status_code == 200:
        return session
    
    else:
        return f'can not login error : {respon.status_code}'
            
def ledcheck(led,status):
    '''this function check that we send right data for controling status led light bars or not'''

    ret = False
    leds = ['ledred' , 'ledyellow' ,'all']
    statuss = ['on' , 'off']
    if led in leds and status in statuss:
        ret = True
        
    return ret

def relaycheck(relaypin, status):
    '''this function check that we send right data for controling relays that they control power stuff or not'''
    ''' in this function relay1 == light & relay2 == fans '''

    ret = False
    relays = ['light', 'fans']
    statuss = ['on', 'off']
    if relaypin in relays and status in statuss:
        ret = True
        
    return ret

def servocheck(servo, status):
    '''this function check that we send right data for controling servo that control food door'''

    ret = False
    servop = "servo"
    statuss = ['open', 'close']
    if servo == servop and status in statuss:
        ret = True
        
    return ret

# check to see if this is the main thread of execution
if __name__ == '__main__':
    	
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	# start a thread that will perform motion detection
	t = threading.Thread(target=detect_motion, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()

	# start the flask app  
	app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()
