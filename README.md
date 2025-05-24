```plaintext
                                 |\    /|
                              ___| \,,/_/
                           ---__/ \/    \
                          __--/     (D)  \
                          _ -/    (_      \
                         // /       \_ /  -\
   __-------_____--___--/           / \_ O o)
  /                                 /   \__/
 /                                 /
||          )                   \_/\
||         /              _      /  |
| |      /--______      ___\    /\  :
| /   __-  - _/   ------    |  |   \ \
 |   -  -   /                | |     \ )
 |  |   -  |                 | )     | |
  | |    | |                 | |    | |
  | |    < |                 | |   |_/
  < |    /__\                <  \
  /__\                       /___\
Boj4ckHoor3man 🐴 
```

> **Ready to automate your Namasha videos?**  
> **Copy a video link and BOOM!** 🔥💥
---
## 🚀 Overview

This is a functional Python automation tool designed to:
- Open **Namasha** video links in Potplayer!!

---

## 📦 First-Time Setup

Before running the program, make sure you've done the following steps:

### 1. Configure config.ini

a file called config.ini in the root of the project directory, fill it like this:

ini
[Paths]
edge_driver_path = C:\Path\To\Your\msedgedriver.exe
potplayer_path = C:\Path\To\Your\PotPlayer\PotPlayerMini64.exe

[Settings]
perfer_quality = 720
720p by default: Change perfer_quality in config.ini to your preferred resolution.


2. Install Microsoft Edge 🌐
If you don't have Edge installed yet, run this PowerShell command:
```
cd ~\Downloads; Start-BitsTransfer "https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx?platform=Default&source=EdgeStablePage&Channel=Stable&language=en&brand=M100" .\MicrosoftEdgeSetup.exe; Invoke-Expression .\MicrosoftEdgeSetup.exe
```

3. Install the Edge WebDriver 🔧
Go to:
🔗 Microsoft Edge WebDriver Downloads
```https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?form=MA13LH#downloads```

Download the WebDriver that matches your version of Edge.

Extract msedgedriver.exe to a folder on your system.

Update the edge_driver_path in config.ini to point to this msedgedriver.exe.

Made by Boj4ckHoor3man 🐴 with 💻
