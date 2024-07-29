# ntrexlab usb2can vcp 파이썬 CAN 인터페이스
이 모듈은 ntrexlab의 usb2can VCP제품을 파이썬으로 can모듈을 사용하기 위해서 작성된 인터페이스 모듈입니다.
ntrexlab에서는 자체툴만 제공해서 임의로 제작되었습니다. 필요에 의해서 작성한 모듈이기 때문에 업데이트가 느릴 수 있습니다.

## ntrexlab usb2can VCP

> MW USB2CAN(VCP) 소개
>> MW USB2CAN(VCP)는 한 개 포트의 CAN 프로토콜을 USB의 VCP(Virtual COM Port) 프로토콜로 변환하는 장치입니다. FT232 칩을 사용하여 USB와 MCU간 비동기 시리얼 데이터를 주고받는 형태로 데이터 전송률은 최대 300K byte/second입니다

<strong>FIFO 제품은 갖고 있는게 없어서 구현하지 않습니다.</strong>

### MW USB2CAN(VCP) 특징
* 속도가 느림
* CAN Bus의 속도는 1M까지 가능하지만 변경과정에서 병목현상이 발생함
  * 예외로 Send 후 딜레이처리 필요(변환 과정)
* CAN bus의 모니터링이 가능함
* 초기화 과정에서 통신 설정 필요
* 전문 송수신에 STX와 ETX가 필요

### MW USB2CAN(VCP) 초기화 구현
메세지 송수신여부, 복구방식, 통신속도를 지정하였습니다.

## 요구사항
Python 3.10 이상을 사용하여야 합니다. (match-case 사용, match-case를 if-elif 문으로 변경하여 사용이 가능합니다.)
pyserial
python-can

## 설치
```
pip install python_ntrexlab_usb2can_vcp
```

## 사용
```
import can
from ntrexlab_usb2can_vcp import MW_USB2CAN_VCP

bus = can.Bus(interface="mw_usb2can_vcp", channel="COM11", bitrate=500000)
```

## 그 밖에
* 해외 판매는 안하는 것 같아서 한글로만 작성합니다.
* USB2CAN 제품 중에 저렴한 제품이 적어서 모듈을 직접 작성했습니다. 마스터 용으로는 사용해도 좋지만 슬레이브로는 사용을 지양합니다.(변환 과정 및 지연 시간으로 누락이 발생됩니다.)
