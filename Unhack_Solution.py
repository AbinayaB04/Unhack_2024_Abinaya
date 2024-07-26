import csv
# Loading care areas from the csv file
def load_care_areas(filename):
    care_areas=[]
    with open(filename,newline='') as csvfile:
        reader=csv.reader(csvfile)  
        for row in reader:
            care_areas.append({
                'id':int(row[0]),
                'x1':float(row[1]),
                'x2':float(row[2]),
                'y1':float(row[3]),
                'y2':float(row[4])
            })
    return care_areas
# Loading metadata from csv file
def load_meta_data(filename):
    with open(filename,newline='') as csvfile:
        reader=csv.DictReader(csvfile)
        headers=reader.fieldnames
        metadata=next(reader)
        try:
            main_field_size=float(metadata['Main Field Size'])
            sub_field_size=float(metadata['Sub Field size'])
        except KeyError as e:
            print(f"Missing expected header: {e}")
            raise
    return main_field_size,sub_field_size

def write_main_field(filename,main_field):
    with open(filename, 'w', newline='') as csvfile:
        field_names=['id','x1','x2','y1','y2']
        writer = csv.DictWriter(csvfile,fieldnames=field_names)
        for main_field1 in main_field:
            writer.writerow(main_field1)
# Here generation of main fields happens using care areas and main field size
def generate_main_field(care_areas,main_field_size):
    main_field=[]
    field_id=0
    for care_area in care_areas:
        x1=care_area['x1']
        while x1<care_area['x2']:
            y1=care_area['y1']
            while y1<care_area['y2']:
                main_field.append({
                    'id':field_id,
                    'x1':x1,
                    'x2':min(x1+main_field_size,care_area['x2']),
                    'y1':y1,
                    'y2':min(y1+main_field_size,care_area['y2'])
                })
                field_id+=1
                y1+=main_field_size
            x1+=main_field_size
    return main_field
# Generation of  sub-fields happens using the main fields and subfield size
def generate_sub_fields(main_fields, sub_field_size):
    sub_fields=[]
    sub_field_id=0
    for main_field in main_fields:
        x_start=main_field['x1']
        while x_start<main_field['x2']:
            y_start=main_field['y1']
            while y_start<main_field['y2']:
                sub_fields.append({
                    'id':sub_field_id,
                    'x1':x_start,
                    'x2':min(x_start+sub_field_size,main_field['x2']),
                    'y1':y_start,
                    'y2':min(y_start+sub_field_size,main_field['y2']),
                    'main_id':main_field['id']
                })
                sub_field_id+=1
                y_start+=sub_field_size
            x_start+=sub_field_size
    return sub_fields

def write_sub_field(filename, sub_field):
    with open(filename,'w',newline='') as csvfile:
        field_names=['id','x1','x2','y1','y2','main_id']
        writer=csv.DictWriter(csvfile, fieldnames=field_names)
        for sub_field1 in sub_field:
            writer.writerow(sub_field1)
main_field_size, sub_field_size = load_meta_data("D:/KLA-2024/pb1/metadata.csv")
care_areas = load_care_areas("D:/KLA-2024/pb1/CareAreas.csv")
main_fields = generate_main_field(care_areas, main_field_size)
sub_fields = generate_sub_fields(main_fields, sub_field_size)
write_main_field("D:/KLA-2024/pb1/MainField.csv", main_fields)
write_sub_field("D:/KLA-2024/pb1/SubField.csv", sub_fields)

