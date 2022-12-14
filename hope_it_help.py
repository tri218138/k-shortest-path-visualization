# -*- coding: utf-8 -*-
"""hope it help

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19epZtqaQv8v4546o7QL03EzqiE4usvK0

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

df = pd.read_excel("dataset.xlsx", usecols="A", header=None)
df

num_rows = df.shape[0]
num_rows

class Point:
  ID = 0
  def __init__(self, coor):
    # self.street = src['Đường'].split(',')
    # self.name = src['Tên địa điểm']
    self.X = coor[0]
    self.Y = coor[1]
    self.ID = Point.ID
    Point.ID += 1

Points = []
Adjacency = []

def distance(p0, p1):
  return pow(pow((p0.X - p1.X),2) + pow((p0.Y - p1.Y),2), 1/2)

def find_in_Points(coor):
  if len(Points) == 0:
    return -1
  for idx in range(len(Points)):
    if Points[idx].X == coor[0] and Points[idx].Y == coor[1]:
      return idx
  return -1

for idx in range(num_rows):
  src = df.iloc(0)[idx][0]
  src = src.split(' ', 1)[1]
  src = src[1: -1]
  src = src.split(', ')

  listID = []

  for coor in src:
    coor = coor.split(' ')
    coor = [float(x) for x in coor]

    idx = find_in_Points(coor)    
    if idx == -1:
      Points.append(Point(coor))
      Adjacency.append([])
      listID.append(Points[-1].ID)
    else:
      listID.append(Points[idx].ID)
  # print(listID)
  n = len(listID)
  if n >= 2:
    if not listID[1] in Adjacency[listID[0]]:
      Adjacency[listID[0]].append(listID[1])
  for i in range(1, n - 1):
    if not listID[i - 1] in Adjacency[listID[i]]:
      Adjacency[listID[i]].append(listID[i - 1])
    if not listID[i + 1] in Adjacency[listID[i]]:
      Adjacency[listID[i]].append(listID[i + 1])
  if n >= 2:
    if not listID[n - 2] in Adjacency[listID[n - 1]]:
      Adjacency[listID[n - 1]].append(listID[n - 2])
    # print(listID[n - 1])

# print(Adjacency)

"""#Chuyển đổi dữ liệu sang class

Khoảng cách giữa 2 địa danh chỉ đo được khi hai địa danh nằm trên cùng 1 tuyến đường
"""

class Route:
  def __init__(self, src):
    self.v = [src]
    self.len = 0
  def __lt__(self, other):
    return self.len < other.len
  def __le__(self, other):
    return self.len <= other.len
  def add(self, vID, len):
    self.v.append(vID)
    self.len += len
  def get_tail(self):
    return self.v[-1]
  def get_vertices(self):
    return self.v

"""# Thiết lập giải thuật

## Ma trận liền kề
"""

# adjacency_matrix = np.zeros((df.shape[0], df.shape[0]))

# for i in range(df.shape[0]):
#   for j in range(df.shape[0]):
#     if i > j:
#       adjacency_matrix[i][j] = adjacency_matrix[j][i]
#     else:
#       adjacency_matrix[i][j] = positions[i].dist2(positions[j])

# adjacency_matrix[0]

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
			# print()
			exit()

# adjacency_matrix = [
#     [0, 2, 6, -1, 4],
#     [2, 0, 3, 5, -1],
#     [6, 3, 0, 1, -1],
#     [-1, 5, 1, 0, 2],
#     [4, -1, -1, 2, 0]
# ]

def flow_from_A_to_B(start, end, k = 3):
  # if (not start in range(df.shape[0])) or (not end in range(df.shape[0])):
  #   print('Điểm xuất phát hoặc điểm đến không hợp lệ')
  #   return []
  # k = min(max(3, k), 10)
  result = []
  cnt = np.zeros(len(Points))
  pq = PriorityQueue()
  pq.push(Route(start))
  # heapq.heappush(pri_queue, ) #length, link_list

  while not pq.isEmpty() and cnt[end] < k:
    shortest = pq.pop()
    u = shortest.get_tail()
    # print(shortest)
    cnt[u] += 1
    if (u == end):
      result.append(shortest)
    if cnt[u] <= k:
      # print(len(Adjacency[u]))
      for i in range(len(Adjacency[u])):
        v = Adjacency[u][i]
        dist = distance(Points[v], Points[u])
        # if adjacency_matrix[u][i] == -1:
        if not v in shortest.get_vertices():
          new_route = copy.deepcopy(shortest)
          new_route.add(v, dist)
          # print(new_route.v)
          pq.push(new_route)
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

df_des = pd.read_excel("destination.xlsx", usecols="A:C")
df_des

# source_name = input('Điểm khởi đầu của bạn là: ')
# destination_name = input('Đích đến của bạn là: ')
source_name = "Trường Đại học bách Khoa"
# destination_name = "Đại học Y DƯợc"
destination_name = "Chợ Bến Thành"
start = -1
end = -1

k = 3

namePlace = df_des['Tên địa điểm'].tolist()

for idx, x in enumerate(namePlace):
  if isTheyAreOne(x, source_name):
    start = idx
  if isTheyAreOne(x, destination_name):
    end = idx
# namePlace
print(start, end)

start = df_des.iloc(0)[start]
end = df_des.iloc(0)[end]

start = Point([float(start[2]), float(start[1])])
end = Point([float(end[2]), float(end[1])])

def get_closest_point(marker):
  minVal = 99999
  minIndex = 0
  for p in Points:
    tmp = distance(marker, p)
    if minVal > tmp:
      minVal = tmp
      minIndex = p.ID
  return minIndex

closest_start = get_closest_point(start)
closest_end = get_closest_point(end)

print(closest_start, closest_end)

"""##Kết quả"""

result = flow_from_A_to_B(closest_start, closest_end, k)

print(result)

for res in result:
  print(res.v)

"""## Lưu trữ"""
f = open("result.txt", "w")
for res in result:
  f.write(str(start.X) + ' ' + str(start.Y) + '\n')
  for v in res.v:
    f.write(str(Points[v].X) + ' ' + str(Points[v].Y) + '\n')
  f.write(str(end.X) + ' ' + str(end.Y) + '@\n')
  # f.write('@\n')
f.write('@\n')
f.close()
