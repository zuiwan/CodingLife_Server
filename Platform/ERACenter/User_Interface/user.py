#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       user
   Description:
   Author:          huangzhen
   date:            2018/3/13
-------------------------------------------------
   Change Activity:
                   2018/3/13:
-------------------------------------------------
The makeReservation method

The interface with the user reservation requests is composed of the single “makeReservation” method, which handles a job reservation request that is sent by some user. Each reservation request can either be accepted and priced or declined by ERA.
The basic input parameters to this method are the job’s bid and the identifier of the job. The bid encapsulates a list of resource requests along with the maximum price that the user is willing to pay in order to get this request (as described above). The output is an acceptance or rejection of the request, and the price that the user will be charged for fulfilling his request in case of acceptance.（Alternatively, the system may allow determining the payment after running is completed (depending on the system load at that time), or may allow flexible payments that take into account boththe amount of resources reserved and the amount of resources actually used.）

The main effect of accepting a job request is that the user is guaranteed to be given the desired amount of resources sometime within the desired time window. An accepted job must be ready to use all requested resources starting at the beginning of the requested window, and the request is considered fulfilled as long as ERA provides the requested resources within the time window.
"""
from Library.singleton import Singleton, ThreadSafeSingleton

__author__ = 'huangzhen'
import socket
import json
import os
import traceback
import struct

from Library.extensions import orm as db
from Platform.ERACenter.Core.model import Job

ERA_PORT = 5555


class Reservation_Center(object):
    REQ_EOF_HEADER = '\t'
    REQ_EOF_CONFIRM = '\n'

    def __init__(self):
        # endpoint = ("api.cannot.cc", ERA_PORT)
        endpoint = ("127.0.0.1", ERA_PORT)

        # 创建一个socket:
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 建立连接:
        try:
            self.conn.connect(endpoint)
        except socket.error as e:
            print("warning: %s" % str(e))
            raise e

    def makeReservation(self, request):
        # 组装符合格式要求的请求，向Go提供的接口发起预定请求
        # TODO: check request and reformat it
        # 发送
        try:
            msg2send = json.dumps(request.to_dict())
            self.conn.send(msg2send + self.REQ_EOF_HEADER + self.REQ_EOF_CONFIRM)
        except os.error as e:
            print("error", str(e), traceback.format_exc())
            return None
        except socket.error as e:
            print("error", str(e), traceback.format_exc())
            return None
        # 接收
        buffer = []
        first = True
        while True:
            # 每次最多接收1k字节:
            bytes_readed = self.conn.recv(1024)
            if bytes_readed:
                if first is True:
                    # 这里的长度是具体的消息长度，不包括终结符
                    # 长度为uint32，占了4个字节，加上2个字节的终结符
                    content_length, = struct.unpack("i", bytes_readed[:4])  # I == unsigned int, 4bytes
                    print("debug", "received content-length: %d bytes" % content_length)
                    if content_length > (1024 - 6):
                        # 消息超过1024字节
                        first = False
                        continue
                    else:
                        buffer.append(bytes_readed[4:])
                        break
                else:
                    buffer.append(bytes_readed)
            else:
                break
        # self.conn.close()
        if not len(buffer) > 0:
            print("warning: not received msg from era server")
            return None
        data = ''.join(buffer)
        try:
            s = data.strip().rstrip(self.REQ_EOF_HEADER + self.REQ_EOF_CONFIRM)
            data = json.loads(s)
        except ValueError as e:
            print("error", str(e), traceback.format_exc())
        print("debug", data)
        return data

    def finish(self):
        # 关闭连接:
        self.conn.close()


@Singleton
class User_Interface(object):
    def __init__(self):
        self.db = db

    def Create_Job(self, env, uid, gid, doc, duration, project_id, code_id, data_ids, entry_cmd, start_cmd,
                   b_tensorboard, b_jupyter, perm):
        job = Job(env=env, uid=uid, gid=gid, doc=doc, duration=duration, project_id=project_id, code_id=code_id,
                  data_ids=data_ids,
                  entry_cmd=entry_cmd,
                  start_cmd=start_cmd,
                  b_tensorboard=b_tensorboard, b_jupyter=b_jupyter, perm=perm)
        self.db.session.add(job)
        self.db.session.commit()
        return job
