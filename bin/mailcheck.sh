#!/bin/bash

read -r pid < ~/.offlineimap/pid

if ps $pid &>/dev/null; then

 echo "offlineimap ($pid): another instnce running." >&2
 kill -9 $pid
fi

nice -10 offlineimap -o

new_mail=0
maildir=" "

sum_mail=0

mailcheck | grep new | grep INBOX 2>&1 >/dev/null
if [ $? -eq 0 ];
then

	maildir=`mailcheck | grep new | grep INBOX | awk '{ print $NF }' \
		| sed 's/\// /g' | awk '{ print $NF }' \
		| awk '{ printf "%s ", $0 }' | sed 's/ /, /g' \
		| sed 's/, $//'`

	new_mail=`mailcheck | grep new | grep INBOX | awk '{ print $3 }'`

	for N in `echo $new_mail`
	do
		sum_mail=`expr $sum_mail + $N`
	done

	if [ $sum_mail -eq 1 ] ;
	then
		DISPLAY=:0 notify-send -c email.arrived -u normal -i mail_new \
		"You have $sum_mail new mail:" "$maildir"
	else
		DISPLAY=:0 notify-send -c email.arrived -u normal -i mail_new \
		"You have $sum_mail new mails:" "$maildir"
	fi
fi

