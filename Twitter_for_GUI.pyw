from logging import error
import sys
import os
import json
import webbrowser
import tweepy
from tweepy.error import TweepError
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font  as tkfont
from tkinter import messagebox
from tkinter import *

from dotenv import load_dotenv

load_dotenv()

class Lang:
    
    def text(self,text_type):      
        text = (os.environ[f'{text_type}'])
        return text

def lang(text_type):
    test = Lang()
    text = test.text(text_type=text_type)
    return text

mode_lang="JA"



try:
    for env in os.environ:
        if str(env + ' : ' + os.environ.get(env)).startswith("USERPROFILE") == True:
            config_path = ((os.environ.get(env))+"\\twitter_gui\\key_config.json")
            config_path = (config_path.replace("\\","/"))
            config_dir = (os.environ.get(env))+"\\twitter_gui\\"
            config_dir = (config_dir.replace("\\","/"))
except:
    print("パスの取得に失敗しました。")
    sys.exit()

def user_path(filename):
    try:
        for env in os.environ:
            if str(env + ' : ' + os.environ.get(env)).startswith("USERPROFILE") == True:
                config_path = ((os.environ.get(env))+f"\\twitter_gui\\{filename}")
                config_path = (config_path.replace("\\","/"))
                config_dir = (os.environ.get(env))+"\\twitter_gui\\"
                config_dir = (config_dir.replace("\\","/"))
                return config_path
    except:
        print("パスの取得に失敗しました。")
        sys.exit()

try:
    json_open = open(config_path, 'r')
    json_load = json.load(json_open)
    ck = json_load['api_key']
    cs = json_load['api_key_secret']
    at = json_load['access_token']
    ats = json_load['access_token_secret']
    default_image_path = json_load['default_image_path']
    mode_lang=json_load['lang']
    if len(mode_lang)<0:
        mode_lang="JA"
    json_open.close
except:
    pass


INFO_TWEETED=os.environ[f'INFO_TWEETED_{mode_lang}']
INFO_TWEET_FAIL=os.environ[f'INFO_TWEET_FAIL_{mode_lang}']
INFO_FAVORITED=os.environ[f'INFO_FAVORITED_{mode_lang}']
INFO_FAVORITE_DESTROYED=os.environ[f'INFO_FAVORITE_DESTROYED_{mode_lang}']
INFO_RETWEETED=os.environ[f'INFO_RETWEETED_{mode_lang}']
INFO_ASK_RETWEET_DESTROY=os.environ[f'INFO_ASK_RETWEET_DESTROY_{mode_lang}']
INFO_RETWEET_DESTROYED=os.environ[f'INFO_RETWEET_DESTROYED_{mode_lang}']

TWEET=os.environ[f'TWEET_{mode_lang}']
SEND_TWEET=os.environ[f'SEND_TWEET_{mode_lang}']

CREATE_FAVORITE=os.environ[f'CREATE_FAVORITE_{mode_lang}']
CREATE_RETWEET=os.environ[f'CREATE_RETWEET_{mode_lang}']

HOME=os.environ[f'HOME_{mode_lang}']
USER_TIMELINE=os.environ[f'USER_TIMELINE_{mode_lang}']

SETTING=os.environ[f'SETTING_{mode_lang}']
HELP=os.environ[f'HELP_{mode_lang}']
RELOAD=os.environ[f'RELOAD_{mode_lang}']

TWEET_CONTENT=os.environ[f'TWEET_CONTENT_{mode_lang}']
FILE_NAME=os.environ[f'FILE_NAME_{mode_lang}']

TL=os.environ[f'TL_{mode_lang}']

TITLE_HOME=os.environ[f'TITLE_HOME_{mode_lang}']
TITLE_USER_TIMELINE=os.environ[f'TITLE_USER_TIMELINE_{mode_lang}']
TITLE_KEY_SETTING=os.environ[f'TITLE_KEY_SETTING_{mode_lang}']

