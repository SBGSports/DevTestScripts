#!/usr/bin/env python3
import sys
import os
import xml.etree.ElementTree as ET
import base64

def main() -> int:
    """given an input folder, find all the squish verifcation point xmls, parse out the image and deposit them in the output folder (mimicing the path under input folder)"""
    if len(sys.argv) <= 2:
        print("Expected two inputs: {input dir} {output dir}")
        return 1

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if(input_dir[-1] != os.path.sep):
        input_dir = "{0}{1}".format(input_dir, os.path.sep)

    if(input_dir[-1] != os.path.sep):
        output_dir = "{0}{1}".format(output_dir, os.path.sep)


    for subdir, dirs, files in os.walk(input_dir):
        destination_dir = output_dir
        destination_dir = os.path.join(destination_dir, subdir[len(input_dir):])

        if not os.path.isdir(destination_dir):
            os.mkdir(destination_dir)
            #print("created: {}".format(destination_dir))

        for file in files:
            cur_file = os.path.join(subdir, file)
            xml_tree = ET.parse(cur_file)
            xml_root = xml_tree.getroot()
            for child in xml_root:
                if child.tag != "Verification":
                    continue
                output_data = base64.b64decode(child.text)
                png_file = "{0}.{1}".format(file, "png")
                destination_file = os.path.join(destination_dir, png_file)
                bak_file = ""
                if os.path.isfile(destination_file):
                    bak_file = "{0}.bak".format(destination_file)
                    os.rename(destination_file, bak_file)

                with open(destination_file, "wb") as output_file:
                    output_file.write(output_data)
                #print("wrote: {}".format(destination_file))
                print('.', end='')
                sys.stdout.flush()
                try:
                    if len(bak_file) > 0:
                        os.unlink(bak_file)
                        #print("deleted: {0}".format(bak_file))
                except:
                    #print("delete of old file failed, ignoring")
                    pass
    print('')
    print("Images successfully extracted to: {}".format(output_dir))
    return 0


if __name__ == '__main__':
    sys.exit(main())
