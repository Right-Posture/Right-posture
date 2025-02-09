import main
from main import *
from modules.app_functions import AppFunctions
import datetime

import os
import cv2
import traceback
import mediapipe as mp
import tensorflow as tf
import numpy as np
import sqlite3
import time
import math
from modules.app_temp import Debug_path, superuser, Setting_func


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


cwd = os.getcwd()
cwd = cwd+Debug_path.path
conn = sqlite3.connect(f"{cwd}/bin/Data/Sessions.db", check_same_thread=False)
# print('connect DB')
cur = conn.cursor()

#cur.execute("CREATE TABLE sessions (session_id INT PRIMARY KEY, user_id TEXT , time_start TEXT, time_end TEXT, incorrect_time FLOAT, correct_time FLOAT, total_time FLOAT, incorrect_per FLOAT, correct_per FLOAT)")


t_start = time.time()
t_last = time.time()
t_checkpoint = time.time()
t_correct_start = time.time()

t_incorrect_total = 0
t_total = 0

t_noti_checkpoint = time.time()

cor_count = 0
inc_count = 0
rest_flag = 0

start_time = time.asctime(time.localtime(time.time()))

cur.execute("SELECT * FROM sessions")
sess_items = cur.fetchall()

# print('item : ', sess_items[-1])

sess_id = int(sess_items[-1][0])+1
session = [(sess_id, '1', start_time, start_time, 0, 0, 0, 0, 0)]


model = None

# Switch model
# model_name = 'MN_Fix_angle_augmented_model3_3'
model_name = 'VGG19_Fix_angle_no_aug'


def Print_log(text):
    date_time = datetime.datetime.now()
    week_now = date_time.strftime("%a")
    time_now = date_time.strftime("%X")
    Camera_detail.log = f"{week_now} {time_now} {text}"
    Camera_detail.Update_log = True
    Camera_detail.setting = f"Pe {Camera_detail.period} \n Se {Camera_detail.sensitive} \n Si {Camera_detail.sitting}"

def Print_exception():
    traceback.print_exc()
    excType, value = sys.exc_info()[:2]
    Camera_detail.traceback = f"\nException error\n{excType}\n{value}\n{traceback.format_exc()}"

def predict_img(dir_img):
    img = tf.keras.preprocessing.image.load_img(dir_img, target_size=(224,224))
    X = tf.keras.preprocessing.image.img_to_array(img)

    
    X = np.expand_dims(X, axis=0)
    image = np.vstack([X])
    
    val = model(image)
    val = np.array(val)
    # val[0][0] : correct ////// val[0][1] : incorrect
    val[0][0] = '%.4f'%(float(val[0][0]*100))
    val[0][1] = '%.4f'%(float(val[0][1]*100))

    return val
        

def predict(img):
    cur.executemany("INSERT OR IGNORE INTO sessions VALUES (?,?,?,?,?,?,?,?,?)", session)
    conn.commit()
    
    X = tf.keras.preprocessing.image.img_to_array(img)

    
    X = np.expand_dims(X, axis=0)
    image = np.vstack([X])
    try:
        val = model(image)
        # correct > incorrect
        if float(val[0][0]) > float(val[0][1]):
            return 0
            # incorrect > correct
        elif float(val[0][0]) < float(val[0][1]):
            return 1
    except:
        Camera_detail.Error_load_model = True
        Camera_detail.model_status = "Critical error in model please restart and try again."
        Print_exception()
        print("Critical error in model please restart and try again.")

