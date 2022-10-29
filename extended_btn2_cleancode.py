# -*- coding: utf-8 -*-
"""Extended-BTN2-cleanCode

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BIjUOc8CCrDPry7QzfhjkuAFNd05i28e

# Trường Đại học Bách Khoa thành phố Hồ Chí Minh  
# Group:
Phan Gia Anh - 2270167  
Nguyễn Trường Thành - 2270084  
Nguyễn Đức Phú - 2171014  
Đoàn Trần Cao Trí (Leader) - 2010733

# Đề tài: Mô phỏng map (google map) và tìm đường đi ngắn nhất từ điểm A đến điểm B. Ngoài ra, đề xuất đường đi ngắn thứ nhì và thứ ba

##Ý tưởng: 
Dữ liệu:  
*) Địa điểm trên google map sẽ lưu về (tên, kinh độ, vĩ độ)  
*) Chuyển dữ liệu trên thành ma trận liền kề  
Giải thuật:  
*) Tìm đường đi ngắn thứ k với priority queue
Ghi chú:
*) Dữ liệu tọa độ của 1 địa điểm trên google map có thể là tọa độ điểm trung tâm tùy vào góc nhìn của bạn, nên cẩn thận để lấy chính xác tọa độ của địa điểm đó.
"""

import numpy as np
import pandas as pd
import heapq #priority queue
import copy

"""#Lấy dữ liệu"""

df = pd.read_excel("dataGGmap.xlsx",usecols="A:D")
df

df.dtypes

df.iloc(0)[1]

df.iloc(0)[1][0]

"""#Chuyển đổi dữ liệu sang class

Khoảng cách giữa 2 địa danh chỉ đo được khi hai địa danh nằm trên cùng 1 tuyến đường
"""

