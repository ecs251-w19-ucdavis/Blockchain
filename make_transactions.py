#!/usr/bin/python 
from console import *
from Transaction import *
import Queue
if __name__ == "__main__":
    console(8002).transfer('8001', 600, 20)
    # console(8002).transfer('8001', 300, 20)
    console(8002).transfer('8003', 300, 22)
    # console(8001).transfer('8002', 400, 21)
    console(8002).transfer('8004', 800, 13)
    # console(8003).transfer('8002', 430, 14)
    # console(8004).transfer('8002', 430, 1)