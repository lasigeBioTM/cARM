def getNewStringESO(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = splitedName[0] + " " + splitedName[1] + "-" + splitedName[2]

    return newName


def getNewStringFSR(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = '[FSR2007]' + " " + splitedName[1]

    return newName


def getNewStringASCC(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = '[KPR2005]' + " " + splitedName[1]

    return newName


def getNewStringAlessi(name):
    name = name.replace('_', ' ')
    splitedName = name.split()
    newName = 'Cl' + " " + splitedName[0] + " " + splitedName[1]

    return newName


def getNewStringAlessiT(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = 'Cl' + " " + splitedName[0] + "-" + splitedName[1] + " " + splitedName[2]

    return newName


def getNewStringAntalova(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = 'Cl' + " " + splitedName[0] + " " + splitedName[1]

    return newName


def getNewStringBH(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = 'Cl' + " " + "VDBH" + " " + splitedName[1]

    return newName


def getNewStringBarkhatova(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = 'Cl' + " " + splitedName[0] + " " + splitedName[1]

    return newName


def getNewStringDolDzim(name):
    splitedName = name.split()

    newName = 'Cl' + " " + "Dolidze-Dzim" + " " + splitedName[2]

    return newName


def getNewStringDutra(name):
    splitedName = name.split()

    newName = "[DB2000] " + splitedName[2]

    return newName


def getNewStringIvanov(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = "[IBP2002] CC0" + " " + splitedName[1]

    return newName


def getNewStringLoden(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = "Cl" + " " + splitedName[0] + " " + splitedName[1]

    return newName


def getNewStringMamajek(name):
    splitedName = name.split()

    newName = "Cl" + " " + splitedName[0] + " " + splitedName[1]

    return newName


def getNewStringBergh(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = "Cl VDB " + splitedName[1]

    return newName

def getNewStringAveni(name):
    name = name.replace('_', ' ')
    splitedName = name.split()

    newName = "Cl AH " + splitedName[2]

    return newName

def getNewName(name):
    if name.startswith("ESO") and (len(name.split()) == 3 or len(name.split('_')) == 3):
        name = getNewStringESO(name)

    elif name.startswith("FSR") and (len(name.split()) == 2 or len(name.split('_')) == 2):
        name = getNewStringFSR(name)

    elif name.startswith("ASCC") and (len(name.split()) == 2 or len(name.split('_')) == 2):
        name = getNewStringASCC(name)

    elif name.startswith("Alessi") and (len(name.split()) == 2 or len(name.split('_')) == 2):
        name = getNewStringAlessi(name)

    elif name.startswith("Alessi") and (len(name.split()) == 3 or len(name.split('_')) == 3):
        name = getNewStringAlessiT(name)

    elif name == "Alicante 1":
        name = "Cl Alicante 1"

    elif name == "Andrews Lindsay 5":
        name = "[AL67] Cl* 5"

    elif name.startswith("Antalova") and (len(name.split()) == 2 or len(name.split('_')) == 2):

        name = getNewStringAntalova(name)

    elif name.startswith("BH") and (len(name.split()) == 2 or len(name.split('_')) == 2):

        name = getNewStringBH(name)

    elif name.startswith("Barkhatova") and (len(name.split()) == 2 or len(name.split('_')) == 2):

        name = getNewStringBarkhatova(name)

    elif name == "C1331 622":
        name = "C 1331-622"


    elif name.startswith("Dol") and len(name.split()) == 3:

        name = getNewStringDolDzim(name)

    elif name.startswith("Dutra") and len(name.split()) == 3:

        name = getNewStringDutra(name)

    elif name == "Havlen Moffat 1":
        name = "Cl HM 1"

    elif name.startswith("Ivanov") and (len(name.split()) == 2 or len(name.split('_')) == 2):

        name = getNewStringIvanov(name)

    elif name.startswith("Loden") and (len(name.split()) == 2 or len(name.split('_')) == 2):

        name = getNewStringLoden(name)

    elif name.startswith("Mamajek") and len(name.split()) == 2:

        name = getNewStringMamajek(name)

    elif name == "Pismis Moreno 1":
        name = name.replace('_', ' ')
        name = "Cl Pismis-Moreno 1"


    elif name == "Sher 1":
        name = "Cl Sher 1"

    elif name.startswith("vdBergh") and(len(name.split()) == 2 or len(name.split('_')) == 2):

        name = getNewStringBergh(name)

    elif name.startswith("Aveni") and(len(name.split()) == 3 or len(name.split('_')) == 3):
        name = getNewStringAveni(name)


    elif name.startswith("DBSB") and(len(name.split()) == 2 or len(name.split('_')) == 2):
        name = name.replace('_', ' ')
        name = name.split()

        name = "[DBS2003] " + name[1]

    elif name.startswith("Ferrero") and(len(name.split()) == 2 or len(name.split('_')) == 2):
        name = name.replace('_', ' ')
        name = name.split()

        name = "Cl Ferrero " + name[1]

    elif name.startswith("Gulliver") and(len(name.split()) == 2 or len(name.split('_')) == 2):
        name = name.replace('_', ' ')
        name = name.split()

        name = "Cl Gulliver " + name[1]

    return name
