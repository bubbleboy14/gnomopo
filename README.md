# gnomopo
GNOme MOuse POsitioner is a Gnome Shell Extension that exposes the mouse position, as well as a python module that wraps communication with the extension in a function, getpos().

This is intended for vanilla/default (Wayland / Gnome Mutter) Ubuntu, which doesn't seem to have an easier way AFAICT.

v0.1

## installation
Type this:

```
pip install gnomopo
gnomopo install
```

First, that will install the gnome extension. Then, it will instruct you to restart your gnome session (to load the extension) and run `gnomopo install` again (to enable the extension).

## cli
In addition to `gnomopo install`, you can type `gnomopo getpos` to get the mouse position.

## py
You can also call it from a python script:

```
import gnomopo
x, y = gnomopo.getpos()
```

## todo
The shell extension currently listens on a port (AF_INET), but it would probably be better to listen on a unix socket (AF_UNIX), or maybe use dbus.