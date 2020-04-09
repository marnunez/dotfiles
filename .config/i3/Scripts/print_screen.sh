#!/bin/bash
case $1 in 
	window_file)
	import -window $(xprop -root | awk '/_NET_ACTIVE_WINDOW\(WINDOW\)/{print $NF}') ~/Imágenes/screenshots/window_screenshot_from_$(date +%Y-%m-%d_%H-%M-%S).png && notify-send 'Captura de la ventana creada en ~/Imágenes/screenshots'
	;;
	screen_file)	
 	import -window root ~/Imágenes/screenshots/screenshot_from_$(date +%Y-%m-%d_%H-%M-%S).png && notify-send 'Captura de pantalla creada en ~/Imágenes/screenshots'
	;;
	section_file)
	maim -s ~/Imágenes/screenshots/section_from_$(date +%Y-%m-%d_%H-%M-%S).png && notify-send 'Captura de región creada en ~/Imágenes/screenshots'
	;;
	window_clipboard)
	maim -i $(xdotool getactivewindow) | xclip -selection clipboard -t image/png && notify-send 'Captura de ventana copiada al portapapeles'
	;;
	screen_clipboard)
	maim | xclip -selection clipboard -t image/png && notify-send 'Captura de pantalla copiada al portapapeles'
	;;
	section_clipboard)
	maim -s | xclip -selection clipboard -t image/png && notify-send 'Captura de región copiada al portapapeles'
	;;
esac
