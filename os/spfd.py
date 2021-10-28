import numpy as np
from pyevtk.hl import polyLinesToVTK,imageToVTK
class spfd():
    def __init__(self):
        # self.Lx = gridLength[0]
        # self.Ly = gridLength[1]
        # self.Lz = gridLength[2]
        self.CoilCurrent = None
        self.affineMat = None
        self.jmag = None
        self.jx = None
        self.jy = None
        self.jz = None


    def convCsv2xyz(self,coil_path):
        x_all = []
        y_all = []
        z_all = []
        pointsPerLine = []
        new_file =[]
        with open(coil_path,mode='r') as f:
            for line in f:
                line = line.replace(',NaN','').replace(',\n','\n')
                each_line = np.fromstring(line, dtype=float, sep=",")
                current = each_line[0]
                x = each_line[1::3]*1e3
                y = each_line[2::3]*1e3
                z = each_line[3::3]*1e3
                x_all.append(x)
                y_all.append(y)
                z_all.append(z)
                pointsPerLine.append(len(x))
                new_file.append(line)
        with open(coil_path,mode='w') as f:
            for line in new_file:
                f.write(line)
        self.CoilCurrent = np.abs(current)
        x = np.asarray(np.concatenate(x_all), order='C')
        y = np.asarray(np.concatenate(y_all), order='C')
        z = np.asarray(np.concatenate(z_all), order='C')
        pointsPerLine = np.array(pointsPerLine)
        return (x,y,z,pointsPerLine)

    def getAffineMatrix(self,coil_position_path):
        with open(coil_position_path) as f:
            for line in f:
                li=line.strip()
                if not li.startswith("#"):
                    pos = line.split()
                    total_len = len(pos)
                    move_arr = np.array(pos[total_len-12:total_len-9],dtype=np.float).reshape(3,1)
                    rot_arr = np.array(pos[total_len-9:total_len],dtype=np.float).reshape(3,3)
                    rot_arr = rot_arr.T
                    break
        affineMat = np.hstack([rot_arr,move_arr])
        affineMat = np.vstack([affineMat,np.array([0,0,0,1])])
        self.affineMat = affineMat
        return (move_arr,rot_arr)

    def visCoil(self,output_coil_vtk_path,coil_csv_path,coil_position_path=None):
        # print('please check grid length is correct, Lx='+str(self.Lx)+',Ly='+str(self.Ly) + ',Lz='+str(self.Lz) )
        x,y,z,pointsPerLine = self.convCsv2xyz(coil_csv_path)
        print(polyLinesToVTK(output_coil_vtk_path,x,y,z,pointsPerLine=pointsPerLine))
        if coil_position_path is not None:
            move_arr,rot_arr = self.getAffineMatrix(coil_position_path)
            x1, y1, z1 = np.dot(rot_arr, np.array([x, y, z]))
            x1, y1, z1 = x1+(move_arr[0]), y1+(move_arr[1]), z1+(move_arr[2])
            # x1, y1, z1 = np.dot(self.affineMat, np.array([x, y, z]))
            save_path = polyLinesToVTK(output_coil_vtk_path,x1,y1,z1,pointsPerLine=pointsPerLine)
            print('with position file, vtk file be overwritten in: '+ save_path)

    def visBrain( self, brain_map_path,spacing):
        output_brain_vtk_path =  brain_map_path.split('.')[0] +'_visBrain'
        with open(brain_map_path) as f:
            first_line = f.readline()
            Dx,Dy,Dz  = [int(t.split('=')[1]) for t in first_line[1:].split(',')[0:3] ]
            print("Readed Array Size",Dx,Dy,Dz)
            lines = f.readlines()
            print("Total lines number:",len(lines))
            Vol = np.zeros((Dx,Dy,Dz))
            for i in range(Dz):
                try:
                    one_slice = np.loadtxt([t.replace(',\n','\n') for t in lines[0+(Dy)*i:Dy+(Dy)*i]], delimiter=',').T
#                     print(one_slice.shape)
                    Vol[:,:,i] = one_slice
                except:
                    print("error happens on z index: "+ str(i))

            imageToVTK(
                output_brain_vtk_path,
                spacing=spacing,
                pointData={'brain':Vol}
            )


    def visE(self,output_j_vtk_path,result_file_name,conductivity=0.11,assign_idx=-1):
        return self.visJ(output_j_vtk_path,result_file_name,varibale_name='E',conductivity=conductivity,assign_idx=assign_idx)

    def visJ(self,output_j_vtk_path,result_file_name,varibale_name='J',conductivity=1,assign_idx=-1):
        txt_keyword = varibale_name +':'
        with open(result_file_name, 'r') as f:
            for line in f:
                if line[:3] == 'LD:':
                    # first_line = f.readline()
                    lengths,dim = line.replace('LD:', '').split(':')
                    lengths = [float(l)*1e3 for l in lengths.split(',')]
                    # self.Lx,self.Ly,self.Lz = lengths
                    # origin = tuple([-t/2 for t in lengths])
                    dim = [int(num) for num in dim.split(',')]
                    print("lengthe is " + str(lengths))
                    print("dim is " + str(dim))
                    spacing = tuple([lengths[i]/dim[i] for i in range(3)])
                    jx = np.zeros(dim)
                    jy = np.zeros(dim)
                    jz = np.zeros(dim)
                elif line[:2] == 'J:':
                    index,j_vec = line.replace('J:','').split('=')
                    material = int(index.split(',')[-1])
                    if assign_idx != -1 and assign_idx!=material:
                        continue
                    index = tuple([int(t) for t in index.split(',')][:-1])
                    j_vec = [float(t) for t in j_vec.split(',')]
                    jx[index] = j_vec[0]/conductivity
                    jy[index] = j_vec[1]/conductivity
                    jz[index] = j_vec[2]/conductivity
                else:
                    print("This line didn't processed :" + line)
                    continue
        jmag = np.sqrt(jx**2+jy**2+jz**2)
        self.jmag = jmag
        self.jx = jx
        self.jy = jy
        self.jz = jz
#         self.jmag = jmag.copy()
        dict_key = [ varibale_name + t for t in ['x','y','z','mag']]
        write_file_name = imageToVTK(
            output_j_vtk_path,
            origin=(0,0,0),
            spacing=spacing,
            pointData={dict_key[0]:jx,dict_key[1]:jy,dict_key[2]:jz,dict_key[3]:jmag}
        )
        print(write_file_name)
        return jmag
#         return jmag.copy()
