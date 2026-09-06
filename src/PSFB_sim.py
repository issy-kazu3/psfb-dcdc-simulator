import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #グラフをdialogに埋め込むためのｍの
from matplotlib.gridspec import GridSpec
import tkinter as tk        #ダイアログボックスでの入力パラメータ入力のため
from tkinter import ttk     #表を作るためのもの
from tkinter import filedialog
from PIL import Image,ImageTk

import numpy as np
import pandas as pd
from interpolate import cal_trans
from interpolate import cal_choke
from load_trans_2nd_LI import load_trans_2nd_LI
from load_choke_LI import load_choke_LI
from load_condition import load_condition


def create_result_plot(parent,df_results):  #グラフの作成
    #fig,ax1=plt.subplots(figsize=(10,6))    #グラフの縦横比はここ
    fig=plt.figure(figsize=(10,5))    #グラフの縦横比はここ

    gs=GridSpec(2,1,figure=fig,height_ratios=[5,2])     #２分割で、5:２の高さ比になる
    ax1=fig.add_subplot(gs[0])
    ax2=fig.add_subplot(gs[1],sharex=ax1)

    ax1.tick_params(axis="x",bottom=False,labelbottom=False)
    ax2.grid(axis="x")
    #ax2.tick_params(axis="y",left=False,labelleft=False)

    time=df_results["time"]

    #------------------
    #左軸：current A
    #------------------
    ax1.plot(
        time,
        df_results["magnetizing current"],
        label="Imag",
        color="blue",
        linestyle="--"
    )
    ax1.plot(
        time,
        df_results["I1 A"],
        label="I1",
        color="orange",
        linestyle="-"
    )

    ax1.plot(
        time,
        df_results["I2 A"],
        label="I2",
        color="purple",
        linestyle="--"
    )

    ax2.set_xlabel("time [sec]")
    ax1.set_ylabel("current [A]")
    ax1.grid(True)
    
    #ax2=ax1.twinx()
    #ax2=fig.add_subplot(2,1,2,sharex=ax1)
    #ax2.set_yticks([0,1])
    #ax2.set_yticklabels(["OFF/ON"])