IMAGE_FOLDER_PATH=os.environ[f'IMAGE_FOLDER_PATH_{mode_lang}']

LOGIN_SUCCESSED=os.environ[f'LOGIN_SUCCESSED_{mode_lang}']
LOGIN_FAILED=os.environ[f'LOGIN_FAILED_{mode_lang}']

LOGIN=os.environ[f'LOGIN_{mode_lang}']
CANCEL=os.environ[f'CANCEL_{mode_lang}']

WINDOW_HELP=os.environ[f'WINDOW_HELP_{mode_lang}']

HOW_TO_LOGIN=os.environ[f'HOW_TO_LOGIN_{mode_lang}']
HOW_TO_TWEET=os.environ[f'HOW_TO_TWEET_{mode_lang}']

HOW_TO_LOGIN_DESCRIPTION=os.environ[f'HOW_TO_LOGIN_DESCRIPTION_{mode_lang}']
HOW_TO_TWEET_DESCRIPTION=os.environ[f'HOW_TO_TWEET_DESCRIPTION_{mode_lang}']

OPEN_IN_GITHUB=os.environ[f'OPEN_IN_GITHUB_{mode_lang}']

TITLE_GITHUB=os.environ[f'TITLE_GITHUB_{mode_lang}']

def connect():
    try:
        json_open = open(config_path, 'r')
        json_load = json.load(json_open)
        ck = json_load['api_key']
        cs = json_load['api_key_secret']
        at = json_load['access_token']
        ats = json_load['access_token_secret']
        default_image_path = json_load['default_image_path']
        mode_lang=json_load['lang']
        json_open.close
        auth = tweepy.OAuthHandler(ck, cs)
        auth.set_access_token(at, ats)
        api = tweepy.API(auth)
        me = api.me()

        return api

    except tweepy.TweepError:
        try:
            os.mkdir(config_dir)
        except:
            pass

        key_setting_window(1)

        sys.exit()

class main_gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (home, user_timeline, KeySetting):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("home")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def close_frame(self):
        self.destroy()

