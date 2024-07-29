import io
import logging
import struct
import time
from typing import Any, List, Optional, Tuple

from can import (
    BusABC,
    CanInitializationError,
    CanInterfaceNotImplementedError,
    CanOperationError,
    CanProtocol,
    CanTimeoutError,
    Message,
)
from can.typechecking import AutoDetectedConfig
import serial

logger = logging.getLogger("can.VCP")


class MW_USB2CAN_VCP(BusABC):
  def _baudrate2canbaud(self, baudrate: int) -> str:
    match baudrate:
      case 10000:
        return "10"
      case 20000:
        return "20"
      case 25000:
        return "25"
      case 40000:
        return "40"
      case 50000:
        return "50"
      case 80000:
        return "80"
      case 100000:
        return "100"
      case 125000:
        return "125"
      case 150000:
        return "150"
      case 200000:
        return "200"
      case 250000:
        return "250"
      case 400000:
        return "400"
      case 500000:
        return "500"
      case 750000:
        return "750"
      case 800000:
        return "800"
      case 1000000:
        return "1000"
    
  def __init__(
    self,
    channel: str,
    baudrate: int = 500,
    timeout: float = 0.1,
    rtscts: bool = False,
    *args,
    **kwargs,
  ) -> None:
    logger.debug("__init__")

    if not channel:
        raise TypeError("Must specify a serial port.")

    self.channel_info = f"MW_USB2CAN_VCP interface: {channel}"
    # self._can_protocol = CanProtocol.CAN_20

    try:
        self._ser = serial.serial_for_url(
            channel, baudrate=921600, timeout=timeout, rtscts=rtscts
        )
        self._ser.write(b"\n")
        rx_byte = self._ser.readall()
        logger.debug(rx_byte)        
        self._ser.write(b"A=1\n")
        rx_byte = self._ser.readall()
        logger.debug(rx_byte)
        self._ser.write(b"B=500\n")
        rx_byte = self._ser.readall()
        logger.debug(rx_byte)    
        self._ser.write(b"T=1\n")
        rx_byte = self._ser.readall()
        logger.debug(rx_byte)                         
        # self._ser.write(b"h\n")
        # rx_byte = self._ser.readall()
        # logger.debug(rx_byte)
    except ValueError as error:
        raise CanInitializationError(
            "could not create the serial device"
        ) from error

    super().__init__(channel, *args, **kwargs)