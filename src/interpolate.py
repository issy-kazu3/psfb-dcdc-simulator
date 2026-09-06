import numpy as np

def cal_trans(exc_cur,trans_2nd_LI,n1):     #exc_curは１次側の励磁電流 n1は１次側のターン数
#    cur_2nd=np.abs(n1*exc_cur)
    exc_cur=np.abs(exc_cur)*n1
    if exc_cur>trans_2nd_LI["2ndary current A"].max():  #この書式はデータフレームでしかなりたたない。
#    if cur_2nd>trans_2nd_LI[0].max():  #numpy配列ではこう扱う
        #return None    #この方式はやめた
        raise ValueError(
            f"trans current {exc_cur} A exceeds the LI data range"  #ここの{}は文字列に変数を埋め込むための記号だよ。辞書ではない
        )
    L_trans=np.interp(                      #cur_2ndという２次電流の絶対値を算出して、最初に２次のインダクタンスを求める
        exc_cur,
        trans_2nd_LI["2ndary current A"],
        trans_2nd_LI["L2 uH"]
        )

    L_trans=n1*n1*L_trans      #1次側のインダクタンスに換算
    L_trans=L_trans/1000000 #uH->Hに変更

    return L_trans

def cal_choke(cur,choke_LI):
    cur=np.abs(cur)
    if cur>choke_LI["A"].max():
        #return None    #この方式はやめた
        raise ValueError(
            f"choke current {cur} A exceeds the LI data range"  #ここの{}は文字列に変数を埋め込むための記号だよ。辞書ではない
            f"({choke_LI['A'].max()} A)"
        )
    
    L_choke=np.interp(
        cur,
        choke_LI["A"],
        choke_LI["uH"]
    )
    L_choke=L_choke/1000000 #uH->Hに変更
    return L_choke


