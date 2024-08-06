"""_summary_
이 모듈은 ntrexlab의 usb2can VCP제품을 파이썬으로 can모듈을 사용하기 위해서 작성된 인터페이스 모듈입니다.

Raises:
    TypeError: 채널정보(channel)가 없을 경우 에러가 발생(컴포트 정보) / 비정상적인 can baudrate가 입력될 경우 에러 발생
    CanInitializationError: 시리얼을 이용한 usb2can VCP의 초기화 실패 시
    CanOperationError: 작업 과정 중에 문제 발생
    CanTimeoutError: 시리얼 전송 타임아웃이 발생한 경우
    NotImplementedError: 플랫폼에서 사용이 불가능한 연결일 경우

Returns:
    _type_: MW_USB2CAN_VCP 객체
"""
import io
import logging
import time
from typing import Optional, Tuple

from can import (
    BusABC,
    CanInitializationError,
    CanOperationError,
    CanTimeoutError,
    Message,
)
import serial
import serial.serialutil

logger = logging.getLogger("can.MW_USB2CAN_VCP")

class MW_USB2CAN_VCP(BusABC):
    def _baudrate2canbaud(self, baudrate: int) -> str:
        logger.debug(f"_baudrate2canbaud baudrate : {baudrate}")
        match baudrate:
            case 10:
                return "b=10"
            case 20:
                return "b=20"
            case 25:
                return "b=25"
            case 40:
                return "b=40"
            case 50:
                return "b=50"
            case 80:
                return "b=80"
            case 100:
                return "b=100"
            case 125:
                return "b=125"
            case 150:
                return "b=150"
            case 200:
                return "b=200"
            case 250:
                return "b=250"
            case 400:
                return "b=400"
            case 500:
                return "b=500"
            case 750:
                return "b=750"
            case 800:
                return "b=800"
            case 1000:
                return "b=1000"
            case _:
                raise TypeError("Must specify a CAN baudrate.")

    def __init__(
        self,
        channel: str,
        baudrate: int = 500,
        *args,
        **kwargs,
    ) -> None:
        logger.debug("__init__")

        if not channel:
            raise TypeError("Must specify a serial port.")

        self.channel_info = f"MW_USB2CAN_VCP interface: {channel}"
        try:
            self._ser = serial.serial_for_url(
                channel, baudrate=921600, timeout=0.1, rtscts=False
            )
            self._ser.write(b"\n")
            rx_byte = self._ser.readall()
            self._ser.write(b"o=1\n")
            rx_byte = self._ser.readall()
            # 복구 방법을 auto로 설정하였을 때, 설정 정보를 응답으로 제공하므로 해당 응답이 정상인지 여부로 초기화 여부를 판단할 수 있음
            if b"O=1" not in rx_byte:
                raise ValueError("An invalid response was received.")
            logger.debug(rx_byte)
            canbaudrate = self._baudrate2canbaud(baudrate) + "\n"
            self._ser.write(bytearray(canbaudrate, "ascii"))
            rx_byte = self._ser.readall()
            logger.debug(rx_byte)
            self._ser.write(b"t=1\n")
            rx_byte = self._ser.readall()
            # 메세지 송수신 여부를 설정하였을 때, 설정 정보를 응답으로 제공하므로 해당 응답이 정상인지 여부로 초기화 여부를 판단할 수 있음
            if b"T=1" not in rx_byte:
                raise ValueError("An invalid response was received.")
            logger.debug(rx_byte)
            self._ser.write(b"e\n")
            rx_byte = self._ser.readall()
            # can 버스가 비정상 적일 경우 초기화를 제한한다.
            if b"E=0" not in rx_byte:
                raise ValueError("An invalid response was received.")
            logger.debug(rx_byte)
        except ValueError as error:
            raise CanInitializationError(
                "could not create the serial device"
            ) from error
        except serial.serialutil.SerialException as err:
            raise CanInitializationError(
                "could not create the serial device"
            ) from err

        super().__init__(channel, *args, **kwargs)

    def shutdown(self) -> None:
        """
        Close the serial interface.
        """
        logger.info("shutdown")
        super().shutdown()
        self._ser.close()

    def send(self, msg: Message, timeout: Optional[float] = None) -> None:
        # logger.debug("send")
        byte_msg = ""
        if not msg.is_extended_id:
            byte_msg += "S"
        else:
            byte_msg += "X"
        idx = hex(msg.arbitration_id).replace("0x", "")
        byte_msg += idx
        byte_msg += " "
        hex_string = msg.data.hex()
        byte_msg += hex_string
        byte_msg += "\n"

        data = bytearray(byte_msg.encode("ascii"))
        logger.debug(data)
        # Write to serial device
        try:
            self._ser.write(data)
            time.sleep(0.02)
        except serial.PortNotOpenError as error:
            raise CanOperationError("writing to closed port") from error
        except serial.SerialTimeoutException as error:
            raise CanTimeoutError() from error

    def _parse_message(self, message):
        # Remove STX ('S') and ETX ('\r\n')
        timestamp = time.time()
        message = message[0:-2]

        # Split arbitration_id and data
        parts = message.split(" ", 1)
        if len(parts) != 2:
            raise ValueError("Invalid message format")

        arbitration_id_str, data_str = parts
        arbitration_id = int(arbitration_id_str, 16)
        data = bytes.fromhex(data_str)
        ret = Message(
            arbitration_id=arbitration_id,
            data=data,
            timestamp=timestamp,
        )
        # logger.debug(ret)
        return ret

    def _recv_internal(
        self, timeout: Optional[float]
    ) -> Tuple[Optional[Message], bool]:
        # logger.debug("_recv_internal")
        try:
            rx_byte = self._ser.read()
            if rx_byte and rx_byte == b"S":
                message = self._ser.read_until(b"\r\n").decode("ascii")
        
                return self._parse_message(message), False
            else:
                return None, False

        except serial.SerialException as error:
            raise CanOperationError("could not read from serial") from error

    def fileno(self) -> int:
        logger.debug("fileno")
        try:
            return self._ser.fileno()
        except io.UnsupportedOperation:
            raise NotImplementedError(
                "fileno is not implemented using current CAN bus on this platform"
            ) from None
        except Exception as exception:
            raise CanOperationError("Cannot fetch fileno") from exception
