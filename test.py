import can
from ntrexlab_usb2can_vcp import MW_USB2CAN_VCP
import logging
logging.basicConfig(level=logging.DEBUG)

bus = can.Bus(interface="mw_usb2can_vcp", channel="COM11", bitrate=500000)
bus.shutdown()