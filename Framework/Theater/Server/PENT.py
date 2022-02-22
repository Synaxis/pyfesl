from Config import ConsoleColor
from Utils import PacketEncoder
import UGAM

def ReceiveComponent(self, data):
    PENTPacket = PacketEncoder.SetVar('TID', self.PacketID)
    PENTPacket = PacketEncoder.encode('PENT', PENTPacket, 0x0, 0)
    self.transport.getHandle().sendall(PENTPacket)

    if data.find('PENT') != -1:
        data = data.split('PENT')[1]
        PENT.ReceiveComponent(self, data)