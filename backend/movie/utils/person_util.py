
# get the name of gender of the given integer
# gender: 0->unknow, 2->male, 1->female, 3->LGBT
def get_gender(gender):
  gender_dict = ["unknown", 'male', 'female', 'LGBT']
  return gender_dict[gender]