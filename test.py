import can
from ntrexlab_usb2can_vcp import MW_USB2CAN_VCP
import logging
logging.basicConfig(level=logging.DEBUG)

bus = can.Bus(interface="mw_usb2can_vcp", channel="COM11", bitrate=250000)
can_id = 0x600 + 10
data = b"\x40\x00\x10\x00\x00\x00\x00\x00"
remote = False
msg = can.Message(is_extended_id=can_id > 0x7FF,
                          arbitration_id=can_id,
                          data=data,
                          is_remote_frame=remote)
bus.send(msg)
msg, tt = bus._recv_internal(5)
print (msg, tt)
bus.shutdown()