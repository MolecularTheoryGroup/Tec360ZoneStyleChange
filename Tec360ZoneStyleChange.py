import TecUtil as tu
import TecVals as tv
from os import name

IsWindows = name == 'nt'

def ApplyFuncToZone(ZoneNames, PerfectNameMatch, FuncList):
    for i in range(1, tu.DataSetGetNumZones() + 1):
        Res = tu.ZoneGetName(i)
        if Res[0]:
            for z in ZoneNames:
                if z == Res[1] or (not PerfectNameMatch and z in Res[1]):
                    for f in FuncList:
                        f([i])
    return

def TP_RCSPaths(PathSize):#, ZoneName = "_RCS"):
    ApplyFuncToZone(["_RCS"], False, [lambda x: tu.ZoneSetScatter(tv.SV_SHOW, x, 0, False),
                               lambda x: [tu.ZoneSetMesh(i[0], x, i[1], i[2]) for i in [
                                            [tv.SV_SHOW, 0, True],
                                            [tv.SV_LINEPATTERN, 0, tv.LinePattern_LongDash],
                                            [tv.SV_PATTERNLENGTH, 0.5, 0],  
                                            [tv.SV_LINETHICKNESS, PathSize, 0],
                                            [tv.SV_COLOR, 0, tv.Red_C]
                                            ]
                                          ],
                               lambda x: tu.ZoneSetActive(x, tv.AssignOp_PlusEquals)
                               ])
    return

AtomStrs = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Uut", "Fl", "Uup", "Lv", "Uus", "Uuo"]

def SetupScatters(ZoneNames,ScatterSize):
    ApplyFuncToZone(ZoneNames, True, [lambda x: [tu.ZoneSetScatter(i[0], x, i[1], i[2]) for i in [
                                            [tv.SV_SHOW, 0, True],
                                            [tv.SV_FRAMESIZE, ScatterSize, 0]]
                                          ],
                               lambda x: tu.ZoneSetActive(x, tv.AssignOp_PlusEquals)
                               ])
    return

def TP_DoScatter(BigAtomSize):
    SetupScatters([AtomStrs[0]], BigAtomSize / 2)
    SetupScatters(AtomStrs[1:], BigAtomSize)
    SetupScatters(["%s CPs" % i for i in ["Nuclear","Bond","Ring","Cage"]], BigAtomSize * (5./16.))
    return

def TP_SetupBondPaths(PathSize):
    ApplyFuncToZone(["Bond path"], False, [lambda x: tu.ZoneSetScatter(tv.SV_SHOW, x, 0, False),
                               lambda x: [tu.ZoneSetMesh(i[0], x, i[1], i[2]) for i in [
                                            [tv.SV_SHOW, 0, True],
                                            [tv.SV_LINEPATTERN, 0, tv.LinePattern_Solid],
                                            [tv.SV_LINETHICKNESS, PathSize, 0],
                                            [tv.SV_COLOR, 0, tv.Black_C]
                                            ]
                                          ],
                               lambda x: tu.ZoneSetActive(x, tv.AssignOp_PlusEquals)
                               ])
    return

def TP_AddRCSPathsFromCSVs():
    import os
    Res = tu.DialogGetFileNames(tv.SelectFileOption_ReadMultiFile, "Comma-separated value files", [], "*.csv")
    tu.DialogMessageBox(str(Res), tv.MessageBox_Information)
    if not Res[0] or len(Res[1]) <= 0 or not os.path.isfile(Res[1][0]):
        return
    NumVars = tu.DataSetGetNumVars()
    for f in Res[1]:
        if os.path.isfile(f):
            File = open(f, 'r')
            ColNum = -1
            AllLines = File.readlines()
            aLine = AllLines[0].split(',')
            for i in range(len(aLine)):
                if "Bohr" in aLine[i]: 
                    ColNum = i
                    break
            XYZ = [] 
            if ColNum >= 0:
                for i in range(1,len(AllLines)-1):
                    XYZ.append([float(j) for j in AllLines[i].split(',')[ColNum:ColNum + 3]])
#                     tu.DialogMessageBox(str(XYZ), tv.MessageBox_Information)
                if IsWindows:
                    ZoneName = f.rpartition("\\")[2].rpartition('.')[0] + "_RCS"
                else:
                    ZoneName = f.rpartition("/")[2].rpartition('.')[0] + "_RCS"
                tu.DataSetAddZone(ZoneName, len(AllLines) - 2, 1, 1, tv.ZoneType_Ordered, [tv.FieldDataType_Double] * NumVars)
                ZoneNum = tu.DataSetGetNumZones()
                for i in range(1, 4):
                    ret = tu.IOrderedDataValuesSet(ZoneNum, i, [j[i-1] for j in XYZ])
                    
    return

def TP_AllInOneSmallSystem():
    TP_AddRCSPathsFromCSVs()
    TP_SetupBondPaths(1.5)
    TP_DoScatter(8)
    TP_RCSPaths(1.5)
    return

def TP_AllInOneBigSystem():
    TP_AddRCSPathsFromCSVs()
    TP_SetupBondPaths(0.4)
    TP_DoScatter(5)
    TP_RCSPaths(1.5)
    return