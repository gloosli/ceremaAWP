import h5py
import os
import sys
import argparse
import csv
import numpy as np
from sklearn.model_selection import ShuffleSplit
from PIL import Image, ImageOps


def get_image(file,width,height,square):
    image = Image.open('.'+file)
    if square==True:
        new_image = ImageOps.fit(image, (int(width),int(width)), Image.ANTIALIAS, 0, (0.5, 0.5))
    else:
        new_image = image.resize((int(width),int(height)))
    return np.array(new_image)


def create(f,prop,square):

    # used values
    imW = 1024
    imH = 631
    lW = ['JB1','JB2','JCN','JP1','JP2','NB1','NB2','NCN','NP1','NP2']
    lC = ['V1','V2']
    lP = ['Ped1','Ped2','Ped3','Ped4','Ped5']
    prop = np.float64(prop)

    # store file structure
    train = f.create_group("train")
    test = f.create_group("test")
    f.attrs['width'] = round(imW*prop)
    f.attrs['heigth'] = round(imH*prop)
    f.attrs['prop'] = prop

    direction = []
    box = []
    labelPC = []
    labelExpo = []
    labelW = []
    labelP = []
    labelC = []
    image = []
    imagename = []
    with open(os.path.abspath('labels.csv')) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        compteur = 0
        for row in readCSV:
            if not compteur==0:
                direction.append(int(row[6])-1)
                box.append(np.array([float(row[1])/imW, float(row[2])/imH, float(row[3])/imW, float(row[4])/imH]))
                labelExpo.append(float(row[7]))
                path = os.path.normpath(row[0]).split(os.path.sep)
                labelW.append(lW.index(path[1]))
                labelP.append(lP.index(path[2]))
                labelC.append(lC.index(path[3]))
                imagename.append(path[4])
                if int(row[5])>0:
                    labelPC.append(int(row[5])-1)
                else:
                    labelPC.append(lP.index(path[2])*2+lC.index(path[3]))

                image.append(get_image(row[0],round(imW*prop),round(imH*prop),square))

            compteur = compteur+1
            if not compteur%1000:
                print("iteration {}".format(compteur))


    # shuffle
    uniqueLabel = 100*np.array(direction)+10*np.array(labelW)+np.array(labelPC)
    rs = ShuffleSplit(n_splits=1, train_size=0.85, test_size=.15, random_state=27)
    for train_index, test_index in rs.split(np.array(labelW), uniqueLabel):
        train.create_dataset('weather', data=[labelW[i] for i in train_index],compression="gzip", compression_opts=9)
        train.create_dataset('pedestrian', data = [labelP[i] for i in train_index],compression="gzip", compression_opts=9)
        train.create_dataset('clothes', data = [labelC[i] for i in train_index],compression="gzip", compression_opts=9)
        train.create_dataset('pedestrianClothes', data = [labelPC[i] for i in train_index],compression="gzip", compression_opts=9)
        train.create_dataset('direction', data = [direction[i] for i in train_index],compression="gzip", compression_opts=9)
        train.create_dataset('exposition', data = [labelExpo[i] for i in train_index],compression="gzip", compression_opts=9)
        train.create_dataset('boundingBox', data = [box[i] for i in train_index],compression="gzip", compression_opts=9)
        train.create_dataset('images', data = [image[i] for i in train_index],compression="gzip", compression_opts=9)
        train.create_dataset('imagename', data = [imagename[i] for i in train_index],compression="gzip", compression_opts=9)


        test.create_dataset('weather', data = [labelW[i] for i in test_index],compression="gzip", compression_opts=9)
        test.create_dataset('pedestrian', data = [labelP[i] for i in test_index],compression="gzip", compression_opts=9)
        test.create_dataset('clothes', data = [labelC[i] for i in test_index],compression="gzip", compression_opts=9)
        test.create_dataset('pedestrianClothes', data = [labelPC[i] for i in test_index],compression="gzip", compression_opts=9)
        test.create_dataset('direction', data = [direction[i] for i in test_index],compression="gzip", compression_opts=9)
        test.create_dataset('exposition', data = [labelExpo[i] for i in test_index],compression="gzip", compression_opts=9)
        test.create_dataset('boundingBox', data = [box[i] for i in test_index],compression="gzip", compression_opts=9)
        test.create_dataset('images', data = [image[i] for i in test_index],compression="gzip", compression_opts=9)
        test.create_dataset('imagename', data = [imagename[i] for i in test_index],compression="gzip", compression_opts=9)

    return f


def main(args):


    try:
        if args.square==True:
            print('\nI will create file {}, containing images resized at proportion {} and cropped to be squared'.format(args.outputfile,args.prop))
        else:
            print('\nI will create file {}, containing images resized at proportion {} and initial ratio'.format(args.outputfile,args.prop))


        f = h5py.File(args.outputfile,'w')
    except:
        print('\nHey, file {} already exists, I stop here!\n'.format(args.outputfile))
        sys.exit(1)

    f = create(f,args.prop, args.square)
    f.close()
    print('Done, good bye')






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CeremaAWP Parser")
    parser.add_argument('-s', dest='square', action='store_true', help="Requires to crop images to get squares")
    parser.add_argument("-p", dest='prop', default=0.25, help="Proportion of initial size for resizing (default 0.25)")
    parser.add_argument("-o", dest='outputfile', default='CeremaAWP0.25.hdf5', help="Output file (default CeremaAWP0.25.hdf5)")
    args = parser.parse_args()

    main(args)
