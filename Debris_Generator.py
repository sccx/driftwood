import pandas as pd
import random
import time


class DebrisGenerator:
    """
        Create debris objects of variable dimensions to feed into the simulation.
    """

    def select_wood_type(self):
        '''
            Generate a random wood type and associated density (in kg/m**3), 1 kg/m3 = 0.001 g/cm3
            Returns: wood type, density
        '''
        wood_types = {'chestnut': 560,
                      'elm': random.randint(550, 820),
                      'pine': random.randint(350, 670),
                      'oak': random.randint(740, 770)
                      } 
        wood_type, density = random.choice(list(wood_types.items()))
        return wood_type, density

    def generate(self, number_of_objects):
        '''
            Create debris objects of variable dimensions to feed into the simulation.
            Returns: debris object dict
        '''
        object_dict = {}
        i = 1
        while i <= number_of_objects:
            # Generate data for the object
            #random_obj_dims = [random.randint(10, 300) / 100,
            #                   random.randint(10, 300) / 100,
            #                   random.randint(10, 300) / 100] # Expressed in meters
            random_obj_dims = [1,1,1]            
            start_time = time.asctime()
            wood_type = self.select_wood_type()
            obj_density = wood_type[1]
            length = max(random_obj_dims)
            width = sorted(random_obj_dims)[1]
            height = min(random_obj_dims)
            volume = length * width * height

            mass = round(volume * obj_density, 3)
            height_below_water = (obj_density / 1024) * height # 1024 is the mass density of salt water

            ref_area1_air = (height - height_below_water) * length
            ref_area1_water = height_below_water * width
            ref_area2_air = (height - height_below_water) * width
            ref_area2_water = height_below_water * length

            reference_areas = [round(ref_area1_air, 3),
                               round(ref_area1_water, 3),
                               round(ref_area2_air, 3),
                               round(ref_area2_water, 3)
                               ]

            # Physical parameters of object in (and out of) water
            area_over_water = ref_area1_air
            area_under_water = ref_area1_water
            immersion_ratio = area_over_water / (area_over_water + area_under_water)

            # Create the dictionary key and entries
            key = i

            # Define the qualities that are stored within the object dictionary
            object_dict[key] = start_time, wood_type, random_obj_dims, volume, mass, \
                reference_areas, immersion_ratio, obj_density
            i += 1
        return object_dict


dg = DebrisGenerator()
debris = dg.generate(1)
debris_df = pd.DataFrame.from_dict(debris)
debris_df = debris_df.rename(index={0: 'Start Time',
                                    1: "Wood Type/Density",
                                    2: "Dimensions",
                                    3: "Volume",
                                    4: "Mass",
                                    5: "Reference Areas",
                                    6: "Immersion Ratio",
                                    7: "Obj_Density"
                                    })

print(debris_df)
'''
with open('debris.txt', 'w') as data:
    data.write(str(debris))
'''


'''
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(
        description='Creates debris objects of variable dimensions to feed into the drift simulation.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    p.add_argument('-n', '--number', help='Number of debris objects.', default=1, action='store')
    p.add_argument('-o', '--output', help='Output filename.', action='store', required=True)
    args = p.parse_args()

    dg = DebrisGenerator()

    if args.number and args.output:
        fn = args.output
        debris = dg.generate(args.number)

        debris_df = pd.DataFrame.from_dict(debris)
        debris_df = debris_df.rename(index={0: 'Start Time',
                                            1: "Wood Type/Density",
                                            2: "Dimensions",
                                            3: "Volume",
                                            4: "Mass",
                                            5: "Reference Areas",
                                            6: "Immersion Ratio",
                                            7: "Obj_Density"
                                            })
        if '.txt' in fn:
            fn = re.sub('.txt', '', fn)

        with open(f'{fn}.txt', 'w') as data:
            data.write(str(debris))

        for d in debris:
            d_list = "\n".join([str(o) for o in debris[d]])
            print(f'\n{d}: \n{d_list}')
'''