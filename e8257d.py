import socket, sys, time

class e8257d(object):

    def __init__(self,IP,port=5025):		#SGの固定IPアドレスを取得してここに入れる
        self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.com.settimeout(1)
        self.IP = IP
        self.port = port
        self.open()

    def open(self):
        try:
            self.com.connect((self.IP,self.port))
            recv = self.query(cmd = "*IDN?\n")
            print("接続完了: " + recv)
        except:
            sys.exit()
            print("接続エラー")
        return

    def close(self):
        try:
            self.com.close()
            return True
        except:
            sys.exit()
            return False

    def query(self,cmd):
        self.send(cmd)
        time.sleep(0.01)	#コマンドをOSが送って受け取るまでの時間
        recv = self.recv()
        return recv

    def send(self,cmd):		#コマンドをSGに送る
        try: self.com.send(cmd.encode())
        except: sys.exit()
        return True

    def recv(self,byte=1024):	#SGから帰ってきた信号を受け取る
        try: recv = self.com.recv(byte).decode()
        except: sys.exit()
        return recv
    # def recv(self, byte=1024):
    #     try:
    #         recv = self.com.recv(byte).decode()
    #         return recv
    #     except socket.timeout:  # タイムアウト例外をキャッチ
    #         print("タイムアウトが発生しました。")  # タイムアウトが発生したことを出力
    #         return None  # None を返して処理を継続する
    #     except Exception as e:
    #         print("エラーが発生しました:", e)  # 他の例外が発生した場合もエラーメッセージを出力
    #         return None  # None を返して処理を継続する

    def get_ID(self):   # 相手の情報を確認
        cmd = "*IDN?\n"
        id = self.query(cmd)
        return id

    def check_RF_on_off(self):  #RF信号のON, OFFを確認
        cmd = 'OUTP?\n'
        recv = self.query(cmd)
        if recv == '0\n':
            state = "RF: OFF"
        elif recv == '1\n':
            state = "RF: ON"
        else:
            state = "NG: check_RF_on_off()" 
        return state

    def set_RF_on(self):
        cmd = "OUTP ON\n"
        recv = self.send(cmd)
        if recv == True:
            state = self.check_RF_on_off()
            if state == "RF: ON":
                state = "RF信号がONに設定されました"
            else:
                state = "RF信号をONに設定できませんでした。\n通信エラーの可能性があります"
        else:
            # state = "set_RF_on_off(): Command transmission error."
            pass
        return state

    def set_RF_off(self):
        cmd = "OUTP OFF\n"
        recv = self.send(cmd)
        if recv == True:
            state = self.check_RF_on_off()
            if state == "RF: OFF":
                state = "RF信号がOFFに設定されました"
            else:
                state = "RF信号をOFFに設定できませんでした。\n通信エラーの可能性があります"
        else:
            # state = "set_RF_on_off(): Command transmission error."
            pass
        return state

    def check_freq(self):
        unit_list = ['GHz', 'MHz', 'KHz']
        cmd = 'Freq?\n'
        rec = float(self.query(cmd).strip())   # 周波数の確認
        if rec >= 10**9 and rec <= 20*10**9:
            rec = rec/10**9
            word = '現在の周波数: ' + str(rec) + '[' + unit_list[0] + ']'
        elif rec <10**9 and rec >=10**6:
            rec = rec/10**6
            word = '現在の周波数: ' + str(rec) + '[' + unit_list[1] + ']'
        elif rec <10**6 and rec >=250*10**3:
            rec = rec/10**3
            word = '現在の周波数: ' + str(rec) + '[' + unit_list[2] + ']'
        else:
            print('周波数エラー\n250kHz〜20GHzで設定してください')
        return word

    # 周波数設定
    def set_freq(self, freq, unit):
        cmd = 'FREQ {:.2f} {}\n'.format(freq, unit)
        self.send(cmd)
        recv = self.check_freq()
        return recv

    # 出力強度[dBm]の確認
    def check_power(self):
        cmd = 'POW?\n'
        rec = float(self.query(cmd).strip("\n"))
        word = '現在の出力強度は ' + str(rec) + "[dBm]です。"
        return word
        # return rec
    
    # 強度設定
    def set_power(self, power, unit):
        cmd = 'POW {:.2f} {}\n'.format(power, unit)
        self.send(cmd)
        rec = self.check_power()
        return rec