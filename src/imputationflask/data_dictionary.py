'''
imputationflask.data_dictionary
-------------------
Provides a data dictionary for discrete values
'''

from collections import OrderedDict

data_dict = {'COW': {0: 'For profit',
                     1: 'Non-profit',
                     2: 'Self-employed',
                     3: 'Government',
                     4: 'Unemployed',

                     },
             'MAR': {0: 'Single', 1: 'Divorced/Separated', 2: 'Married', 3: 'Widowed'},
             'SCH': {0: 'Public', 1: 'Private', 2: 'No'},
             'SCHL': {
    0: 'No highschool',
    1: 'GED',
    2: 'Highschool',
    3: 'Some college',
    4: "Associate's",
    5: "Bachelor's",
    6: "Master's",
    7: 'Professional degree',
    8: 'Doctorate',
},
    'SEX': {1: 'Male',
            2: 'Female'},
    'HICOV': {1: 'With health insurance',
              2: 'No health insurance'},
    'RAC1P': {

    1: 'White',
    2: 'Black',
    3: 'Asian',
    4: 'Native American',
    5: 'Pacific Islander',
    6: 'Two or more',
    7: 'Other'}

}

data_dict_inv = {k: {k2: k1 for k1, k2 in v.items()}
                 for k, v in data_dict.items()}
