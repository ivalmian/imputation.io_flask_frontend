from numpy.random import choice

def make_from_data( data_dict, numeric_fields):
 
    data = dict()

    for key in numeric_fields:

        data[key]=str(choice(list(range(100))))
        data['mask_' + key]=choice(['y','n'])

    for key in data_dict:

        data[key]=choice([-1,0,1])
        data['mask_' + key]=choice(['y','n'])

    return data