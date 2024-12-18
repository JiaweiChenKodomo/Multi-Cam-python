# What it does and what you need
This repo contains the Python scripts to set up servers and clients to control Canon cameras remotely. A number of cameras can be connected to computers running the server. The client controls the cameras by sending instructions to the servers. This code is used in our lab to control multiple cameras during tests. 

What you need are:
1. A Canon camera.
2. A computer running the server code, connected to the Canon camera. Current server code assumes that one server controls one camera, which is the case in our lab where you need to control cameras over a large area. With a few modifications to the server code and client code, one server can control more than one camera.
3. A computer (usu. a seperate one from the server) running the client code to control all servers. 
4. USB and power cables.
5. Access to the correct version of Canon EDSDK. 
*****

# Compile C++ program for Windows by Canon
## Operating environment
 Canon recommends using this sample with "windows terminal" because it uses ESC character (\033) for screen control.

## Install build tools
 Visual Studio 2019 version 16.5 or later
 Build it as a cmake project.

## Build Method
 1.Download the package. Note that the EDSDK in the current directory is for Linux. Replace it with EDSDK for Windows, which can be downloaded from Canon's developer website.

 2.Start Visual Studio.

 3.Click "Open a local folder,"
   Select the package folder.

 4.Choose between x64-Debug or x64-Release
   If you want to run the sample app on another PC rather than a build machine, you must build it with x 64 -Release.

 5.Build -> Build All


*****

# for Linux
## Operating environment
 Canon recommends using this sample with
  "Raspberry Pi 4/Raspberry Pi OS 32bit" and "Jetson nano/ubuntu18.04 64bit."

## Install build tools

 1.Install toolchain
  sudo apt install cmake build-essential

  ### for jetson nano:
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:ubuntu-toolchain-r/test
    sudo apt-get update
    sudo apt install gcc-9 g++-9
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 10
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 10


## Build Method
 1.Download the package.

 2.Go to the folder.
   cd Multi-Cam-python

 3.Edit CMakeLists.txt
  If you are building on the arm64 architecture, change line 61 of "CMakeLists.txt" to:
    ${EDSDK_LDIR}/Library/ARM64/libEDSDK.so
  If you are building with arm32 architecture, you do not need to change it.

 4.Configure
   cmake CMakeLists.txt

 5.Build
   make

## Trouble shooting tips
 1. If the camera can't be found, it is likely because Nautilus is holding the USB device. Disable Nautilus automount.
 `gsettings set org.gnome.desktop.media-handling automount false`
To enable it again use the following:
 `gsettings set org.gnome.desktop.media-handling automount true`
This works for Jetson Nano.

The real issue is likely `gvfs-gphoto2-volume-monitor` holding up the camera storage. On Raspbian OS, one would need to kill `gvfs-gphoto2-volume-monitor` before connecting to the camera. This is done automatically in the `server3.py` code.

## Automatically start the server on start up.
On the Raspberry Pi (etc.) controling the camera (i.e., the server), run the startup script by adding the following line to `/etc/rc.local`:
 `sudo bash /home/peer/Desktop/MultiCamCui/Documents/startup.sh  > /tmp/basherr.log 2>&1 &`
The directory should be changed according to the directory of the project as well as the type of the camera used. 
See `./etc/rc.local` in the project directory for example. ` /etc/rc.local` needs to be set to execuatble:
`sudo chmod +x /etc/rc.local`. Also make sure system service is enabled with `rc.local` as suggested by [this post](https://www.linuxbabe.com/linux-server/how-to-enable-etcrc-local-with-systemd).

## Run the client code to control the cameras remotely.
To trigger camera events, run the `client2.py` and put in instructions as prompted on any machine. In `client2.py`, the IP and the names of the servers need to be specified. 
***** 

# How to use the sample app by Canon
 1.Connect the camera to your PC with a USB cable.

 2.Run MultiCamCui.exe.
   The top menu lists the detected cameras.

 3.Select the camera you want to connect.
   ex.
   - Select camera No.2 to No.5
     Enter "2-5"

   - Select camera No.3
     Enter "3"

   - Select all listed cameras
     Enter "a"

   - Quit the app
     Enter "x"

   * The camera number changes in the order you connect the camera to your PC.

 4.Control menu
   The control menu is the following:
		[ 1] Set Save To
		[ 2] Set Image Quality
		[ 3] Take Picture and download
		[ 4] Press Halfway
		[ 5] Press Completely
		[ 6] Press Off
		[ 7] TV
		[ 8] AV
		[ 9] ISO
		[10] White Balance
		[11] Drive Mode
		[12] Exposure Compensation
		[13] AE Mode (read only)
		[14] AF Mode (read only)
		[15] Aspect setting (read only)
		[16] Get Available shots (read only)
		[17] Get Battery Level (read only)
		[18] Edit Copyright
		[20] Get Live View Image
		[30] All File Download
		[31] Format Volume
    [32] Set Meta Data(EXIF) to All Image files
		[33] Set Meta Data(XMP) to All Image files

   Select the item number you want to control.
   The following is a description of the operation for each input number.
   *Enter "r" key to move to "Top Menu"

		[ 1] Set Save To
    Set the destination for saving images.

		[ 2] Set Image Quality
    Set the image Quality.

		[ 3] Take Picture and download
    Press and release the shutter button without AF action,
    create a "cam + number" folder in the folder where MultiCamCui.exe is located
    and save the pictures taken with each camera.

    * If you can't shoot, change the mode dial to "M" and then try again.
    * The camera number changes in the order you connect the camera to your PC.

		[ 4] Press Halfway
    Press the shutter button halfway.

		[ 5] Press Completely
    Press the shutter button completely.
    When Drive mode is set to continuous shooting,
    Continuous shooting is performed.

		[ 6] Press Off
    Release the shutter button.

		[ 7] TV
    Set the Tv settings.

		[ 8] AV
    Set the Av settings.

		[ 9] ISO
    Set the ISO settings.

		[10] White Balance
    Set the White Balance settings.

		[11] Drive Mode
    Set the Drive mode settings.

		[12] Exposure Compensation
    Set the exposure compensation settings.

		[13] AE Mode (read only)
    Indicates the AE mode settings. (not configurable)

		[14] AF Mode (read only)
    Indicates the AF mode settings. (not configurable)

	  [15] Aspect setting (read only)
    Indicates the aspect settings. (not configurable)

	  [16] Get Available shots (read only)
    Indicates the number of shots available on a camera. (not configurable)

	  [17] Get Battery Level (read only)
    Indicates the camera battery level. (not configurable)

	  [18] Edit Copyright
    Indicates/Set a string identifying the copyright information on the camera.

		[20] Get Live View Image
    Get one live view image.
    In the folder where MultiCamCui.exe is located
    Automatically create a "cam number" folder and save each camera's image.

		[30] All File Download
    Download all picture File in the camera's card to PC.
    In the folder where MultiCamCui.exe is located
    automatically create a "cam number" folder and save each camera's image.

		[31] Format Volume
    Formats volumes of memory cards in a camera.

    [32] Set Meta Data(EXIF) to All Image files
    Writes information from "resources/gpsexifdata.txt"to the metadata of an image (Jpeg only) in the camera.

		[33] Set Meta Data(XMP) to All Image files
    Writes information from "resources/metadata_xmp.txt"to the metadata of an image (Jpeg only) in the camera.
    
   * Some settings may not be available depending on the mode dial of the camera.
     If you can't set, change the mode dial to "M" and then try again.
