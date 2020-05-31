import numpy as np
from pyevtk.hl import polyLinesToVTK,imageToVTK
class convSPFDFormat():
    def __init__(self,gridLength=(150,150,75)):
        self.Lx = gridLength[0]
        self.Ly = gridLength[1]
        self.Lz = gridLength[2]
        self.CoilCurrent = None
        
    def convCsv2xyz(self,coil_path):
        coils = np.loadtxt(coil_path, delimiter=',')
        x_all = []
        y_all = []
        z_all = []
        # coil_arr_size = coils.shape
        pointsPerLine = np.zeros(len(coils))
        for i,each_line in enumerate(coils):
            current = each_line[0]
            x = each_line[1::3]*1e3
            y = each_line[2::3]*1e3
            z = each_line[3::3]*1e3
            x_all.append(x) 
            y_all.append(y)
            z_all.append(z)
            pointsPerLine[i] = len(x) 
        self.CoilCurrent = np.abs(current)
        x = np.asarray(np.concatenate(x_all), order='C')
        y = np.asarray(np.concatenate(y_all), order='C')
        z = np.asarray(np.concatenate(z_all), order='C')
        return (x,y,z,pointsPerLine)
    
    def getAffineMatrix(self,coil_position_path):
        with open(coil_position_path) as f:
            for line in f:
                li=line.strip()
                if not li.startswith("#"):
                    pos = line.split()
                    move_arr = np.array(pos[1:4],dtype=np.double)
                    rot_arr = np.array(pos[4:],dtype=np.double).reshape(3,3)
        return (move_arr,rot_arr) 
    
    def visCoil(self,output_coil_vtk_path,coil_csv_path,coil_position_path=None):
        print('please check grid length is correct, Lx='+str(self.Lx)+',Ly='+str(self.Ly) + ',Lz='+str(self.Lz) )
        x,y,z,pointsPerLine = self.convCsv2xyz(coil_csv_path)
        print(polyLinesToVTK(output_coil_vtk_path,x,y,z,pointsPerLine=pointsPerLine))
        if coil_position_path is not None:
            move_arr,rot_arr = self.getAffineMatrix(coil_position_path)
            x1, y1, z1 = np.dot(rot_arr, np.array([x, y, z]))
            x1, y1, z1 = x1+(move_arr[0] - self.Lx/2), y1+(move_arr[1]- self.Ly/2), z1+(move_arr[2]-self.Lz/2)
            save_path = polyLinesToVTK(output_coil_vtk_path,x1,y1,z1,pointsPerLine=pointsPerLine)
            print('with position file, vtk file be overwritten in: '+ save_path)
    
    def visB(self,output_j_vtk_path,result_file_name):
        self.visJ(output_j_vtk_path,result_file_name,varibale_name='B')
        
    def visJ(self,output_j_vtk_path,result_file_name,varibale_name='J'):
        txt_keyword = varibale_name +':'
        with open(result_file_name, 'r') as f:
            first_line = f.readline()
            lengths,dim = first_line.replace('LD:', '').split(':')
            lengths = [float(l)*1e3 for l in lengths.split(',')]
            self.Lx,self.Ly,self.Lz = lengths
            origin = tuple([-t/2 for t in lengths])
            dim = [int(num) for num in dim.split(',')]
            spacing = tuple([lengths[i]/dim[i] for i in range(3)])
            jx = np.zeros(dim)
            jy = np.zeros(dim)
            jz = np.zeros(dim)
            for line in f:
                if line[:2] == 'C:':
                    break
                index,j_vec = line.replace(txt_keyword,'').split('=')
                index = tuple([int(t) for t in index.split(',')][:-1])
                j_vec = [float(t) for t in j_vec.split(',')]
                jx[index] = j_vec[0]
                jy[index] = j_vec[1]
                jz[index] = j_vec[2]
        jmag = np.sqrt(jx**2+jy**2+jz**2)
        dict_key = [ varibale_name + t for t in ['x','y','z','mag']]
        write_file_name = imageToVTK(
            output_j_vtk_path,
            origin=origin,
            spacing=spacing,
            pointData={dict_key[0]:jx,dict_key[1]:jy,dict_key[2]:jz,dict_key[3]:jmag}
        )
        print(write_file_name)
     