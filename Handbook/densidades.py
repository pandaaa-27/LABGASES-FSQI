#DENSIDADES
#Agua
from math import*
from sympy import*
def densidad_agua(x):
        Den_agua= (1e-12 * x**5) - (4e-10 * x**4) + (6e-08 * x**3) - (8e-06 * x**2) + (6e-05 * x) + 0.9998
        return Den_agua
def densidad_hielo(x):
        Den_hielo=(-1e-09 * x**3) - (7e-07 * x**2) - (0.0002 * x) + 0.9168
        return Den_hielo





