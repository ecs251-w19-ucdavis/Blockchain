from console import *
from Transaction import *
import Queue
if __name__ == "__main__":
    console(8001).register()
    console(8002).register()
    console(8003).register()
    console(8004).register()
    console(8001).transfer('8002', 200, 10)
    console(8002).transfer('8001', 100, 20)
    console(8003).transfer('8002', 150, 22)
    console(8001).transfer('8002', 400, 21)
    console(8002).transfer('8003', 450, 13)
    console(8003).transfer('8002', 430, 14)
    console(8004).transfer('8002', 430, 1)