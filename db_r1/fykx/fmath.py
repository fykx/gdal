from sklearn.metrics import confusion_matrix
import numpy as np
import re
import math


class ConfusionMatrix:
    def __init__(self, data, weight, predicted, actual, prob, thr):
        # data为csv文件（含表头）
        # weight为权重所在列的索引
        # predicted为预测值（运算提取）所在列的索引
        # actual为真实值（人工解译）所在列的索引
        # prob为可能所在列的索引
        # thr为阈值
        self.data = data
        self.weight = weight
        self.predicted = predicted
        self.actual = actual
        self.prob = prob
        self.thr = thr

    def read_weight(self):
        a = []
        f = open(self.data, 'r')
        f.readline()
        for line in f.readlines():
            a.append(float(re.split(',', line.strip())[self.weight]))
        f.close()
        return a

    def read_predicted(self):
        a = []
        f = open(self.data, 'r')
        f.readline()
        for line in f.readlines():
            if re.split(',', line.strip())[self.predicted] != "None":
                a.append('true')
            else:
                a.append('false')
        f.close()
        return a

    def read_actual(self):
        a = []
        f = open(self.data, 'r')
        f.readline()
        for line in f.readlines():
            if re.split(',', line.strip())[self.actual] != "None":
                a.append('true')
            else:
                a.append('false')
        f.close()
        return a
    
    def read_prob(self):
        a = []
        f = open(self.data, 'r')
        f.readline()
        for line in f.readlines():
            a.append(re.split(',', line.strip())[self.prob])
        f.close()
        return a

    def overall_accuracy(self):
        predicted_value = self.read_predicted()
        actual_value = self.read_actual()
        weight_value = self.read_weight()
        prob_value = self.read_prob()

        for i in range(len(prob_value)):
            if prob_value[i] != "None" and  float(prob_value[i]) < self.thr:
                predicted_value[i] = 'false'
        c = confusion_matrix(actual_value, predicted_value, labels=['true', 'false'])
        oa = np.sum(np.diag(c))/np.sum(c)
        return oa

    def pro_accuracy_true(self):
        predicted_value = self.read_predicted()
        actual_value = self.read_actual()
        weight_value = self.read_weight()
        prob_value = self.read_prob()
        for i in range(len(prob_value)):
            if prob_value[i] != "None" and  float(prob_value[i]) < self.thr:
                predicted_value[i] = 'false'
        c = confusion_matrix(actual_value, predicted_value, labels=['true', 'false'])
        pat = c[0, 0]/np.sum(c[0, :])
        return pat

    def pro_accuracy_false(self):
        predicted_value = self.read_predicted()
        actual_value = self.read_actual()
        weight_value = self.read_weight()
        prob_value = self.read_prob()
        for i in range(len(prob_value)):
            if prob_value[i] != "None" and  float(prob_value[i]) < self.thr:
                predicted_value[i] = 'false'
        c = confusion_matrix(actual_value, predicted_value, labels=['true', 'false'])
        paf = c[1, 1]/np.sum(c[1, :])
        return paf

    def user_accuracy_true(self):
        predicted_value = self.read_predicted()
        actual_value = self.read_actual()
        weight_value = self.read_weight()
        prob_value = self.read_prob()
        for i in range(len(prob_value)):
            if prob_value[i] != "None" and  float(prob_value[i]) < self.thr:
                predicted_value[i] = 'false'
        c = confusion_matrix(actual_value, predicted_value, labels=['true', 'false'])
        uat = c[0, 0]/np.sum(c[:, 0])
        return uat

    def user_accuracy_false(self):
        predicted_value = self.read_predicted()
        actual_value = self.read_actual()
        weight_value = self.read_weight()
        prob_value = self.read_prob()
        for i in range(len(prob_value)):
            if prob_value[i] != "None" and  float(prob_value[i]) < self.thr:
                predicted_value[i] = 'false'
        c = confusion_matrix(actual_value, predicted_value, labels=['true', 'false'])
        uaf = c[1, 1]/np.sum(c[:, 1])
        return uaf


class RmseMae:
    def __init__(self, data, predicted, actual):
        # 本段代码计算时将年份值+1970，还原真实年份
        # data为csv文件（含表头）
        # predicted为预测值（运算提取）所在列的索引
        # actual为真实值（人工解译）所在列的索引
        self.data = data
        self.predicted = predicted
        self.actual = actual

    def read_predicted(self):
        a = []
        f = open(self.data, 'r')
        f.readline()
        for line in f.readlines():
            if re.split(',', line.strip())[self.predicted] != "None":
                a.append(re.split(',', line.strip())[self.predicted])
            else:
                a.append('false')
        f.close()
        return a

    def read_actual(self):
        a = []
        f = open(self.data, 'r')
        f.readline()
        for line in f.readlines():
            if re.split(',', line.strip())[self.actual] != "None":
                a.append(re.split(',', line.strip())[self.actual])
            else:
                a.append('false')
        f.close()
        return a

    def root_mean_square_error(self):
        predicted_value = self.read_predicted()
        actual_value = self.read_actual()

        f = []
        for i in range(len(predicted_value)):
            if predicted_value[i] == 'false' or actual_value[i] == 'false':
                pass
            else:
                f.append(float(predicted_value[i]) - float(actual_value[i]) + 1970.0)
        a = 0
        b = 0
        for j in f:
            a = a + j ** 2
        b = math.sqrt(a / len(f))
        return b

    def mean_absolute_error(self):
        predicted_value = self.read_predicted()
        actual_value = self.read_actual()

        f = []
        for i in range(len(predicted_value)):
            if predicted_value[i] == 'false' or actual_value[i] == 'false':
                pass
            else:
                f.append(float(predicted_value[i]) - float(actual_value[i]) + 1970.0)
        c = 0
        d = 0
        for x in f:
            c = c + abs(x)
        d = c / len(f)
        return d