# -------------------------
# ax2 : Gate signal
# -------------------------
    q_position={
        "Q1":4,
        "Q2":3,
        "Q3":2,
        "Q4":1
    }

    for q,pos in q_position.items():
        y=np.where(
            df_results[q]==1,
            pos,
            np.nan
        )
        ax2.plot(
            df_results["time"],
            y,
            label=q,
            linewidth=1
        )

    #ax2グラフのy軸表示
    ax2.set_ylim(0.5,4.5)
    ax2.set_yticks([4,3,2,1])
    ax2.set_yticklabels(["Q1","Q2","Q3","Q4"])



    #for q in ["Q1", "Q2", "Q3", "Q4"]:
    #    ax2.step(
    #    df_results["time"],
    #    df_results[q],
    #    where="post",
    #    label=q
    #)               


    #凡例をまとめる
    lines1,labels1=ax1.get_legend_handles_labels()

    ax1.legend(
        lines1,
        labels1,
        loc="upper left",
        fontsize=14,
        bbox_to_anchor=(1.06, 1.0)
    )
    fig.subplots_adjust(right=0.78)

    ax1.set_ylim(-20*(-df_results["I1 A"].min()//20+1),20*(df_results["I2 A"].max()//20+1))

    fig.tight_layout()

    #Tkinterに埋め込む
    canvas=FigureCanvasTkAgg(
        fig,
        master=parent
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill=tk.BOTH,
        expand=True
    )

    return fig,canvas   #figがグラフで、canvasがダイアログの生地部分か



def create_result_table(parent,df_conclusion):
    frame=ttk.LabelFrame(
        parent,
        text="Simulation result"
    )

    frame.pack(
        fill=tk.X,
        padx=10,
        pady=10
    )

    items=[
        ("turn 1",f"{df_conclusion['turn 1'].iloc[0]}"),
        ("turn 2",f"{df_conclusion['turn 2'].iloc[0]}"),
        ("V1",f"{df_conclusion['V1 V'].iloc[0]:.1f} V"),
        ("V2",f"{df_conclusion['V2 V'].iloc[0]:.1f} V"),
        ("I2",f"{df_conclusion['I2 A'].iloc[0]:.1f} A"),
        ("fs",f"{df_conclusion['fs kHz'].iloc[0]:.1f} kHz"),
        ("duty",f"{df_conclusion['duty'].iloc[0]:.2f}"),
        ("I1max",f"{df_conclusion['I1max A'].iloc[0]:.2f} A"),
        ("I1min",f"{df_conclusion['I1min A'].iloc[0]:.2f} A"),
        ("I2max",f"{df_conclusion['I2max A'].iloc[0]:.2f} A"),
        ("I2min",f"{df_conclusion['I2min A'].iloc[0]:.2f} A"),
        ("Imag_max",f"{df_conclusion['Imag_max A'].iloc[0]:.2f} A"),
        ("Imag_min",f"{df_conclusion['Imag_min A'].iloc[0]:.2f} A")
    ]

    for i,(name,value) in enumerate(items):
        row=i//7        #0->0//3=0 4->4//3=1
        col=(i%7)*2     #0%3*2=0 1%3*2=2 2%3*2=4 3%3*2=0

        if i < 7:
            result_color="black"
        else:
            result_color="blue"

        tk.Label(
            frame,
            text=name,
            fg=result_color,
            font=("Arial",12)
        ).grid(
            row=row,
            column=col,
            padx=10,
            pady=5,
            sticky="w"
        )

        tk.Label(
            frame,
            text=value,
            fg=result_color,
            font=("Arial",12)
        ).grid(
            row=row,
            column=col+1,
            padx=10,
            pady=5,
            sticky="w"
        )
    return frame


def show_result(df_results,df_conclusion):
    root=tk.Tk()
    root.title("PSFB DCDC simulation result")
    root.geometry("1100x700")

    #-----------------
    #タイトル
    #-----------------
    title=ttk.Label(
        root,
        text="PSFB DCDC simulator result",
        font=("Arial",14,"bold")
    )

    title.pack(
        pady=2
    )

    #-----------------
        #グラフ領域
    #-----------------
    graph_frame=ttk.Frame(root)
    
    graph_frame.pack(
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=5
    )
    
    create_result_plot(
        graph_frame,
        df_results
    )
        
    #--------------
    #結果表
    #--------------
    create_result_table(
        root,
        df_conclusion
    )

    root.wait_window()



#--------グラフ表示関連ここまで-----------------------

#csv_path=r"D:\Userarea\J0125789\Documents\Python_code\PSFB\apply_dialog"
csv_path=r"C:\Users\kazi3\Documents\my_program\Github\PSFB\apply_dialog"
file_drive=r"drive_condition.csv"
file_trans=r"trans_2nd_LI.csv"
file_choke=r"choke_LI.csv"

def select_file(title_text,entry):
    file_path=filedialog.askopenfilename(
        title=title_text,#"Trans LI(1 turn) csv file select",
        filetypes=[
            ("CSV files","*.csv"),
            ("All files","*.*")
        ]
    )
    if file_path:
        entry.delete(0,tk.END)         #テキストボックスのエントリーのなかを頭0～最後tk.ENDまで消去
        entry.insert(0,file_path)      #テキストボックスに選んだファイル名をパスを含めて挿入

def get_conditions(dic_config,input_trans,input_choke):     #ここではからなず引数に使う辞書dic_configを入れねばならない

    confirmed=False #confirmedはここで作った関数ローカルの変数 Falseだと、そのままwindowが閉じられたことを呼び出し側に知らせる

    def start_simulation():

        nonlocal confirmed  #ローカル変数でない。上の変数を使うという宣言
        nonlocal input_trans    #注意！　単独の変数は、スコープは関数の中だけ。ここでは、input_transとinput_chokeをstart_simulationの外に渡したいので、nonlocalとしている。ただし、辞書(単独変数以外は基本的に)はオブジェクト渡しなので、ここでの変更は外部でも反映される
        nonlocal input_choke

        dic_config["n1"]=int(entry_turn1.get())
        dic_config["n2"]=dic_config["n2"]
        dic_config["v1"]=float(entry_v1.get())
        dic_config["v2"]=float(entry_v2.get())
        dic_config["i2"]=float(entry_i2set.get())
        dic_config["fs"]=float(entry_fs.get())*1000
        dic_config["duty"]=dic_config["v2"]/dic_config["v1"]*dic_config["n1"]/dic_config["n2"]
        dic_config["tcyc"]=1/dic_config["fs"]
        dic_config["ton"]=dic_config["tcyc"]/2*dic_config["duty"]
        dic_config["toff"]=dic_config["tcyc"]/2-dic_config["ton"]

        input_trans=entry_trans_file.get()
        input_choke=entry_choke_file.get()

        confirmed=True  #正しく終了した場合には、False->Trueに変更する！
        root.destroy()

    def cancel():    #windowがそのまま閉じられた場合の関数
        root.destroy()    #そのままwindowを消滅させている。confirmedはFalseのまま


    root=tk.Tk()                #親ウィンドウの生成 Tk()
    root.title("Simulation condition")

    #xボタンを押したときもcancel()を実行
    root.protocol("WM_DELETE_WINDOW",cancel)  #mainloop()の前に指定しておく　windowが消されたらcancel()

    #-----------------
    # PSFB回路図
    #-----------------
    image=Image.open(csv_path+"\\psfb_dcdc.png")
    #画像サイスの変更
    image=image.resize((400,200))
    photo=ImageTk.PhotoImage(image)
    label_image=tk.Label(root,image=photo)
    label_image.image=photo #画像が消えないように保持
    #label_image.pack(pady=10)   #これはだめだった。gridとpackは併用できず?
    label_image.grid(
        row=0,
        column=0,
        rowspan=8,  #画像に割り当てるサイズ
        padx=(210,10),
        pady=(120,10)
    )

    #-------------transの設定ファイル---------------------------------------
    entry_trans_file=tk.Entry(root,width=80)      #テキストボックス
    entry_trans_file.grid(row=0,column=0,padx=10,pady=10)
    entry_trans_file.insert(0,input_trans)

    button_trans_file=tk.Button(
        root,
        text=("Trans_LI"),
        command=lambda:select_file("Trans LI(1 turn) csv file select",entry_trans_file)  #ボタン処理時の関数をlambdaで登録してcommandに入れる処理らしい
    )
    button_trans_file.grid(row=0,column=1,padx=10,pady=10)
    #-------------transの設定ファイルここまで---------------------------------------

    #-----------chokeの設定ファイル--------------
    entry_choke_file=tk.Entry(root,width=80)      #テキストボックス
    entry_choke_file.grid(row=1,column=0,padx=10,pady=10)
    entry_choke_file.insert(0,input_choke)

    button_choke_file=tk.Button(
        root,
        text=("Choke_LI"),
        command=lambda:select_file("Choke LI csv file select",entry_choke_file)  #ボタン処理時の関数をlambdaで登録してcommandに入れる処理らしい
    )
    button_choke_file.grid(row=1,column=1,padx=10,pady=10)
    #-----------chokeの設定ファイルここまで--------------

    tk.Label(root,text="turn n1").grid(row=2,column=0,sticky="w",padx=(10,0))
    entry_turn1=tk.Entry(root,justify="center")            #tk.Entryはテキストボックス
    entry_turn1.insert(0,str(int(dic_config["n1"])))
    entry_turn1.grid(row=2,column=0,sticky="w",padx=(80,0))
    tk.Label(root,text="turn n2").grid(row=3,column=0,sticky="w",padx=(10,0))
    tk.Label(root,text=str(dic_config["n2"])).grid(row=3,column=0,sticky="w",padx=(135,0))
    tk.Label(root,text="V1 V").grid(row=4,column=0,sticky="w",padx=(10,0))
    entry_v1=tk.Entry(root,justify="center")
    entry_v1.insert(0,str(float(dic_config["v1"])))
    entry_v1.grid(row=4,column=0,sticky="w",padx=(80,0))
    tk.Label(root,text="V2 V").grid(row=5,column=0,sticky="w",padx=(10,0))
    entry_v2=tk.Entry(root,justify="center")
    entry_v2.insert(0,str(float(dic_config["v2"])))
    entry_v2.grid(row=5,column=0,sticky="w",padx=(80,0))
    tk.Label(root,text="I2 A").grid(row=6,column=0,sticky="w",padx=(10,0))
    entry_i2set=tk.Entry(root,justify="center")
    entry_i2set.insert(0,str(float(dic_config["i2"])))
    entry_i2set.grid(row=6,column=0,sticky="w",padx=(80,0))
    tk.Label(root,text="fs kHz").grid(row=7,column=0,sticky="w",padx=(10,0))
    entry_fs=tk.Entry(root,justify="center")
    entry_fs.insert(0,str(float(dic_config["fs"]/1000)))
    entry_fs.grid(row=7,column=0,sticky="w",padx=(80,0))

    tk.Button(
        root,
        text=" start ",
        command=start_simulation
    ).grid(row=11,column=0,columnspan=2,pady=(20,5))

    root.mainloop()     #rootが最初のダイアログ　それを表示するコマンド

    if not confirmed:   #キャンセルの場合
        return None,input_trans,input_choke

    return dic_config,input_trans,input_choke





input_file=csv_path+"\\"+file_drive
dic_config=load_condition(input_file)

input_trans=csv_path+"\\"+file_trans
trans_2nd_LI=load_trans_2nd_LI(input_trans) #trans_2nd_LIはnumpy配列

input_choke=csv_path+"\\"+file_choke
choke_LI=load_choke_LI(input_choke) #choke_LIはnumpy配列

dic_config,input_trans,input_choke=get_conditions(dic_config,input_trans,input_choke)
if dic_config==None:
    dic_config=load_condition(input_file)

print(dic_config)



n1=dic_config["n1"]
n2=dic_config["n2"]
v1=dic_config["v1"]
v2=dic_config["v2"]
i2set=dic_config["i2"]
fs=dic_config["fs"]
duty=dic_config["duty"]
tcyc=dic_config["tcyc"]
ton=dic_config["ton"]
toff=dic_config["toff"]


n_time=800  #800分割で計算実施
n_cyc=2     #2ｻｲｸﾙ計算実施
deltat=tcyc/(n_time/n_cyc)  #離散時間のΔt  1サイクルは400分割　要するに2ｻｲｸﾙ計算して表示する

#-------事前の計算--------------
#定常状態でのimの初期のﾏｲﾅｽｵﾌｾｯﾄを算出
im=0    #im:励磁電流
for i in range(n_time): #iは0～n_time-1まで
    if i*deltat>=ton/2:
        break
    L=cal_trans(im,trans_2nd_LI,n1)
    im=im+v1/L*deltat       #v1=L・dim/dt -> dim=v1/L・dt   ※dt=deltat
im=im*-1
#ここまで、定常状態でのimの初期のﾏｲﾅｽｵﾌｾｯﾄを算出
#I2の初期値を算出
i2=i2set
for i in range(n_time): #iは0～n_time-1まで
    if i*deltat>=ton/2:
        break
    L=cal_choke(i2,choke_LI)
    i2=i2-(v1*n2/n1-v2)/L*deltat       #v1*n2/n1-v2=-L・di2/dt -> di2=(v1*n2/n1-v2)/L・dt   ※dt=deltat
i1=im+i2*n2/n1
q1=1
q2=0
q3=0
q4=1
#-------事前の計算はここまで-------------------------
results=[]
conclusion=[]
i=0

#--------逐次計算-------------------------
for j in range(n_cyc):
    state=1
    for i in range(int(n_time/n_cyc)):
        results.append(
            {
                "time":i*deltat+j*tcyc,
                "magnetizing current":im,
                "I1 A":i1,
                "I2 A":i2,
                "Q1":q1,
                "Q2":q2,
                "Q3":q3,
                "Q4":q4
            }
        )
        match state:
            case 1:
                L = cal_trans(im,trans_2nd_LI,n1)
                im = im + v1 / L * deltat
                L = cal_choke(i2,choke_LI)
                i2 = i2 + (v1 *n2/n1 - v2) / L * deltat
                i1 = im + i2 *n2/n1
                q1=1
                q2=0
                q3=0
                q4=1
            case 2:
                L = cal_trans(im,trans_2nd_LI,n1)
                im = im
                L = cal_choke(i2,choke_LI)
                i2 = i2 - v2 / L * deltat
                i1 = im
                q1=0
                q2=1
                q3=0
                q4=1
            case 3:
                L = cal_trans(im,trans_2nd_LI,n1)
                im = im - v1 / L * deltat
                L = cal_choke(i2,choke_LI)
                i2 = i2 + (v1 *n2/n1- v2) / L * deltat
                i1 = im - i2 *n2/n1
                q1=0
                q2=1
                q3=1
                q4=0
            case 4:
                L = cal_trans(im,trans_2nd_LI,n1)
                im = im
                L = cal_choke(i2,choke_LI)
                i2 = i2 - v2 / L * deltat
                i1 = im
                q1=1
                q2=0
                q3=1
                q4=0
        if i * deltat < ton:
            state=1
        elif i * deltat < ton+toff:
            state=2
        elif i* deltat < ton+toff+ton:
            state=3
        else:
            state=4

            
df_results=pd.DataFrame(results)        #resultsという辞書が入ったリストを、見出し付きのcsvのような書式(dataframe)に変更
df_results.to_csv(csv_path+"\\psfb_sim_result.csv",index=False)      #このdfをcsvに出力 indexという行番号見出しは不要としている

conclusion.append(
    {
        "turn 1":n1,
        "turn 2":n2,
        "V1 V":v1,
        "V2 V":v2,
        "I2 A":i2set,
        "fs kHz":fs/1000,
        "duty":duty,
        "I1max A":df_results["I1 A"].max(),
        "I1min A":df_results["I1 A"].min(),
        "I2max A":df_results["I2 A"].max(),
        "I2min A":df_results["I2 A"].min(),
        "Imag_max A":df_results["magnetizing current"].max(),
        "Imag_min A":df_results["magnetizing current"].min()
    }
)

#df_conclusion=pd.DataFrame(conclusion)
#df_conclusion.to_csv(csv_path+"\\PSFB_sim_conclusion.csv",index=False)   
#コメントアウトした出力を縦書きに変更
df_conclusion=pd.DataFrame(conclusion)
df_conclusionT=df_conclusion.T   #縦横転置
df_conclusionT.columns=["Value"]
df_conclusionT.to_csv(
    csv_path+"\\PSFB_sim_conclusion.csv",
    #index=False,
    index_label="Item"
    )   

show_result(df_results,df_conclusion)