def tweet_gui(self,controller,base_x=30):
    
    def send_tweet():
        tweet_content=gui_tweet_box.get()
        tweet_id=gui_id_box.get()
        if (len(tweet_content)>0):
            print(tweet_content)
            print(tweet_id)
            try:
                api.update_status(status = tweet_content, in_reply_to_status_id = tweet_id,auto_populate_reply_metadata=True)
                label_info["text"] = INFO_TWEETED
            except:
                print(INFO_TWEET_FAIL)
                label_info["text"] = INFO_TWEET_FAIL

    def send_favorite():
        tweet_id=gui_id_box.get()
        if (len(tweet_id)>0):
            print(tweet_id)
            try:
                api.create_favorite(tweet_id)
                label_info["text"] = INFO_FAVORITED

            except:
                api.destroy_favorite(tweet_id)
                label_info["text"] = INFO_FAVORITE_DESTROYED

    def send_retweet():
        tweet_id=gui_id_box.get()
        if (len(tweet_id)>0):
            print(tweet_id)
            try:
                api.retweet(tweet_id)
                label_info["text"] = INFO_RETWEETED
            except:
                ret = messagebox.askyesno('INFO', INFO_ASK_RETWEET_DESTROY)
                #ret = messagebox.askyesno('INFO', 'リツイートを取り消ししますか？')

                if (ret==True):

                    status = api.get_status(tweet_id, include_my_retweet=1)

                    if status.retweeted == True:
                        api.destroy_status(status.current_user_retweet['id'])
                        label_info["text"] = INFO_RETWEET_DESTROYED
                        #messagebox.showinfo("INFO", "リツイートを取り消ししました。")      
        
    def close():
        api = connect()
        controller.close_frame()
        print(me.name)
        app = main_gui()
        app.mainloop()

    self.controller = controller
    
    gui_label = tk.Label(self, text=TWEET)
    gui_label.place(x=base_x,y=20)
    gui_send_button = tk.Button(self,text = SEND_TWEET,command=send_tweet)
    gui_send_button.place(x=base_x, y=220)
    gui_fav_button = tk.Button(self,text = CREATE_FAVORITE,command=send_favorite)
    gui_fav_button.place(x=base_x+45, y=220)
    gui_RT_button = tk.Button(self,text = CREATE_RETWEET,command=send_retweet)
    gui_RT_button.place(x=base_x+95, y=220)
    gui_home_bottun = tk.Button(self,text = HOME,command=lambda: [controller.show_frame("home"),controller.title(f"{HOME}")])
    gui_home_bottun.place(x=base_x, y=260)
    gui_at_mention_button = tk.Button(self,text = f'{USER_TIMELINE} ',command=lambda: [controller.show_frame("user_timeline"),controller.title(USER_TIMELINE)])
    gui_at_mention_button.place(x=base_x+45, y=260)
    gui_at_setting_button = tk.Button(self,text = f'{SETTING} ',command=lambda: [controller.show_frame("KeySetting"),controller.title(f"{SETTING}")])
    gui_at_setting_button.place(x=base_x, y=300)
    gui_at_setting_help_button = tk.Button(self,text = f'{HELP}',command=setting_help)
    gui_at_setting_help_button.place(x=base_x+45, y=300)
    gui_at_reload_button = tk.Button(self,text = f'   {RELOAD}   ',command=close)
    gui_at_reload_button.place(x=base_x+95, y=300)

    gui_tweet_label = tk.Label(self,text=f'{TWEET_CONTENT}')
    gui_tweet_label.place(x=base_x, y=45)
    gui_id_label = tk.Label(self,text='id')
    gui_id_label.place(x=base_x, y=105)
    gui_image_name_label = tk.Label(self,text=f'{FILE_NAME}')
    gui_image_name_label.place(x=base_x, y=165)

    gui_tweet_box = tk.Entry(self,width=40)
    gui_tweet_box.place(x=base_x, y=70)
    gui_id_box = tk.Entry(self,width=40)
    gui_id_box.place(x=base_x, y=130)
    gui_image_box = tk.Entry(self,width=40)
    gui_image_box.place(x=base_x, y=190)

    label_info=Label(self,text="")
    label_info.place(x=base_x,y=330)

def setting(controller,title,width=630,height=450):
    controller.geometry(f"{width}x{height}")
    controller.title(title)
    

