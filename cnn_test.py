import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from keras.utils import to_categorical
from keras.datasets import cifar10
import warnings
warnings.filterwarnings("ignore", message="Do not pass an `input_shape`/`input_dim` argument to a layer.")

# C:\Users\91948\PycharmProjects\datascience_projects\Scripts\pip.exe list --outdated
# C:\Users\91948\PycharmProjects\datascience_projects\Scripts\python.exe -m pip install --upgrade pip

# Load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

classification=["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]


# one-hot encode labels
y_train_onehot = to_categorical(y_train)
y_test_onehot = to_categorical(y_test)
x_train = x_train / 255
x_test = x_test / 255

# create a model architecture
model = Sequential()

# first convolutional layer
model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(32, 32, 3)))

# pooling layer
model.add(MaxPool2D(pool_size=(2, 2)))

# second convolutional layer
model.add(Conv2D(32, (5, 5), activation='relu'))

# pooling layer
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Flatten())

# add a dense layer
model.add(Dense(1000, activation='relu'))

# add a dropout layer
model.add(Dropout(0.5))

# add a dense layer
model.add(Dense(250, activation='relu'))

# output layer
model.add(Dense(10, activation='softmax'))

# print model summary
model.summary()

model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

# train the model
history = model.fit(x_train, y_train_onehot, batch_size=256, epochs=20, validation_split=0.2)

# evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test_onehot)
# print("Test accuracy:", test_acc)

# display a dog image
dog_image = plt.imread("dog.jpg")
# img=plt.imshow(dog_image)
# plt.axis('off')
# plt.show(img)
# from  skimage import transform
# resize=transform.resize(dog_image(32,32,3))
# plt.axis('off')
# img=plt.imshow(resize)
# prediction=model.predict(np.array(resize))
# print(prediction)
from skimage import transform

# Resize the dog image
resize = transform.resize(dog_image, (32,32,3))  # Fix the resize function call
plt.axis('off')
img = plt.imshow(resize)
prediction = model.predict(np.array([resize]))  # Make sure to pass the image as an array

list_index=[0,1,2,3,4,5,6,7,8,9]
x=prediction
# for i in range(10):
#     for j in range(10):
#         if x[10][[list_index][i]]>x[0][[list_index][j]]:
#             temp=list_index[i]
#             list_index[i]=list_index[j]
#             list_index[j]=temp
for i in range(len(list_index)):
    for j in range(len(list_index)):
        if x[0][list_index[i]] > x[0][list_index[j]]:  # Update this line
            temp = list_index[i]
            list_index[i] = list_index[j]
            list_index[j] = temp


# print(list_index)
for i in range(1):
    print("the predictive picture is a ",classification[list_index[i]])