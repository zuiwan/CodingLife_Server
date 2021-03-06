#!/usr/bin/env bash
rm /root/CodingHub/logs/*_supervisor.log

#echo "-----------强制更新代码-----------"
#git fetch --all
#git reset --hard origin/dev

# upgrade database
python tool/create_db.py
if [ ! -d "/root/CodingHub/migrations" ]; then
  python tool/database_manager.py orm init
fi
python tool/database_manager.py orm migrate
python tool/database_manager.py orm upgrade



#docker service rm $(docker service ls | awk '{print $1}')

#supervisord
supervisorctl restart uwsgi:CodingHub
#supervisorctl restart celery_cpu
#supervisorctl restart celery_gpu
#supervisorctl restart celery_fork