# :star: LMPM (Led Matrix Plugin Manager)
<img align="right" src="https://i.imgur.com/tpx3227.jpg">

Script your own plugins and display **whatever you want** on a L.E.D. matrix
and control/interact with your plugins from a web interface.

<img src="https://img.shields.io/badge/platform-linux-lightgrey.svg"> <img src="https://img.shields.io/badge/release-v0.11.1--alpha-8833bb.svg"> <img src="https://img.shields.io/badge/license-MIT-blue.svg">

##  :computer: Hardware
* Computer with [python 3](https://www.python.org/downloads/) installed (tested on linux only)
* [Arduino UNO](https://store.arduino.cc/arduino-uno-rev3)
* [L.E.D. Matrix](https://www.ebay.com/itm/Provide-Arduino-code-64x16-dot-Matrix-LED-for-diy-Sign-Light-Neon-Bright-UNO-MCU-/271303628009?pt=LH_DefaultDomain_0&hash=item3f2af4d4e9) (only works on this one for now)

<img src="https://i.imgur.com/ONcQDo8.gif">

---

# :beginner: Guide
## :scroll: Installation
* Clone :

    >```git clone https://github.com/tomsimonart/LMPM.git```

    >```cd ./LMPM```

<img src="https://i.imgur.com/epAzNsI.png" heigth="150" width="370" align="right">

* Install python packages (**Using "**virtualenv**" is recommended**) :

    >```pip install -r requirements.txt```

    > You also need to install [TKinter](https://wiki.python.org/moin/TkInter) (for the **guishow** feature)
    

* Upload the arduino sketch to your arduino (tested with **arduino uno**):

    > You can for example use the [Arduino IDE](https://www.arduino.cc/en/Main/Software) or [PlatformIO](https://platformio.org/platformio-ide)

    > The sketch is located in [LMPM/GLM/matrix_IO/matrix_IO.ino](https://github.com/tomsimonart/LMPM/blob/master/GLM/matrix_IO/matrix_IO.ino)


## :rocket: Starting

* Start LMPM :

    >```./lmpm```

    the available arguments can be found with :

    >```./lmpm -h```

    some examples :

    >```./lmpm -vvv```

    >```./lmpm -s```

    >```./lmpm -V check -V info -m```

## :earth_africa: Web
* Url should be

    > **[http://localhost:5000](http://localhost:5000)** (also works for multiple clients)

## :green_book: Documentation
* Full documentation will *soon* (:feelsgood:) be available [here](https://tomsimonart.github.io/LMPM/)



#### :+1: Special thanks
* **Maribib** for his help with the server
* **Mino** for the guishow feature
* **Etnarek** and **iTitou** for their help with the arduino code
