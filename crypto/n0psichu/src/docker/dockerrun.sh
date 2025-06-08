#!/bin/bash

docker_name="n0psichu"
localhost_port=20210
docker_port=12431
haproxy_port=13371

for c in `docker ps -a | grep "$docker_name\|Created\|127.0.0.1:$(echo $localhost_port | head -c 4)\|Exited" | awk '{print $1}'`; do
	docker rm -f $c
done

# remove old and unused images
docker images | grep none | awk '{print $3}' | xargs -I mm docker rmi -f mm

if [ -z "$1" ]
then
      echo "\$1 is empty, we will run only 1 instance!"
      docker run -dit --restart always -p 127.0.0.1:$localhost_port:$docker_port $docker_name
      num=1
else
	num=$1
	re='^[0-9]+$'
	if ! [[ $1 =~ $re ]] ; then
		echo "error: Not a number" >&2; exit 1
	fi
	echo "we will run $1 instance of this docker"
	for port in `seq $localhost_port $(echo $localhost_port + $num - 1| bc -l)`; do
		docker run -dit --restart always -p 127.0.0.1:$port:$docker_port $docker_name
	done
fi

tab='\t'

printf "#----------------------------------------------------------------------------------------------------\n" > haproxy.txt
printf "frontend $docker_name"_"$haproxy_port\n" >> haproxy.txt
printf "$tab bind 127.0.0.1:$haproxy_port\n" >> haproxy.txt
printf "$tab mode tcp\n" >> haproxy.txt
printf "$tab option tcplog\n" >> haproxy.txt
printf "$tab timeout client 5m\n" >> haproxy.txt
printf "$tab # Table definition\n" >> haproxy.txt
printf "$tab stick-table type ip size 100k expire 30s store conn_cur\n" >> haproxy.txt
printf "$tab # Allow clean known IPs to bypass the filter\n" >> haproxy.txt
printf "$tab # tcp-request connection accept if { src -f /etc/haproxy/whitelist.lst }\n" >> haproxy.txt
printf "$tab # Shut the new connection as long as the client has already 10 opened\n" >> haproxy.txt
printf "$tab tcp-request connection reject if { src_conn_cur ge 10 }\n" >> haproxy.txt
printf "$tab tcp-request connection track-sc1 src\n" >> haproxy.txt
printf "$tab default_backend $docker_name\n" >> haproxy.txt
printf "\n" >> haproxy.txt
printf "backend $docker_name\n" >> haproxy.txt
printf "$tab mode tcp\n" >> haproxy.txt
printf "$tab option tcplog\n" >> haproxy.txt
printf "$tab option log-health-checks\n" >> haproxy.txt
printf "$tab option redispatch\n" >> haproxy.txt
printf "$tab log global\n" >> haproxy.txt
printf "$tab balance source\n" >> haproxy.txt
printf "$tab timeout connect 120s\n" >> haproxy.txt
printf "$tab timeout server 2m\n" >> haproxy.txt
for i in `seq -w 00 $(echo $num - 1| bc -l)`; do
	printf "$tab server $docker_name""_$i 127.0.0.1:""$(echo $localhost_port + $i | bc -l) check maxconn 30\n" >> haproxy.txt
done;