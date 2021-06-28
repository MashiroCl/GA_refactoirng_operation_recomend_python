from metricCalculation import *

class Qmood():
    def __init__(self):
        self.DSC=0
        self.NOH=0
        self.ANA=0
        self.DAM=0
        self.DCC=0
        self.CAM=0
        self.MOA=0
        self.MFA=0
        self.NOP=0
        self.CIS=0
        self.NOM=0
        self.Resusability = 0
        self.Flexibility = 0
        self.Understandability = 0
        self.Functionality = 0
        self.Extendibility = 0
        self.Effectiveness = 0

    def calculateQmood(self,jClass,jClassList):
        self.DSC=DSC()
        self.NOH=NOH()
        self.ANA=ANA()

        self.DAM=DAM(jClass)
        self.DCC=DCC(jClassList)
        self.CAM=CAM(jClass)
        self.MOA=MOA(jClassList,jClass)
        self.MFA=MFA(jClass)
        self.NOP=NOP(jClass)
        self.CIS=CIS(jClass)
        self.NOM=NOM(jClass)

        self.Resusability = -0.25*self.DCC+0.25*self.CAM+0.5*self.CIS+0.5*self.DSC
        self.Flexibility = 0.25*self.DAM-0.25*self.DCC+0.5*self.MOA+0.5*self.NOP
        self.Understandability = -0.33*self.ANA+0.33*self.DAM-0.33*self.DCC+0.33*self.CAM-0.33*self.NOP-0.33*self.NOM-0.33*self.DSC
        self.Functionality = 0.12*self.CAM+0.22*self.NOP+0.22*self.CIS+0.22*self.DSC+0.22*self.NOH
        self.Extendibility = 0.5*self.ANA-0.5*self.DCC+0.5*self.MFA+0.5*self.NOP
        self.Effectiveness = 0.2*self.ANA+0.2*self.DAM+0.2*self.MOA+0.2*self.MFA+0.2*self.NOP



    def getResusability(self):
        return self.Resusability
    def getFlexibility(self):
        return self.Flexibility
    def getUnderstandability(self):
        return self.Understandability
    def getFunctionality(self):
        return self.Functionality
    def getExtendibility(self):
        return self.Extendibility
    def getEffectiveness(self):
        return self.Effectiveness
