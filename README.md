# SoulKnightHelper

元气骑士联机小工具（支持安卓，iOS）

## 原理

联机小工具的原理是：房主会用 UDP 包广播房间信息，客户端收到包之后才能发现服务器。UDP 包内容大致如下，包含房间信息

```bash
	0x0000:  4500 00ab e7da 0000 3f11 7f63 0a00 0002  E.......?..c....
	0x0010:  0a00 0003 e5d0 5b25 0097 ea98 0000 09e7  ......[%........
	0x0020:  f800 0008 ae00 0000 0000 0000 0000 0000  ................
	0x0030:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0040:  0000 0000 0000 0000 0100 0000 0173 006f  .............s.o
	0x0050:  0075 006c 0020 006b 006e 0069 0067 0068  .u.l...k.n.i.g.h
	0x0060:  0074 002d 0046 0061 006c 0073 0065 002d  .t.-.F.a.l.s.e.-
	0x0070:  0056 0020 0032 002e 0035 002e 0031 002d  .V...2...5...1.-
	0x0080:  0030 0030 0032 0032 002d 0054 0072 0075  .0.0.2.2.-.T.r.u
	0x0090:  0065 002d 0031 0039 0036 0037 0039 0030  .e.-.1.9.6.7.9.0
	0x00a0:  0033 0033 0037 002d 0030 00              .3.3.7.-.0.
```

然而元气骑士并不会在 VPN 运行的 Interface 上进行广播，所以需要联机小工具监听广播包并将广播包转发到客户端，此后可以正常联机。

## iOS 上的联机小工具

- 在 App Store 里面下载名为 Python3IDE 的应用
- 粘贴如下代码，将里面的三个 IP 改为对应客户端 IP，如果不足三个可以留空
- 点击右上角运行即可

```python
import socket

PORT = 23333

def startRelayServer(players):
    hostRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostRecv.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST or socket.SO_REUSEADDR, 1)
    
    try:
        hostRecv.bind(("", PORT))
    except Exception as e:
        print("Port has been occupied, please run the script before hosting the game.")
        return
    
    players = [player for player in players if player != ""]
    socks = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for i in players]
    print("Relay server started, now host your game.")

    while True:
        for i in range(len(players)):
            hostData, hostAddr = hostRecv.recvfrom(1024)
            if len(hostData) > 0 and hostAddr[0] not in players:
                socks[i].sendto(hostData, (players[i], PORT))
                print(f"Broadcast package received, sending to {players[i]}.")

if __name__ == "__main__":
    players = ["10.8.0.3", "10.8.0.4", ""] # 不足三个则留空
    startRelayServer(players)
```

## 使用流程

- 连接 VPN
- 打开元气骑士到主页面，保证手机已经连接 WiFi（如果是流量则打开热点开关）
- 填入客户端的 IP，运行小工具，应当看到  `Relay server started, now host your game.`。如果出现 `Port has been occupied, please run the script before hosting the game.`，请先运行脚本再创建房间，如果仍不行，杀掉 Python3IDE 再进
- 创建游戏，进入英雄选择页面
- 切换到小工具，此时应当看到不断的有信息输出，这表示转发成功，此时客户端应该能够搜到该房间
- 切换到元气骑士，客户端已经可以加入

## Tips

使用 WireGuard 能获比 OpenVPN 更好的性能以及稳定性。 
