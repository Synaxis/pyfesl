from Utilities.Packet import Packet


def ReceivePacket(self, data):
    toSend = Packet().create()

    allowed = data.get("PacketData", "ALLOWED")

    if str(allowed) == "1":
        self.CONNOBJ.joiningPlayers += 1

    toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
    Packet(toSend).send(self, "EGRS", 0x00000000, 0)
