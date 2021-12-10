import tkinter as tk
import tkinter.font as font
from tkinter import filedialog
import os
import natsort

class MainWindow(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        self.font_bt = font.Font(family="HY엽서M", size=14)

        self.movie_only = tk.BooleanVar(value=True)
        self.sub_only = tk.BooleanVar(value=True)

        self.current_dir = "/"

        self.Init()
        self.InitComponent()

        self.dir_path = None
        self.file_list = None

        self.sub_list = (".smi", ".srt", ".ssa", ".ass", ".lrc",
                         ".SMI", ".SRT", ".SSA", ".ASS", ".LRC")
        self.movie_list = (".webm", ".mkv", ".flv", ".vob", ".ogv", ".ogg", ".drc", ".gif", ".gifv", ".mng",
                      ".avi", ".MTS", ".M2TS", ".TS", ".mov", ".qt", ".wmv", ".yuv", ".rm", ".rmvb",
                      ".asf", ".amv", ".mp4", ".m4p", ".m4v", "flv",
                           ".WEBM", ".MKV", ".FLV", ".VOB", ".OGV", ".OGG", ".DRC", ".GIF", ".GIFV", ".MNG",
                           ".AVI", ".MTS", ".M2TS", ".TS", ".MOV", ".QT", ".WMV", ".YUV", ".RM", ".RMVB",
                           ".ASF", ".AMV", ".MP4", ".M4P", ".FLV")




    #프레임 관련 초기화 함수
    def Init(self):
        self.w = 900
        self.h = 400

        x = (self.root.winfo_screenwidth() // 2) - (self.w // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.h // 2)

        self.root.title("Filename Modifier")
        self.root.geometry("%dx%d+%d+%d" % (self.w, self.h, x, y))
        self.root.resizable(False, False)

    #Component 관련 초기화 함수
    def InitComponent(self):
        self.frame_left = tk.Frame(self.root, bg="#bdd7f0", width=self.w*0.8, relief="solid", borderwidth=1)
        self.frame_left.pack(side="left", fill="both", expand="true")

        self.scrollbar_y = tk.Scrollbar(self.frame_left, orient=tk.VERTICAL)
        self.scrollbar_y.pack(side="right", fill="y")
        self.text_filelist = tk.Text(self.frame_left, width=100, height=30, wrap="none", yscrollcommand=self.scrollbar_y.set)
        self.text_filelist.pack()
        self.scrollbar_y.config(command=self.text_filelist.yview)

        self.frame_right = tk.Frame(self.root, bg="#bdd7f0", width=self.w*0.2, relief="solid", borderwidth=1)
        self.frame_right.pack(side="right", fill="both", expand="true")

        #0번째 행 -> 폴더선택
        self.bt_folder = tk.Button(self.frame_right, text="폴더선택", font=self.font_bt, command=self.SelectFolder)
        self.bt_folder.grid(row=0, column=0, padx=20, pady=10, columnspan=2)

        #1번째 행 -> 제목 설정
        self.txt_name = tk.Text(self.frame_right, height=2, width=20)
        self.txt_name.grid(row=1, column=0, padx=20, pady=10, columnspan=2)

        #2번째 행 -> season설정
        self.lb_season = tk.Label(self.frame_right, text="시즌", font=self.font_bt, bg="#bdd7f0")
        self.lb_season.grid(row=2, column=0, pady=10)

        #DropDownMenu를 만들기 위한 부분
        list_font = font.Font(family="맑은 고딕", size=15, weight="bold")
        self.var = tk.StringVar(self.root)
        option_list = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "99"]
        self.var.set(option_list[1])
        option = tk.OptionMenu(self.frame_right, self.var, *option_list)
        option.config(font = list_font, width = 3, bg = "#80b0f0")
        option["highlightthickness"] = 0
        option["activebackground"] = "#40a0e0"
        option.grid(row=2, column=1, pady=10)
        menu = self.nametowidget(option.menuname)
        menu.config(font = list_font)

        #3번째 행 -> 자막 존재 체크
        # self.cVar = tk.IntVar()
        # self.check_sub = tkinter.Checkbutton(self.frame_right, text="자막여부", font=self.font_bt, variable=self.cVar, activebackground="#cdd7ff")
        # self.check_sub.grid(row=3, column=0, pady=10, columnspan=2)

        #4번째 행 -> 변환
        self.bt_modify = tk.Button(self.frame_right, text="변환", font=self.font_bt, bg="#bdd7f0", command=self.Modify)
        self.bt_modify.grid(row=4, column=0, pady=10, columnspan=2)

        #5, 6번째 행 -> 체크박스
        self.chk_movie_only = tk.Checkbutton(self.frame_right, text="영상파일만보기", bg="#bdd7f0", \
            variable=self.movie_only, command=self.ShowFileList)
        self.chk_movie_only.grid(row=5, column=0, pady=10, columnspan=2)

        self.chk_sub_only = tk.Checkbutton(self.frame_right, text="자막파일만보기", bg="#bdd7f0", \
            variable=self.sub_only, command=self.ShowFileList)
        self.chk_sub_only.grid(row=6, column=0, pady=10, columnspan=2)

        #맨밑에 -> 종료
        self.bt_exit = tk.Button(self.frame_right, text="종료", font=self.font_bt, bg="#bda7d0", command=self.Exit)
        self.bt_exit.grid(row=7, column=1, pady=50, columnspan=2)

    #작업할 폴더 선택
    def SelectFolder(self):
        try:
            self.dir_path = filedialog.askdirectory(parent=self.root, initialdir=self.current_dir, title='Please select a directory')

            #Set Current Directory -> Change selected directory's parent dir
            parent_dir = self.dir_path.split("/")[:-1]
            self.current_dir = ""
            for dir in parent_dir:
                self.current_dir += dir + "/"
                
            self.ShowFileList()
        except Exception as e:
            print(e)
            return

    #파일 리스트 새로고침
    def ShowFileList(self):
        self.file_list = os.listdir(self.dir_path)          #폴더에서 파일 리스트를 가지고옴
        self.file_list = natsort.natsorted(self.file_list)  #파일 순서를 정렬

        try:
            self.text_filelist.delete("1.0", "end")
        except:
            pass

        #Get Boolean Type Value from checkbox value
        only_movie = self.movie_only.get()
        only_sub = self.sub_only.get()

        show_file_list = []

        if only_movie or only_sub:
            for file in self.file_list:
                if only_movie and file.endswith(self.movie_list):
                    show_file_list.append(file)
                if only_sub and file.endswith(self.sub_list):
                    show_file_list.append(file)
        else:
            show_file_list = self.file_list

        for file in show_file_list:
            self.text_filelist.insert("end", file + "\n")


    #파일 이름 수정
    def Modify(self):
        name = self.txt_name.get("1.0", "end")  #text로부터 텍스트를 받아옴
        name = name[:-1]
        selected_season = self.var.get()


        movie_index = 1
        sub_index = 1

        try:
            for file in self.file_list:
                filename, fileExtension = os.path.splitext(file)
                src = os.path.join(self.dir_path, file)
                if fileExtension in self.sub_list:   #자막 파일일 경우
                    dst = name + "-" + "S" + selected_season + "E" + str(sub_index).zfill(2) + fileExtension.lower()
                    sub_index += 1
                elif fileExtension in self.movie_list:   #영상 파일일 경우
                    dst = name + "-" + "S" + selected_season + "E" + str(movie_index).zfill(2) + fileExtension.lower()
                    movie_index += 1
                else:
                    continue
                dst = os.path.join(self.dir_path, dst)
                os.rename(src, dst)
            
            tk.messagebox.showinfo("성공", f"{movie_index-1}개의 영상파일과\n{sub_index-1}개의 자막파일을 \n수정하였습니다")
            self.ShowFileList()
        except Exception as e:
            tk.messagebox.showwarning("실패", f"무언가의 이유로 작업이 실패하였습니다.\nError : {e}")

    #프로그램 종료
    def Exit(self):
        self.root.quit()