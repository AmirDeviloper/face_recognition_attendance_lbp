import os
import shutil
import random
from pathlib import Path
from settings import TRAIN_DATASET_PATH, TEST_DATASET_PATH

names = {
    's1': 'John Smith',
    's2': 'Emma Johnson',
    's3': 'Michael Williams',
    's4': 'Sophia Brown',
    's5': 'David Jones',
    's6': 'Olivia Garcia',
    's7': 'Daniel Miller',
    's8': 'Ava Davis',
    's9': 'James Rodriguez',
    's10': 'Isabella Martinez',
    's11': 'Robert Hernandez',
    's12': 'Mia Lopez',
    's13': 'William Gonzalez',
    's14': 'Charlotte Wilson',
    's15': 'Joseph Anderson',
    's16': 'Amelia Thomas',
    's17': 'Charles Taylor',
    's18': 'Harper Moore',
    's19': 'Thomas Jackson',
    's20': 'Evelyn Martin',
    's21': 'Christopher Lee',
    's22': 'Abigail Perez',
    's23': 'Matthew Thompson',
    's24': 'Emily White',
    's25': 'Anthony Harris',
    's26': 'Elizabeth Sanchez',
    's27': 'Mark Clark',
    's28': 'Sofia Ramirez',
    's29': 'Donald Lewis',
    's30': 'Avery Robinson',
    's31': 'Steven Walker',
    's32': 'Ella Young',
    's33': 'Paul Allen',
    's34': 'Scarlett King',
    's35': 'Kevin Wright',
    's36': 'Grace Scott',
    's37': 'George Torres',
    's38': 'Chloe Nguyen',
    's39': 'Kenneth Hill',
    's40': 'Victoria Flores'
}


def create_dataset_structure():
    
    dataset_path = r"Olivetti_Dataset"
    
    os.makedirs(TRAIN_DATASET_PATH, exist_ok=True)
    os.makedirs(TEST_DATASET_PATH, exist_ok=True)
    

    if not os.path.exists(dataset_path):
        print(f"error '{dataset_path}' not found!")
        return
    
    for i in range(1, 41):
        folder_name = f"s{i}"
        person_name = names[folder_name]
        
        print(f"\nprocessing {folder_name} - [{person_name}]")
        
        source_folder = os.path.join(dataset_path, folder_name)
        
        if not os.path.exists(source_folder):
            print(f"folder not found {folder_name}!")
            continue
        
        pgm_files = [f for f in os.listdir(source_folder) if f.lower().endswith('.pgm')]
        
        if len(pgm_files) < 10:
            print(f"folder {folder_name} just have {len(pgm_files)} files. [must have 10]")
            continue
        
        random.shuffle(pgm_files)
        train_files = pgm_files[:8]
        test_files = pgm_files[8:]
        
        new_person_folder = os.path.join(TRAIN_DATASET_PATH, person_name.replace(" ", "_"))
        os.makedirs(new_person_folder, exist_ok=True)
        
        for file_name in train_files:
            source_file = os.path.join(source_folder, file_name)
            dest_file = os.path.join(new_person_folder, file_name)
            shutil.copy2(source_file, dest_file)
        
        print(f"train files go to: {new_person_folder}")
        
        for j, file_name in enumerate(test_files, 1):
            source_file = os.path.join(source_folder, file_name)
            
            random_num = random.randint(10000, 99999)
            new_file_name = f"{person_name.replace(' ', '_')}-{random_num}.pgm"
            dest_file = os.path.join(TEST_DATASET_PATH, new_file_name)
            
            shutil.copy2(source_file, dest_file)
            

        print(f"train files go to: {dest_file.split('-')[0]}")

    
    print("\n" + "=" * 60)
    print("complete!")
    print("=" * 60)
    