class Position:
  ID = 0
  def __init__(self, src):
    self.street = src['Đường'].split(',')
    self.name = src['Tên địa điểm']
    self.X = src['x'] * 1000
    self.Y = src['y'] * 1000
    self.ID = Position.ID
    Position.ID += 1
  def intersection(self, lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
  def dist2(self, another):
    tmp = self.intersection(self.street, another.street)
    if len(tmp) > 0:
      return pow(pow((self.X - another.getX()),2) + pow((self.Y - another.getY()),2), 1/2)
    else:
      return -1
  def getX(self):
    return self.X
  def getY(self):
    return self.Y
  def getID(self):
    return self.ID

"""Xem thử 1 mẫu ví dụ"""

positions = []
for i in range(df.shape[0]):
  positions.append(Position(df.iloc(0)[i]))
positions[0].name

"""## Ma trận liền kề"""

adjacency_matrix = np.zeros((df.shape[0], df.shape[0]))

for i in range(df.shape[0]):
  for j in range(df.shape[0]):
    if i > j:
      adjacency_matrix[i][j] = adjacency_matrix[j][i]
    else:
      adjacency_matrix[i][j] = positions[i].dist2(positions[j])

adjacency_matrix[3]

"""# Thiết lập giải thuật

## Route class
"""

class Route:
  def __init__(self, src):
    self.v = [src]
    self.len = 0
  def __lt__(self, other):
    return self.len < other.len
  def __le__(self, other):
    return self.len <= other.len
  def add(self, v, len):
    self.v.append(v)
    self.len += len
  def get_tail(self):
    return self.v[-1]
  def get_vertices(self):
    return self.v
  def draw_by_id(self):
    content = "Đường đi: " + str(self.v[0])
    for i in range(1, len(self.v)):
      content += " -> " + str(self.v[i])
    content += " = " + str(self.len)
    print(content)
  def draw_by_name(self):
    content = "Đường đi: " + positions[self.v[0]].name
    for i in range(1, len(self.v)):
      content += " -> " + positions[self.v[i]].name
    content += " = " + str(self.len)
    print(content)
  def intersection(self, lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
  def getStreetThrough(self):
    segment = []
    for i in range(1, len(self.v)):
      inter = self.intersection(positions[self.v[i]].street, positions[self.v[i - 1]].street)
      segment.append(inter)
    ## remove duplicate adjecently
    for i in range(1, len(segment)):
      if (segment[i] == segment[i - 1]):
        segment[i - 1] = ''
    segment = [value for value in segment if value != '']
    return segment

"""## Implement Pririty Queue"""

# A simple implementation of Priority Queue
# using Queue.
class PriorityQueue(object):
	def __init__(self):
		self.queue = []

	def __str__(self):
		return ' '.join([str(i) for i in self.queue])

	# for checking if the queue is empty
	def isEmpty(self):
		return len(self.queue) == 0

	# for inserting an element in the queue
	def push(self, data):
		self.queue.append(data)

	# for popping an element based on Priority
	def pop(self):
		try:
			min_val = 0
			for i in range(len(self.queue)):
				if self.queue[i] < self.queue[min_val]:
					min_val = i
			item = self.queue[min_val]
			del self.queue[min_val]
			return item
		except IndexError:
			print()
			exit()

# adjacency_matrix = [
#     [0, 2, 6, -1, 4],
#     [2, 0, 3, 5, -1],
#     [6, 3, 0, 1, -1],
#     [-1, 5, 1, 0, 2],
#     [4, -1, -1, 2, 0]
# ]

def flow_from_A_to_B(start, end, k = 3):
  if (not start in range(df.shape[0])) or (not end in range(df.shape[0])):
    print('Điểm xuất phát hoặc điểm đến không hợp lệ')
    return []
  # k = min(max(3, k), 10)
  result = []
  cnt = np.zeros(df.shape[0])
  pq = PriorityQueue()
  pq.push(Route(start))

  # heapq.heappush(pri_queue, ) #length, link_list

  while not pq.isEmpty() and cnt[end] < k:
    shortest = pq.pop()
    u = shortest.get_tail()
    # print(shortest)
    cnt[u] += 1
    if (u == end):
      # sign = False
      # for rr in result:
      #   if rr.getStreetThrough() == shortest.getStreetThrough():
      #     sign = True
      # if not sign:
      #   result.append(shortest)
      # else:
      #   cnt[u] -= 1
      result.append(shortest)
    if cnt[u] <= k:
      for id in range(len(adjacency_matrix[u])):
        # if adjacency_matrix[u][i] == -1:
        if adjacency_matrix[u][id] > 0: # valid distance
          if not id in shortest.get_vertices(): # new point
            if len(positions[id].street) > 1 or id == end: # Giao lộ hoặc điểm cuối
              new_route = copy.deepcopy(shortest)
              new_route.add(id, adjacency_matrix[u][id])

              pq.push(new_route)
  # print(pq.isEmpty())
  return result

"""#Main function

##Nhận dữ liệu đầu vào

Tên địa danh được copy từ google map
"""

def isTheyAreOne(des0, des1):
  des0 = des0.lower()
  des1 = des1.lower()

  if (des0 == des1):
    return True
  if (des0 in des1) or (des1 in des0):
    return True
  return False

def getInput():
  return "trường đại học bách khoa", "chợ bến thành", 3
  source_name = input('Điểm khởi đầu của bạn là: ')
  destination_name = input('Đích đến của bạn là: ')
  # k = int(input('Nhập số đường đi gợi ý (default = 3): '))
  return source_name, destination_name, 3

source_name, destination_name, k = getInput()

def searchStartandEndDestination():
  start = []
  end = []

  namePlace = df['Tên địa điểm'].tolist()

  for idx, x in enumerate(namePlace):
    if isTheyAreOne(x, source_name):
      start.append(idx)
    if isTheyAreOne(x, destination_name):
      end.append(idx)
  return start, end

start, end = searchStartandEndDestination()

print(start, end)

def removeDuplicateStreet(res):
  for i in range(1, len(res)):
    if (res[i].getStreetThrough() == res[i - 1].getStreetThrough()):
      res[i - 1] = []
  res = [value for value in res if value != []]
  return res


def mainFunction(st, en, k):
  res = []
  for i in range(len(st)):
    for j in range(len(en)):
      res = res + flow_from_A_to_B(st[i], en[j], k)
  print(len(res))
  for r in res:
    r.draw_by_name()
    print(r.getStreetThrough())
  # print(res[0].getStreetThrough())
  res = removeDuplicateStreet(res)
  res.sort(key= lambda x: x.len)
  res = res[0: min(k, len(res))]
  # if (len(res) < k):
  #   k += 5
  #   res = mainFunction(start, end, k)
  return res

result = mainFunction(start, end, k)

"""##Kết quả"""

if len(result) > 0:
  for res in result:
    res.draw_by_name()


"""## Lưu trữ"""
f = open("result.txt", "w")
for res in result:
  for v in res.v:
    f.write(str(positions[v].Y/ 1000) + ' ' + str(positions[v].X / 1000) + '\n')
  f.write('@\n')
f.close()