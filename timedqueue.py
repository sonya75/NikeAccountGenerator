from threading import Lock,Condition
import Queue
import time
class TimedQueue:
	def __init__(self):
		self.itemqueue=Queue.PriorityQueue()
		self.getlock=Lock()
		self.itemlock=Lock()
		self.itemconfirm=Condition(self.itemlock)
	def get(self,nowait=False):
		self.getlock.acquire()
		while True:
			self.itemlock.acquire()
			if self.itemqueue.qsize()==0:
				if nowait:
					self.itemlock.release()
					self.getlock.release()
					raise Exception
				self.itemconfirm.wait()
				self.itemlock.release()
				continue
			else:
				w=self.itemqueue.get()
				z=w[0]-time.time()
				if z<=0:
					self.itemlock.release()
					self.getlock.release()
					return w[1]
				else:
					self.itemqueue.put(w)
					if nowait:
						self.itemlock.release()
						self.getlock.release()
						raise Exception
					self.itemconfirm.wait(timeout=z)
					self.itemlock.release()
					continue
	def get_nowait(self):
		return self.get(True)
	def put(self,item,timeafter=0):
		self.itemlock.acquire()
		self.itemqueue.put((time.time()+timeafter,item))
		self.itemconfirm.notify()
		self.itemlock.release()