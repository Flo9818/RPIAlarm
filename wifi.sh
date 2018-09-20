#!/bin/bash

HOST=google.de

if ping -c1 $HOST 1>/dev/null 2>/dev/null
then
	echo "We have a internet connection"
	env > success.list
else
	echo "No internet connection!"
	echo "Running lynx script"
	env > fail.list
	lynx --cmd_script=RPIAlarm/staff.log --accept_all_cookies http://www.google.de
fi