class VideoThread(QThread):
    # シグナル設定
    change_pixmap_signal = Signal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.threadpool = QThreadPool()

    # QThreadのrunメソッドを定義
    def run(self):
        global t_start, t_last, t_checkpoint, t_incorrect_total, t_total, cor_count, inc_count, t_noti_checkpoint, rest_flag, t_correct_start
        
        if Camera_detail.First_load_model:
            print("Start Load model")
            worker = Worker(self.execute_this_fn)  # Any other args, kwargs are passed to the run function
            # worker.signals.result.connect(self.print_output)
            # worker.signals.progress.connect(self.progress_fn)
            worker.signals.finished.connect(self.thread_complete)
            self.threadpool.start(worker)
        if Camera_detail.Finish_load_model:
            cap = cv2.VideoCapture(Setting_func.Camera, cv2.CAP_DSHOW)
            with mp_pose.Pose(
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as pose:
                while self._run_flag:
                    success, raw = cap.read()
                    # Check camera available
                    try:
                        resize = cv2.resize(raw, (384, 288))
                        image = cv2.flip(resize, 1)

                        image.flags.writeable = False
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        results = pose.process(image)

                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        # Draw the pose annotation on the image.
                        image.flags.writeable = True
                        mp_drawing.draw_landmarks(
                            image,
                            results.pose_landmarks,
                            mp_pose.POSE_CONNECTIONS,
                            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                        # prediction
                        image_resize = cv2.resize(image, (224, 224), interpolation = cv2.INTER_AREA)
                        pred = predict(image_resize)

                        if pred == 0:
                            cv2.putText(image, "Correct", (20, 20), 2, 0.5, (0, 255, 0), 1)
                            cor_count+=1
                            t_checkpoint = time.time()
                            if rest_flag == 1:
                                t_correct_start = time.time() + 1
                                rest_flag = 0
                        if pred == 1:
                            cv2.putText(image, "Incorrect", (20, 20), 2, 0.5, (0, 0, 255), 1)
                            inc_count+=1
                            t_last = (time.time()) - t_checkpoint

                            # preriod of notification
                            pon = Camera_detail.period
                            if time.time() - t_noti_checkpoint >= pon and rest_flag ==0:
                                # incorrect sensitive
                                sensitive = Camera_detail.sensitive
                                if int((t_last))%sensitive ==0:

                                    # ดัก send noti รัวๆ #
                                    AppFunctions.notifyIncorrect(self, 'พบการนั่งที่ผิดท่า!!!', 'กรุณาปรับเปลี่ยนท่านั่งของท่านให้ถูกต้อง')
                                    Print_log("Incorrect posture.")
                                    t_noti_checkpoint = time.time()

                        # timer of sitting 10 m  (10 m * 60s)

                        tos = Camera_detail.sitting
                        # >= 10 คือเอาไว้ดัก แจ้งเตือนรัวๆ และต้องค่าน้อยกว่า pon
                        if (time.time()) - t_noti_checkpoint >= 10 and rest_flag == 0:
                            if int(math.ceil((time.time()+2) - t_correct_start)) % (tos*60) == 0:
                                AppFunctions.notifyMe(self, f'คุณนั่งมาเป็นเวลา {tos} นาทีแล้ว', 'กรุณาลุกไปยืดเส้น ยืดสาย')
                                Print_log("Sitting too long.")
                                t_noti_checkpoint = time.time()
                                t_correct_start = time.time()+1
                                rest_flag = 1

                        # 新たなフレームを取得できたら
                        # シグナル発信(cv_imgオブジェクトを発信)
                        if success:
                            self.change_pixmap_signal.emit(image)

                    except Exception as e:
                        # print(e)
                        Camera_detail.Error_load_model = True
                        Camera_detail.traceback = "\nCamera not found please try to change in setting"

                if not Camera_detail.Error_load_model:
                    end_time = time.asctime(time.localtime(time.time()))

                    user = superuser.user
                    t_total = (time.time() - t_start)
                    t_incorrect_total = (inc_count/(inc_count+cor_count))*t_total
                    t_cor = (cor_count/(inc_count+cor_count))*t_total
                    inc_per = (inc_count/(inc_count+cor_count))*100
                    cor_per = (cor_count/(inc_count+cor_count))*100

                    t_total = '{:.2f}'.format(t_total)
                    t_incorrect_total = '{:.2f}'.format(t_incorrect_total)
                    t_cor = '{:.2f}'.format(t_cor)
                    inc_per = '{:.2f}'.format(inc_per)
                    cor_per = '{:.2f}'.format(cor_per)

                    print('t_incorrect       : {} sec'.format(t_incorrect_total))
                    print('t_cor             : {} sec'.format(t_cor))
                    print('t_total           : {} sec'.format(t_total))
                    print('inc_per           : {} %'.format(inc_per))
                    print('cor_per           : {} %'.format(cor_per))
                    if not user == "Guest":
                        cur.execute("UPDATE sessions SET time_end = ? , user_id = ? , incorrect_time = ? , correct_time = ? , total_time = ? , incorrect_per = ? , correct_per = ? WHERE session_id = ?", (end_time, user, t_incorrect_total, t_cor, t_total, inc_per, cor_per, sess_id,))
                    conn.commit()

                cap.release()
                cv2.destroyAllWindows()

            # videoCaptureのリリース処理

    # スレッドが終了するまでwaitをかける
    def stop(self):
        self._run_flag = False
        self.wait()

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self):
        global model
        dir_model = f"{cwd}/bin/Model/{model_name}"
        try:
            modeling = tf.keras.models.load_model(dir_model)
            model = modeling
        except:
            # Use to trick critical error check
            # Camera_detail.Finish_load_model = True

            Camera_detail.Error_load_model = True
            Camera_detail.model_status = f"Model not found in '{dir_model}'."
            Print_exception()
            print(f"Model not found in '{dir_model}'.")

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        if not Camera_detail.Error_load_model:
            Camera_detail.Finish_load_model = True
            Camera_detail.model_status = "Loaded"
            print("Finish load model")



class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class Camera_detail:
    log = ""
    traceback = ""
    get_model_name = model_name
    model_status = "Not loaded"
    First_load_model = True
    Finish_load_model = False
    Error_load_model = False
    Update_log = None
    # Setting sections
    period = 30
    sensitive = 7
    sitting = 1

class Camera:
    
    def detect(self, enable):
        if enable:
            self.image_label = QLabel(self)

            # vboxにQLabelをセット
            Camera_1 = self.ui.Camera_Frame_1_Layout
            Camera_1.addWidget(self.image_label)

            # vboxをレイアウトとして配置
            self.setLayout(Camera_1)

            # ビデオキャプチャ用のスレッドオブジェクトを生成
            self.thread = VideoThread()
            # ビデオスレッド内のchange_pixmap_signalオブジェクトのシグナルに対するslot
            self.thread.change_pixmap_signal.connect(self.update_image)

            self.thread.start()  # スレッドを起動

            # Delay to update detail
            if VideoThread != 0:
                QTimer.singleShot(1000, lambda: self.Update_detail())

        else:
            try:
                self.ui.Camera_Frame_1_Layout.removeWidget(self.image_label)
                self.image_label.deleteLater()
                self.thread.stop()
            except:
                pass