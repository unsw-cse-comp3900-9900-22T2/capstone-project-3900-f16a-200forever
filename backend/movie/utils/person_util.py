

def get_gender(gender):
  # gender: 0->unknow, 2->male, 1->female, 3->LGBT
  gender_dict = ["unknown", 'male', 'female', 'LGBT']
  return gender_dict[gender]