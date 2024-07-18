import pickle
with open(r"obj_camera.pickle", "rb") as input_file:
     e = pickle.load(input_file)
print(e)