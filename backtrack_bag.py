import time
from typing import List
import csv

# 定义物品类
class Item:
    def __init__(self, value: int, weight: int):
        self.value = value
        self.weight = weight
        self.unit_value = value / weight  # 单位重量价值

# 全局变量
C = 20  # 背包总容量
n = 3   # 物品数量
items = [
    Item(25, 18),
    Item(24, 15),
    Item(15, 10)
]
best_value = 0  # 当前最优值
best_solution = []  # 当前最优解

# 回溯函数，使用“当前价值 + 剩余价值”限界
def backtrack1(i: int, current_weight: int, current_value: int, selection: List[int]):
    global best_value, best_solution

    # 计算当前节点的上界
    remaining_value = sum(item.value for item in items[i:])  # 剩余物品总价值
    bound = current_value + remaining_value
    if bound <= best_value:  # 剪枝
        return

    if i == n:  # 遍历到叶子节点
        if current_value > best_value:
            best_value = current_value
            best_solution = selection[:]  # 记录当前最优解
        return

    # 不选择第 i 个物品
    selection[i] = 0
    backtrack1(i + 1, current_weight, current_value, selection)

    # 选择第 i 个物品（前提是重量不超过背包容量）
    if current_weight + items[i].weight <= C:
        selection[i] = 1
        backtrack1(i + 1, current_weight + items[i].weight, current_value + items[i].value, selection)

# 贪心思想计算上界
def calculate_bound(i: int, current_weight: int, current_value: int) -> float:
    bound = current_value
    remaining_capacity = C - current_weight

    # 按单位重量价值从大到小排序物品（已经排序好）
    for j in range(i, n):
        if items[j].weight <= remaining_capacity:
            bound += items[j].value
            remaining_capacity -= items[j].weight
        else:
            bound += items[j].unit_value * remaining_capacity
            break

    return bound

# 回溯函数，使用“贪心思想”限界
def backtrack2(i: int, current_weight: int, current_value: int, selection: List[int]):
    global best_value, best_solution

    if i == n:  # 遍历到叶子节点
        if current_value > best_value:
            best_value = current_value
            best_solution = selection[:]  # 记录当前最优解
        return

    # 计算当前节点的上界
    bound = calculate_bound(i, current_weight, current_value)
    if bound <= best_value:  # 剪枝
        return

    # 不选择第 i 个物品
    selection[i] = 0
    backtrack2(i + 1, current_weight, current_value, selection)

    # 选择第 i 个物品（前提是重量不超过背包容量）
    if current_weight + items[i].weight <= C:
        selection[i] = 1
        backtrack2(i + 1, current_weight + items[i].weight, current_value + items[i].value, selection)

# 主函数
if __name__ == "__main__":
    # 按单位重量价值对物品排序（贪心限界需要此步骤）
    items.sort(key=lambda x: x.unit_value, reverse=True)

    # 记录选择状态
    selection = [0] * n

    # 初始化计时结果
    results = []

    # 运行两种限界方法1000次，并计算平均时间
    for method in range(1, 3):
        total_time = 0
        for _ in range(1000):
            best_solution = [0] * n  # 重置最优解
            if method == 1:
                start = time.perf_counter_ns()
                best_value = 0  # 重置最佳价值
                backtrack1(0, 0, 0, selection)
                end = time.perf_counter_ns()
            else:
                start = time.perf_counter_ns()
                best_value = 0  # 重置最佳价值
                backtrack2(0, 0, 0, selection)
                end = time.perf_counter_ns()

            total_time += (end - start)

        average_time = total_time // 1000
        results.append((f"限界{method}", best_value, average_time))

        # 打印最优解和统计信息到控制台
        print(f"{f'限界{method}'}：最大价值 = {best_value}, 平均运行时间 = {average_time} 纳秒, 最优解 = {best_solution}")

    # 输出结果到CSV文件（不含最优解）
    with open("backtrack_bag.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["限界方法", "最大价值", "平均运行时间（纳秒）"])
        csvwriter.writerows(results)
