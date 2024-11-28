import pyxel
import json
import socket

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.h = 10
        self.w = 10

    def move(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 1
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y += 1

    def shot(self):
        pass

    def dump(self):
        # 相手に渡すように作る
        return json.dumps({"x":self.x, "y":self.y}).encode("utf-8")
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.h, self.w, 1)

class Enemy:
    def __init__(self):
        self.x = 190
        self.y = 200
        self.h = 10
        self.w = 10

    def update(self, info):
        # infoを参照してインスタンス変数を更新
        # 自分からみたPlayerと渡した後のplayerの値は反転するはずなので注意s
        info = json.loads(info)
        print(info)
        #self.x = info["x"]
        self.y = info["y"]
    
    def shot(self):
        pass

    def draw(self):
        pyxel.rect(self.x, self.y, self.h, self.w, 1)

class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self):
        pass
    
    def dump(self):
        pass


class App:
    def __init__(self, is_host: bool):
        pyxel.init(200,200)
        self.is_host = is_host
        self.host = "localhost"
        self.port = 3000
        self.player = Player()
        self.enemy = Enemy()
        self.player_shot = []
        self.enemy_shot = []
        self.__connection()
        pyxel.run(self.update, self.draw)
    
    def __connection(self):
        if self.is_host:
            print("wait for connection...")
            self.wait_for_connection()
            print("connection established")
        else:
            print("finding host...")
            self.find_host()
            print("host found")

    def wait_for_connection(self):
        # ソケットを作って待機
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        while True:
            self.client, self.addr = self.sock.accept()
            break

    def find_host(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        # ゲーム開始
        pass
    
    def recv(self):
        buff = self.client.recv(1024)
        return buff

    def send(self):
        data = self.player.dump()
        self.client.send(data)
    
    def update(self):
        self.player.move()
        self.send()
        enemy_info = self.recv()
        if enemy_info:
            self.enemy.update(enemy_info)

    def draw(self):
        pyxel.cls(7)
        if self.is_host:
            pyxel.text(100,100, "Host", 9)
        else:
            pyxel.text(100,100, "Guest", 9)
        self.player.draw()
        self.enemy.draw()

if __name__ == "__main__":
    App(is_host=False)
