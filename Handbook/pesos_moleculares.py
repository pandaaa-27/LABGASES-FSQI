#masa_molar
import re
w_atomico={
    "Hf":178.49,
    "Hs":277,
    "He": 4.002602,
    "Ho":164.93032,
    "H": 1.00794,
    "In":114.818,
    "I":126.90447,
    "Ir":192.217,
    "Fe":55.9349421,
    "Kr":83.798,
    "La":138.9055,
    "Lr":262.1097,
    "Pb":207.2,
    "Li": 6.941,
    "Lu":174.967,
    "Mg":24.3050,
    "Mn":54.9380496,
    "Mt":268.1388,
    "Md":258.0984,
    "Hg":200.59,
    "Mo":95.94,
    "Nd":144.24,
    "Ne":19.9924401759,
    "Np":237.0482,
    "Ni":58.6934,
    "Nb":92.90638,
    "N":14.0067,
    "No":259.1010,
    "Os":190.23,
    "O":15.9994,
    "Pd":106.42,
    "P": 30.973761,
    "Pt": 195.078,
    "Pu":244.0642,
    "Po":208.9824,
    "K":39.0983,
    "Pr":140.90765,
    "Pm":144.9127,
    "Pa":231.03588,
    "Ra":226.0254,
    "Rn":222.0176,
    "Re":186.207,
    "Rh":102.90550,
    "Rb":85.4678,
    "Ru":101.07,
    "Rf":261.1088,
    "Sm":150.36,
    "Sc":44.955910,
    "Sg":266.1219,
    "Se":78.96,
    "Si": 28.0855,
    "Ag":107.8682,
    "Na":22.98976967,
    "Sr":87.62,
    "S":32.065,
    "Ta":180.9479,
    "Tc":97.9072,
    "Te":127.60,
    "Tb":158.92534,
    "Tl":204.3833,
    "Th":232.0381,
    "Tm":168.93421,
    "Sn":118.710,
    "Ti":47.867,
    "W":183.84,
    "Uub":285,
    "Uuh":289,
    "Uuq":289,
    "Uuu":272.1535,
    "U":238.02891,
    "V": 50.9415,
    "Xe":131.293,
    "Y":88.90585,
    "Zn":65.409,
    "Zr":91.224,
    "Be":9.012182,
    "B":10.811,
    "C": 12.0107,
    "F":18.99840320,
    "Al":26.981538,
    "Cl": 35.453,
    "Ar": 39.948,
    "Ca": 40.078,
    "Cr": 51.9961,
    "Co":58.933200,
    "Cu":63.546,
    "Ba": 137.327,
    "Sb": 121.760,
    "As":74.92160,
    "Bi": 208.98038,
    "Br":79.904,
    "Cd": 112.411,
    "Ce":140.116,
    "Cs": 132.90545,
    "Fr":223.0197,
    "Au":196.96655,
}

    
#estos funcionan en simultaneo
def masa(Formula,n):
    Formula=re.sub(r"([A-Z][a-z]?)(\d+)",r"\1*\2",Formula) #multiplica el numero con la letra
    Formula=re.sub(r"([A-Za-z0-9])(?=[A-Z])",r"\1+",Formula) #Separa si hay mas de un elmento
    Formula=re.sub(r"([A-Za-z0-9])(?=\()",r"\1+",Formula) #Caso con () hace que lo que esta dentro del parentesis se sume
    Formula=re.sub(r"(\))(\d+)",r"\1*\2",Formula)#en el caso de encontrar parentesis y depsues un numero hace que se multiplique
    Formula=re.sub(r"(\))(?=[A-Z][a-z]?)",r"\1+",Formula) #si hay otro compuestoluego, hace que lo depsues del parentesis se sume(si es un elemnto)
    Formula=Formula.replace(".","+")
    for simb in  sorted(w_atomico.keys(),key=len,reverse=True):  #.keys() da los datos del diccionario
        Formula=re.sub(f'\\b{simb}\\b',str(w_atomico[simb]),Formula) 
    respuesta=eval(Formula)
    R=round(respuesta,n)
    return R

#key es el criterio con el que vas a ordenar
#reverse es para indicar si va ir ascendente(TRUE) o descente(FALSE,POR DEFECTO, SI NO SE COLOCA NADA)
#En este caso, es impt porque tenemos Ca y C, si primero
#detecta C (key->1), en compuestos como CaCO3, traduce como 12.00a
#el \ es para decir que lo que viene despues es el caracter 
#el \\b es el boundary es para decirle que debe tomar hasta donde termine la cadena(nombre de elemento)


if __name__=="__main__":
    Formula=input("Ingrese el elemento o compuesto: ")
    n=int(input("¿Cuantos decimales desea considerar? "))