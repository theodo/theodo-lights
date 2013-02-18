#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket


class DomoticController:

    ip = ''
    port = 20000
    password = '12345'

    def __init__(self, ip, password = '12345', port = 20000):
        self.ip       = ip
        self.port     = port
        self.password = password

    def command(self, switch_id, binary_state):
        BUFFER_SIZE = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.send("")
        data = s.recv(BUFFER_SIZE)

        s.send("*99*0##")
        data = s.recv(BUFFER_SIZE)

        auth_command = ownCalcPass(self.password, str(data[2:-2]))
        auth_command = '*#' + str(auth_command) + '##'
        s.send(auth_command)
        data = s.recv(BUFFER_SIZE)

        s.send("*1*" + str(binary_state) + "*" + str(switch_id) + "##")
        data = s.recv(BUFFER_SIZE)


def ownCalcPass (password, nonce) :
    m_1 = 0xFFFFFFFFL
    m_8 = 0xFFFFFFF8L
    m_16 = 0xFFFFFFF0L
    m_128 = 0xFFFFFF80L
    m_16777216 = 0XFF000000L
    flag = True
    num1 = 0L
    num2 = 0L
    password = long(password)

    for c in nonce :
        num1 = num1 & m_1
        num2 = num2 & m_1
        if c == '1':
            length = not flag
            if not length :
                num2 = password
            num1 = num2 & m_128
            num1 = num1 >> 7
            num2 = num2 << 25
            num1 = num1 + num2
            flag = False
        elif c == '2':
            length = not flag
            if not length :
                num2 = password
            num1 = num2 & m_16
            num1 = num1 >> 4
            num2 = num2 << 28
            num1 = num1 + num2
            flag = False
        elif c == '3':
            length = not flag
            if not length :
                num2 = password
            num1 = num2 & m_8
            num1 = num1 >> 3
            num2 = num2 << 29
            num1 = num1 + num2
            flag = False
        elif c == '4':
            length = not flag

            if not length:
                num2 = password
            num1 = num2 << 1
            num2 = num2 >> 31
            num1 = num1 + num2
            flag = False
        elif c == '5':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 << 5
            num2 = num2 >> 27
            num1 = num1 + num2
            flag = False
        elif c == '6':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 << 12
            num2 = num2 >> 20
            num1 = num1 + num2
            flag = False
        elif c == '7':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 & 0xFF00L
            num1 = num1 + (( num2 & 0xFFL ) << 24 )
            num1 = num1 + (( num2 & 0xFF0000L ) >> 16 )
            num2 = ( num2 & m_16777216 ) >> 8
            num1 = num1 + num2
            flag = False
        elif c == '8':
            length = not flag
            if not length:
                num2 = password
            num1 = num2 & 0xFFFFL
            num1 = num1 << 16
            num1 = num1 + ( num2 >> 24 )
            num2 = num2 & 0xFF0000L
            num2 = num2 >> 8
            num1 = num1 + num2
            flag = False
        elif c == '9':
            length = not flag
            if not length:
                num2 = password
            num1 = ~num2
            flag = False
        else :
            num1 = num2
        num2 = num1
    return num1 & m_1
