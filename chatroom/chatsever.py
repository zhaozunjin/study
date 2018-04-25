# -*- coding: utf-8 -*-
'''
聊天室服务器类
'''
import socket,select

class ChatSever():
	def __init__(self,host,port,numofclients):
		#初始化服务器
		self.HOST = host
		self.PORT = port
		self.sever_socket = socket.socket()
		#绑定到服务器地址和端口号
		self.sever_socket.bind((self.HOST,self.PORT))
		#设置最大监听数
		self.sever_socket.listen(numofclients)
		self.socket_list = []
		#连接进入服务器的客户端的名称
		self.client_names = {}
		self.socket_list.append(self.sever_socket)
		print 'Chatroom has been open...'
		
	def connect(self):
		#响应一个客户端请求，建立一个连接，用来收发数据
		client_conn,client_addr = self.sever_socket.accept()
		try:
			#向新的连接的客户端发送欢迎信息
			welcome_msg = 'welcome to chatroom,please enter your nickname:'
			client_conn.send(welcome_msg.encode('utf-8'))
			#接收客户端发来的用户名
			client_name = client_conn.recv(4096).decode('utf-8')
			self.socket_list.append(client_conn)
			self.client_names[client_conn] = client_name
			msg = 'There are ' + str(len(self.client_names))  + ' clients in chatroom: [' + ', '.join(list(self.client_names.values())) +']'
			client_conn.send(msg.encode('utf-8'))
			#向所有用户端发送新的成员信息
			for sock in self.client_names.keys():
				if (not sock == client_conn):
					msg = self.client_names[client_conn] + 'joins in chatroom'
					sock.send(msg.encode('utf-8'))
		except Exception as e:
			print e
			
			
	def disconnect(self):
		self.sever_socket.close()
		
		
	def run(self):
		#响应客户端连接和传输数据
		while True:
			#如果只是服务器开启，36000秒内没有客户端响应，则会超时关闭
			readlist,writelist,errorlist = select.select(self.socket_list,[],[],36000)
			if not readlist:
				print 'There is not connection,Chatroom is to be closed.'
				self.disconnect()
				break
			for client_socket in readlist:
				if client_socket is self.sever_socket:
					self.connect()
				else:
					#表示一个client连接上有数据到达服务器
					disconnection = False
					try:
						#接受客户端data,连接上有数据到达服务器
						data = client_socket.recv(4096).decode('utf-8')
						data = self.client_names[client_socket] + ':' + data 
					except socket.error as arr:
						#客户端异常表明该用户已经离线
						data = self.client_names[client_socket] + ':' + 'leave chatroom.'
						disconnection = True
					if disconnection:
						#如果用户离开聊天室，则从其他用户的读入列表readlist中移除
						self.socket_list.remove(client_socket)
						print data
						for sock in self.socket_list:
							if (not sock == self.sever_socket) and (not sock == client_socket):
								try:
									sock.send(data.encode('utf-8'))
								except Exception as e:
									print e
						del self.client_names[client_socket]
					else:
						print data
						for sock in self.socket_list:
							if (not sock == self.sever_socket) and (not sock == client_socket):
								try:
									sock.send(data.encode('utf-8'))
								except Exception as e:
									print e 
									

if __name__ =="__main__":
	HOST = socket.gethostname()
	PORT = 8888
	sever  = ChatSever(HOST,PORT,10)
	sever.run()