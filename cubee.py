import magiccube

def up_face(alg):
    cube = magiccube.Cube(
        3, "YYYYYYYYYRRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBWWWWWWWWW")
    
    cube.reset()
    cube.rotate("Z Z")
    cube.rotate(alg)

    print(cube)

    c = str(cube)
    c = c[:100]
    c = c.replace(" ","")
    c = c.replace("\n","")
    return list(c)


c = up_face("L2 U L2 F2 L2 D' L2 U B2 F U' L2 F L' R2 U L D2 B' Rw Uw'")
print(c)