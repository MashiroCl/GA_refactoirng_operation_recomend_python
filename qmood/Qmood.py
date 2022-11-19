from .metricCalculation import *


class Qmood():

    def __init__(self, java_classes):
        self.DSC = len(java_classes)
        self.hierarchies = count_hierarchies(java_classes)
        self.NOH = self.hierarchies
        self.classes_with_child_class = count_classes_with_child_class(java_classes)
        self.ANA = self.classes_with_child_class
        self.DAM = 0
        self.DCC = 0
        self.CAM = 0
        self.MOA = 0
        self.MFA = 0
        self.NOP = 0
        self.CIS = 0
        self.NOM = 0
        self.Resusability = 0
        self.Flexibility = 0
        self.Understandability = 0
        self.Functionality = 0
        self.Extendibility = 0
        self.Effectiveness = 0

    def calculateQmood(self, java_classes, user_defined_packages, inline_class_info):
        'obtain metrics for all classes and calculate the average value '
        sDAM, sDCC, sCAM, sMOA, sMFA, sNOP, sCIS, sNOM = 0, 0, 0, 0, 0, 0, 0, 0
        length = len(java_classes)
        for each in java_classes:
            sDAM += DAM(each)
            sDCC += DCC(each, user_defined_packages)
            sCAM += CAM(each)
            sMOA += MOA(each, user_defined_packages)
            sMFA += MFA(each)
            curNOP = NOP(each)
            if curNOP != 0:
                sNOP += curNOP
            sCIS += CIS(each)
            curNOM = NOM(each)
            if curNOM != 0:
                sNOM += curNOM
        self.DSC = DSC(length, inline_class_info)
        self.NOH = NOH(length, inline_class_info)
        self.ANA = ANA(len(self.classes_with_child_class), inline_class_info, length)
        self.DAM = sDAM / length
        self.DCC = sDCC / length
        self.CAM = sCAM / length
        self.MOA = sMOA / length
        self.MFA = sMFA / length
        self.NOP = sNOP / length
        self.CIS = sCIS / length
        self.NOM = sNOM / length

        # print("DSC:{},NOH:{},ANA:{},DAM:{},DCC:{},CAM:{},MOA:{},MFA:{},NOP:{},CIS:{},NOM:{}".format(self.DSC,self.NOH,self.ANA,self.DAM,self.DCC,self.CAM,self.MOA,self.MFA,self.NOP,self.CIS,self.NOM))

        self.Resusability = -0.25 * self.DCC + 0.25 * self.CAM + 0.5 * self.CIS + 0.5 * self.DSC
        # print("====================================================================================")
        # print(f"DCC:{self.DCC}, CAM:{self.CAM}, CIS:{self.CIS}, DSC:{self.DSC}")
        # print("====================================================================================")
        self.Flexibility = 0.25 * self.DAM - 0.25 * self.DCC + 0.5 * self.MOA + 0.5 * self.NOP
        self.Understandability = -0.33 * self.ANA + 0.33 * self.DAM - 0.33 * self.DCC + 0.33 * self.CAM - 0.33 * self.NOP - 0.33 * self.NOM - 0.33 * self.DSC
        self.Functionality = 0.12 * self.CAM + 0.22 * self.NOP + 0.22 * self.CIS + 0.22 * self.DSC + 0.22 * self.NOH
        self.Extendibility = 0.5 * self.ANA - 0.5 * self.DCC + 0.5 * self.MFA + 0.5 * self.NOP
        self.Effectiveness = 0.2 * self.ANA + 0.2 * self.DAM + 0.2 * self.MOA + 0.2 * self.MFA + 0.2 * self.NOP

        result = dict()
        result["Resusability"] = self.Resusability
        result["Flexibility"] = self.Flexibility
        result["Understandability"] = self.Understandability
        result["Functionality"] = self.Functionality
        result["Extendibility"] = self.Extendibility
        result["Effectiveness"] = self.Effectiveness
        return result
