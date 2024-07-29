import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')
setup(
    name="python_ntrexlab_usb2can_vcp",
    version="{{VERSION_PLACEHOLDER}}",
    author="changu",
    author_email="ckdo8008@gmail.com",
    description="이 모듈은 ntrexlab의 usb2can VCP제품을 파이썬으로 can모듈을 사용하기 위해서 작성된 인터페이스 모듈입니다.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    py_modules = ["python_ntrexlab_usb2can_vcp"],
    python_requires=">=3.10",
    install_requires=[
        "python-can",
        "pyserial",
    ],
    entry_points = {
        'can.interface': [
            'mw_usb2can_vcp = ntrexlab_usb2can_vcp:MW_USB2CAN_VCP'
        ]
    }
)