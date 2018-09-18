#!/bin/sh

HOST=google.de

if ping -c1 $HOST 1>/dev/null 2>/dev/null
then
	echo "We have a internet connection"
else
	echo "No internet connection!"
	echo "Running lynx script"
	lynx -cmd_script=staff.log -accept_all_cookies http://www.google.de
fi
