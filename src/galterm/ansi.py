from typing import Literal

def ansi(n):return f"\033[{n}m"

RESET           = ansi(0)
BOLD            = ansi(1)
DIM             = ansi(2)
ITALIC          = ansi(3)
UNDERLINE       = ansi(4)
REVERSE         = ansi(7)
STRIKE          = ansi(9)
NORMAL          = ansi(22)
NO_ITALIC       = ansi(23)
NO_UNDERLINE    = ansi(24)
NO_REVERSE      = ansi(27)
NO_STRIKE       = ansi(29)
OVERLINE        = ansi(53)
NO_OVERLINE     = ansi(55)
FG_BLACK        = ansi(30)
FG_RED          = ansi(31)
FG_GREEN        = ansi(32)
FG_YELLOW       = ansi(33)
FG_BLUE         = ansi(34)
FG_MAGENTA      = ansi(35)
FG_CYAN         = ansi(36)
FG_WHITE        = ansi(37)
FG_RESET        = ansi(39)
BG_BLACK        = ansi(40)
BG_RED          = ansi(41)
BG_GREEN        = ansi(42)
BG_YELLOW       = ansi(43)
BG_BLUE         = ansi(44)
BG_MAGENTA      = ansi(45)
BG_CYAN         = ansi(46)
BG_WHITE        = ansi(47)
BG_RESET        = ansi(49)

def fg_256(n):return f"\033[38;5;{n}m"
def bg_256(n):return f"\033[48;5;{n}m"
def fg_rgb(r,g,b):return f"\033[38;2;{r};{g};{b}m"
def bg_rgb(r,g,b):return f"\033[48;2;{r};{g};{b}m"


def fmt_error(message:str): return FG_RED + "ERROR : " + RESET + message
def fmt_warning(message:str): return FG_YELLOW + "WARNING : " + RESET + message


def move_cursor(row:int,clm:int):print(f"\033[{row};{clm}H",end="",flush=True)
    
def erase_line(mode:Literal["TO_LINE_END","FROM_LINE_START","ENTIRE_LINE"]="ENTIRE_LINE"):
    if mode=="TO_LINE_END":         print("\033[0K",end="",flush=True)
    elif mode=="FROM_LINE_START":   print("\033[1K",end="",flush=True)
    elif mode=="ENTIRE_LINE":       print("\033[2K",end="",flush=True)



if __name__=="__main__":
    move_cursor(1,1)
    erase_line()
