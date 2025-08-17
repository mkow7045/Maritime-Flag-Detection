import os
import random
from PIL import Image
from PIL import ImageChops
import json


class FlagPaster:
    def __init__(self):
        self.current_flag = 0
        self.current_image = 1
        self.cwd = os.getcwd()
        self.flags_folder = os.path.join(self.cwd, "flags")
        self.sea_images_folder = os.path.join(self.cwd, "sea")
        self.flag_image_paths = os.listdir(self.flags_folder)
        self.sea_image_paths = os.listdir(self.sea_images_folder)

        self.coco_output = {
            "images": [],
            "annotations": [],
            "categories": [
                {"id": 1, "name": "alfa"},
                {"id": 2, "name": "bravo"},
                {"id": 3, "name": "charlie"},
                {"id": 4, "name": "delta"},
                {"id": 5, "name": "echo"},
                {"id": 6, "name": "foxtrot"},
                {"id": 7, "name": "golf"},
                {"id": 8, "name": "hotel"},
                {"id": 9, "name": "india"},
                {"id": 10, "name": "juliett"},
                {"id": 11, "name": "kilo"},
                {"id": 12, "name": "lima"},
                {"id": 13, "name": "mike"},
                {"id": 14, "name": "november"},
                {"id": 15, "name": "oscar"},
                {"id": 16, "name": "papa"},
                {"id": 17, "name": "quebec"},
                {"id": 18, "name": "romeo"},
                {"id": 19, "name": "sierra"},
                {"id": 20, "name": "tango"},
                {"id": 21, "name": "uniform"},
                {"id": 22, "name": "victor"},
                {"id": 23, "name": "whiskey"},
                {"id": 24, "name": "xray"},
                {"id": 25, "name": "yankee"},
                {"id": 26, "name": "zulu"}
            ]
        }
        self.annotation_id = 1

        random.seed(42)
    
        random.shuffle(self.flag_image_paths)

    def trim_image(self,image):
        rgba = image.convert("RGBA")
        datas = rgba.getdata()
            
        newData = []
        for item in datas:
            if item[0] < 20 and item[1] < 20 and item[2] < 20:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        
        rgba.putdata(newData)

        bbox = rgba.getbbox()

        if bbox:
            return image.crop(bbox)
        else:
            return image
    
    def add_flags_to_image(self,num_of_flags):
        background = Image.open(os.path.join(self.sea_images_folder, self.sea_image_paths[random.randrange(0, len(self.sea_image_paths))]))
        for i in range(num_of_flags):
            flag = Image.open(os.path.join(self.flags_folder,self.flag_image_paths[self.current_flag]))
            
            flag = self.trim_image(flag)

            resize_amount = random.uniform(1, 7)
            new_size = (int(flag.width * resize_amount), int(flag.height * resize_amount))
            flag = flag.resize(new_size, Image.LANCZOS)

            width, height = background.size
            width_flag, height_flag = flag.size
            width_offset = random.randrange(0, width - width_flag)
            height_offset = random.randrange(0,height-height_flag)

            if flag.mode != 'RGBA':
                flag = flag.convert('RGBA')

            background.paste(flag, (width_offset,height_offset),flag)
            flagLetter = self.flag_image_paths[self.current_flag][0]
            flagCategory = ord(flagLetter.upper()) - ord('A') + 1

            annotation = {
                "id": self.annotation_id,
                "image_id": self.current_image,
                "category_id": flagCategory,
                "bbox": [width_offset,height_offset,width_flag,height_flag],
                "area": width_flag * height_flag,
                "iscrowd": 0,
                "segmentation": [[
                    width_offset, height_offset,
                    width_offset + width_flag, height_offset,
                    width_offset + width_flag, height_offset + height_flag,
                    width_offset, height_offset + height_flag
                ]]
            }
            self.coco_output["annotations"].append(annotation)
            self.annotation_id += 1


            self.current_flag = self.current_flag + 1
            output_path = os.path.join(self.cwd, "compositions", f"output_{self.current_image}.png")

        if(num_of_flags == 0):
            output_path = os.path.join(self.cwd, "compositions", f"output_{self.current_image}.png")
        
        background = background.resize((1920,1440), Image.LANCZOS)
        background.save(output_path)
        image_info = {
            "id": self.current_image,
            "file_name": f"output_{self.current_image}.png",
            "width": 1920,
            "height": 1440
        }
        self.coco_output["images"].append(image_info)
        self.current_image += 1




def main():
    paster = FlagPaster()
    for i in range(1000):
        flag_number = random.randrange(0, 10)
        if(paster.current_flag + flag_number <= len(paster.flag_image_paths)):
            paster.add_flags_to_image(flag_number)
        else:
            paster.add_flags_to_image(len(paster.flag_image_paths) - paster.current_flag)
            break
    
    with open('annotations.json', 'w') as f:
        json.dump(paster.coco_output, f, indent=4)
        
if __name__ == "__main__":
    main()