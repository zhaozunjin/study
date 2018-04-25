# -*- coding: utf-8 -*-
import socket,select,threading,sys
'''
聊天客户端
'''
class ChatClient():
	def __init__(self,host,port):
		self.HOST = host
		self.PORT = port
		self.client_socket = socket.socket()
		self.client_socket.connect((self.HOST,self.PORT))
		self.client_readlist = [self.client_socket]
	def receivemessage(self):
		while True:
			readlist,writelist,errorlist = select.select(self.client_readlist,[],[])
			if self.client_socket in readlist:
				try:
					#从服务器接收数据
					print self.client_socket.recv(4096).decode('utf-8')
				except socket.error as err:
					print 'connection error...'
					exit()
					
	def sendmessage(self):
		#发送数据，将客户端的数据发送出去
		while True:
			try:
				data = raw_input()
				#print 'data:%s'%data
			except Exception as e:
				print 'sorry,message cannot be entered because there are errors while connecting.'
				#exit()
				break
			try:
				self.client_socket.send(data.encode('utf-8'))
			except Exception as e:
				exit()
				
	def run(self):
		#分别启动接收数据和发送数据的线程
		thread_recievemsg = threading.Thread(target = self.receivemessage)
		thread_recievemsg.start()
		thread_sendmsg = threading.Thread(target = self.sendmessage)
		thread_sendmsg.start()
		
if __name__ =="__main__":
	HOST = socket.gethostname()
	PORT = 8888
	client  = ChatClient(HOST,PORT)
	client.run()
