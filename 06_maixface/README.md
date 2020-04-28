### Maixpy Face-Recognition Model

https://www.maixhub.com/index.php/index/index/detail/id/235.html


### MaixPy firmware Configration

Within Ubuntu Enviroment

#### downloads

~~~
$ git clone https://github.com/sipeed/MaixPy.git
$ git submodule update --recursive --init
~~~

#### Python Install

~~~
$ conda create -n ml python=3.6
$ conda activate ml
$ pip install -r requirements.txt
~~~

#### kendryte-toolchain Install
~~~
$ wget http://dl.cdn.sipeed.com/kendryte-toolchain-ubuntu-amd64-8.2.0-20190409.tar.xz
$ sudo tar -Jxvf kendryte-toolchain-ubuntu-amd64-8.2.0-20190409.tar.xz -C /opt
$ ls /opt/kendryte-toolchain/bin
~~~

#### MaixPy firmware Build

~~~
$ cd MaixPy
$ cd projects/maixpy_k210/
$ python project.py menuconfig
$ python project.py build
~~~
