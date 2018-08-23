from hazard_substance.models import HazardousChemical

all_chemicals = HazardousChemical.objects.all()

for chem in all_chemicals:
    print(chem)

for chem in all_chemicals:
    print(chem.id, chem.name, chem.k7_1, chem.k7_2, chem.k7)
    k7_list = eval(chem.k7_1)
    if (k7_list[4]>9):
        k7_list[4] = k7_list[4]/10
        chem.k7_1 = str(k7_list)
        print(chem.id)
    if chem.k7_2==None:
        chem.k7_2 ='null'
    chem.k7 = '[{},{}]'.format(chem.k7_1,chem.k7_2)
    chem.save()
    print(chem.k7)