def set_scroll_bar(self,controller):

    self.controller = controller

    gui_tl_label = tk.Label(self,text=f'{TL}')
    gui_tl_label.place(x=300, y=20)

    #start scroll bar and frame
    canvas = tk.Canvas(self, bg="white")
    canvas.place(x=300, y=50, width=300, height=350)
    canvas = Canvas(canvas, height=200) # a canvas in the canvas object
    frame = Frame(canvas) # a frame in the canvas
    scrollbar = Scrollbar(canvas, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y") # comment out this line to hide the scrollbar
    canvas.pack(side="left", fill="both", expand=True) # pack the canvas
    # make the frame a window in the canvas
    canvas.create_window((4,4), window=frame, anchor="nw", tags="frame")
    # bind the frame to the scrollbar
    frame.bind("<Configure>", lambda x: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Down>", lambda x: canvas.yview_scroll(3, "units")) # bind "Down" to scroll down
    canvas.bind("<Up>", lambda x: canvas.yview_scroll(-3, "units")) # bind "Up" to scroll up
    # bind the mousewheel to scroll up/down
    canvas.bind("<MouseWheel>", lambda x: canvas.yview_scroll(int(-1*(x.delta/40)), "units"))
    #end

    return frame

#button1 = tk.Button(self, text="Go to the start page",
#        command=lambda: controller.show_frame("home"))
#button2 = tk.Button(self, text="Go to the start page",
#        command=lambda: controller.show_frame("KeySetting"))

def get_tl(mode,frame):
    api=connect()
    if mode==0:
        for status in api.home_timeline():
            user_name_readonly = tk.Label(frame,text=status.user.name+"  "+status.user.screen_name)
            text_readonly = tk.Label(frame,text=status.text)
            id_readonly = tk.Entry(frame)
            id_readonly.insert(0, status.id)
            id_readonly.config(state="readonly")
            url_readonly = tk.Entry(frame)
            url_readonly.insert(0, "https://twitter.com/"+status.user.screen_name+"/status/"+str(status.id))
            url_readonly.config(state="readonly")
            inner_line=Label(frame,text="-"*100)
            inner_line.pack(anchor=tk.W)
            user_name_readonly.pack(anchor=tk.W)
            text_readonly.pack(anchor=tk.W)
            id_readonly.pack(anchor=tk.W) #.pack(anchor=tk.W)
            url_readonly.pack(anchor=tk.W)
    elif mode==1:
        for status in api.user_timeline():
            user_name_readonly = tk.Label(frame,text=status.user.name+"  "+status.user.screen_name)
            text_readonly = tk.Label(frame,text=status.text)
            id_readonly = tk.Entry(frame)
            id_readonly.insert(0, status.id)
            id_readonly.config(state="readonly")
            url_readonly = tk.Entry(frame)
            url_readonly.insert(0, "https://twitter.com/"+status.user.screen_name+"/status/"+str(status.id))
            url_readonly.config(state="readonly")
            inner_line=Label(frame,text="-"*100)
            inner_line.pack(anchor=tk.W)
            user_name_readonly.pack(anchor=tk.W)
            text_readonly.pack(anchor=tk.W)
            id_readonly.pack(anchor=tk.W) #.pack(anchor=tk.W)
            url_readonly.pack(anchor=tk.W)

def restart(controller):

    controller.close_frame()

    print(me.name)

    api = connect()

    app = main_gui()
    app.mainloop()

class home(tk.Frame):
    def __init__(self, parent, controller):
        setting(controller=controller,title=f"{TITLE_HOME}")
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # ボタンの作成と配置

        frame = set_scroll_bar(self,controller)

        api=connect()

        me=api.me()

        tweet_gui(self,controller)

        get_tl(0,frame)
        

class user_timeline(tk.Frame):

    def __init__(self, parent, controller):
        #setting(controller=controller,title=f"{TITLE_USER_TIMELINE}")
        tk.Frame.__init__(self, parent)
        self.controller = controller

        frame = set_scroll_bar(self,controller)

        api=connect()

        me=api.me()

        tweet_gui(self,controller)

        get_tl(1,frame)

            
class KeySetting(tk.Frame):

    def __init__(self, parent, controller):
        #setting(controller=controller,title=f"{TITLE_KEY_SETTING}")
        tk.Frame.__init__(self, parent)
        self.controller = controller

        api=connect()

        me=api.me()

        frame = set_scroll_bar(self,controller)
        
        label_sub = tk.Label(self, text=f"{TITLE_KEY_SETTING}")
        label_sub.place(x=30,y=20)

        # ラベル
        gui_api_key_label = tk.Label(self,text='API Key')
        gui_api_key_label.place(x=30, y=45)

        gui_api_key_secret_label = tk.Label(self,text='API Key Secret')
        gui_api_key_secret_label.place(x=30, y=105)

        gui_access_token_label = tk.Label(self,text='Access token')
        gui_access_token_label.place(x=30, y=165)

        gui_access_token_secret_label = tk.Label(self,text='Access token secret')
        gui_access_token_secret_label.place(x=30, y=225)

        gui_image_path_label = tk.Label(self,text=f'{IMAGE_FOLDER_PATH}')
        gui_image_path_label.place(x=30, y=285)

        gui_lang_label = tk.Label(self,text=f'言語')
        gui_lang_label.place(x=30, y=350)

        # テキストボックス
        gui_api_key_Entry = tk.Entry(self,width=40)
        gui_api_key_Entry.place(x=30, y=70)

        gui_api_key_secret_Entry = tk.Entry(self,width=40)
        gui_api_key_secret_Entry.place(x=30, y=130)

        gui_access_token_Entry = tk.Entry(self,width=40)
        gui_access_token_Entry.place(x=30, y=190)

        gui_access_token_secret_Entry = tk.Entry(self,width=40)
        gui_access_token_secret_Entry.place(x=30, y=250)

        gui_image_path_Entry = tk.Entry(self,width=40)
        gui_image_path_Entry.place(x=30, y=310)

        gui_Lang_Entry = tk.Entry(self,width=40)
        gui_Lang_Entry.place(x=30, y=370)


        gui_api_key_Entry.insert(0, ck)
        gui_api_key_secret_Entry.insert(0, cs)
        gui_access_token_Entry.insert(0, at)
        gui_access_token_secret_Entry.insert(0, ats)
        gui_image_path_Entry.insert(0,default_image_path)
        gui_Lang_Entry.insert(0,mode_lang)

        def val():
            # テキストボックスの値を取得
            if(len(gui_api_key_Entry.get())>0 and len(gui_api_key_Entry.get())>0 and len(gui_access_token_secret_Entry.get())>0 and len(gui_access_token_Entry.get())>0 and len(gui_access_token_secret_Entry.get())>0):


                api_key=gui_api_key_Entry.get()
                api_key_secret=gui_api_key_secret_Entry.get()
                access_token=gui_access_token_Entry.get()
                access_token_secret=gui_access_token_secret_Entry.get()
                image_path=gui_image_path_Entry.get()
                lang_Entry=gui_Lang_Entry.get()

                if len(gui_Lang_Entry.get())>0:
                    data6="JA"

                data=list([api_key,api_key_secret,access_token,access_token_secret,image_path,lang_Entry])

                key_data = {
                    'api_key': api_key, 
                    'api_key_secret': api_key_secret,
                    'access_token': access_token,
                    'access_token_secret':access_token_secret,
                    'default_image_path':image_path,
                    'lang':lang_Entry
                }

                with open(config_path, 'w') as f:
                    json.dump(key_data, f, indent=2, ensure_ascii=False)

                try:
                    json_open = open(config_path, 'r')
                    json_load = json.load(json_open)
                    api_key = json_load['api_key']
                    api_key_secret = json_load['api_key_secret']
                    access_token = json_load['access_token']
                    api_key_secret = json_load['access_token_secret']
                    default_image_path = json_load['default_image_path']
                    mode_lang=json_load['lang']
                    if len(mode_lang)<0:
                        mode_lang="JA"
                        json_open.close
                except:
                    pass

                try:
                    auth = tweepy.OAuthHandler(api_key, api_key_secret)
                    auth.set_access_token(access_token, access_token_secret)
                    api = tweepy.API(auth)
                    try:
                        me=api.me()
                    except Exception as e:
                        print(e)
                    
                    #print(f"認証が完了しました。")
                    print(f"{LOGIN_SUCCESSED}")
                    messagebox.showinfo("INFO", f"{LOGIN_SUCCESSED}")
                    
                    data=list([api_key,api_key_secret,access_token,access_token_secret,image_path,lang_Entry])
                    print(data)

                    with open(config_path, 'w') as f:
                        json.dump(key_data, f, indent=2, ensure_ascii=False)
                    
                    controller.close_frame()

                    app = main_gui()

                    app.mainloop()

                    return data
                    
                except Exception as e:
                    #print("認証できませんでした。")
                    print(f"{LOGIN_FAILED}")
                    print(e)
                    messagebox.showinfo("INFO", f"{LOGIN_FAILED}")
                    
                    data=list([api_key,api_key_secret,access_token,access_token_secret,image_path,lang_Entry])

                    with open(config_path, 'w') as f:
                        json.dump(key_data, f, indent=2, ensure_ascii=False)
                    print(data)
                    return data

        button = tk.Button(self,text = f'{LOGIN}',command = val)
        button.place(x=30, y=400)

        button = tk.Button(self,text = f'{CANCEL}',command = lambda:[controller.show_frame("home"),controller.title(f"`{TITLE_HOME}")])
        button.place(x=75, y=400)
        
    
def key_setting_window(mode=0):

    if(mode==0):
        key_setting_window_gui = tk.Toplevel()
    elif(mode==1):
        key_setting_window_gui = tk.Tk()
    else:
        key_setting_window_gui = tk.Tk()

    key_setting_window_gui.geometry("360x450")
    key_setting_window_gui.title(f"{SETTING}")
    label_sub = tk.Label(key_setting_window_gui, text=f"{SETTING}")
    label_sub.pack()

    # ラベル
    gui_api_key_label = tk.Label(key_setting_window_gui,text='API Key')
    gui_api_key_label.place(x=30, y=45)
    gui_api_key_secret_label = tk.Label(key_setting_window_gui,text='API Key Secret')
    gui_api_key_secret_label.place(x=30, y=105)
    gui_access_token_label = tk.Label(key_setting_window_gui,text='Access token')
    gui_access_token_label.place(x=30, y=165)
    gui_access_token_secret_label = tk.Label(key_setting_window_gui,text='Access token secret')
    gui_access_token_secret_label.place(x=30, y=225)
    gui_image_path_label = tk.Label(key_setting_window_gui,text=f'{IMAGE_FOLDER_PATH}')
    gui_image_path_label.place(x=30, y=285)
    gui_lang_label = tk.Label(key_setting_window_gui,text=f'言語')
    gui_lang_label.place(x=30, y=350)
    # テキストボックス
    gui_api_key_Entry = tk.Entry(key_setting_window_gui,width=40)
    gui_api_key_Entry.place(x=30, y=70)
    gui_api_key_secret_Entry = tk.Entry(key_setting_window_gui,width=40)
    gui_api_key_secret_Entry.place(x=30, y=130)
    gui_access_token_Entry = tk.Entry(key_setting_window_gui,width=40)
    gui_access_token_Entry.place(x=30, y=190)
    gui_access_token_secret_Entry = tk.Entry(key_setting_window_gui,width=40)
    gui_access_token_secret_Entry.place(x=30, y=250)
    gui_image_path_Entry = tk.Entry(key_setting_window_gui,width=40)
    gui_image_path_Entry.place(x=30, y=310)
    gui_Lang_Entry = tk.Entry(key_setting_window_gui,width=40)
    gui_Lang_Entry.place(x=30, y=370)
    
    def val():
        # テキストボックスの値を取得
        if(len(gui_api_key_Entry.get())>0):

            api_key=gui_api_key_Entry.get()
            api_key_secret=gui_api_key_secret_Entry.get()
            access_token=gui_access_token_Entry.get()
            access_token_secret=gui_access_token_secret_Entry.get()
            image_path=gui_image_path_Entry.get()
            mode_lang=gui_Lang_Entry.get()

            data=list([api_key,api_key_secret,access_token,access_token_secret,image_path])            

            key_data = {
                'api_key': api_key, 
                'api_key_secret': api_key_secret,
                'access_token': access_token,
                'access_token_secret':access_token_secret,
                'default_image_path':image_path,
                'lang':mode_lang,
            }

            with open(config_path, 'w') as f:
                json.dump(key_data, f, indent=2, ensure_ascii=False)


            try:
                auth = tweepy.OAuthHandler(api_key, api_key_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)
                me=api.me()
                print(f"{LOGIN_SUCCESSED}")
                messagebox.showinfo("INFO", f"{LOGIN_SUCCESSED}")
            except Exception as e:
                print(f"{LOGIN_FAILED}")
                print(e)
                messagebox.showinfo("INFO", f"{LOGIN_FAILED}")

            print(data)


    def close():
        key_setting_window_gui.destroy()

    # ボタンの作成と配置
    button = tk.Button(key_setting_window_gui,text = f'{LOGIN}',command = val)
    button.place(x=30, y=400)

    button = tk.Button(key_setting_window_gui,text = f'{CANCEL}',command = close)
    button.place(x=75, y=400)

    key_setting_window_gui.mainloop()

        
def setting_help():

    setting_help_gui = tk.Toplevel()
    setting_help_gui.geometry("365x250")
    setting_help_gui.title(f"{WINDOW_HELP}")

    gui_help_label = tk.Label(setting_help_gui, text=f"{WINDOW_HELP}")
    gui_help_label.pack()

    # ラベル

    gui_how_to_login_label = tk.Label(setting_help_gui,text=f'{HOW_TO_LOGIN}')
    gui_how_to_login_label.place(x=30, y=15)

    gui_how_to_login_description_label = tk.Label(setting_help_gui,text='設定→キー設定でAPIのキーをセットし、\nOKボタンを押してください。')
    gui_how_to_login_description_label.place(x=30, y=35)

    gui_how_to_tweet_label = tk.Label(setting_help_gui,text=f'{HOW_TO_TWEET}')
    gui_how_to_tweet_label.place(x=30, y=95)

    gui_how_to_tweet_description_label = tk.Label(setting_help_gui,text='キーをセットしたらソフトを再起動し、\nツイートボタンを押してください。')
    gui_how_to_tweet_description_label.place(x=30, y=115)

    def val():
        setting_help_gui.destroy()

    def val2():
        close_brain_askyesno = messagebox.askyesno('INFO', '脳みそを閉じますか？')
        if close_brain_askyesno==True:
            sys.exit()
        else:
            messagebox.showinfo("INFO", "いや、何でもない。")
        
        setting_help_gui.destroy()

    
    github_url="https://github.com/hashibutogarasu/Twitter-for-GUI"

    github_label=tk.Label(setting_help_gui,text="github")
    github_label.place(x=30,y=170)

    github_Entry=tk.Entry(setting_help_gui)
    github_Entry.insert(0,github_url)
    github_Entry.config(state="readonly",width=45)
    github_Entry.place(x=30,y=190)


    button = tk.Button(setting_help_gui,text = '把握した',command = val)
    button.place(x=30, y=220)

    button1 = tk.Button(setting_help_gui,text = 'わけわかめ',command = val2)
    button1.place(x=90, y=220)


    setting_help_gui.mainloop()

def help_github():

    github_url="https://github.com/hashibutogarasu/Twitter-for-GUI"

    help_github_gui = tk.Toplevel()
    help_github_gui.geometry("400x250")
    help_github_gui.title(f"{TITLE_GITHUB}")

    gui_github_label = tk.Label(help_github_gui, text=f"{TITLE_GITHUB}")
    gui_github_label.pack()

    # ラベル
    gui_url_label = tk.Label(help_github_gui,text=f'{github_url}')
    gui_url_label.place(x=30, y=17)

    def val():
        webbrowser.open(github_url)
        help_github_gui.destroy()

    gui_open_in_browser_button = tk.Button(help_github_gui,text = f'{OPEN_IN_GITHUB}',command = val)
    gui_open_in_browser_button.place(x=30, y=40)

    help_github_gui.mainloop()

if __name__  == '__main__':
    
    try:
        os.mkdir(config_dir)
    except:
        pass

    try:
        api=connect()
        me=api.me()
        try:
            app = main_gui()
            app.mainloop()
        except:
            pass
    except Exception as e:
        key_data = {'api_key': "", 'api_key_secret': "", 'access_token': "",'access_token_secret':"",'default_image_path':"","lang":"JA"}

        with open(config_path, 'w') as f:
            json.dump(key_data, f, indent=2, ensure_ascii=False)

        messagebox.showinfo("INFO", f"{config_path}にファイルを生成しました。次回、ソフトを再起動することで設定ができるようになります。")

        print(e)