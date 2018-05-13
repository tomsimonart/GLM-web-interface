# Guide
---
## Installation
* Clone :

    >```cd ./GLM-web-interface```

* Install python packages (**Using "**virtualenv**" is recommended**) :

    >```pip install -r requirements.txt```

    > You also have to install **TKinter** (for the guishow feature)

* Upload the arduino sketch (tested with **arduino uno**):

    > You can for example use the **Arduino IDE** or **PlatformIO**

    > The sketch is located in ***LMPM/GLM/matrix_IO/matrix_IO.ino***

## Starting

* Start LMPM :

    >```./lmpm```

    the available arguments can be found with :

    >```./lmpm -h```

    some examples :

    >```./lmpm -vvv```

    >```./lmpm -s```

    >```./lmpm -V check -V info -m```

## Web
* Url should be

    > **[http://localhost:5000](http://localhost:5000)**

#### Special thanks
* **Maribib** for his more than great help with the server
* **Mino** for the guishow feature and for making this project happen
* **Etnarek** and **iTitou** for their help with the arduino code
