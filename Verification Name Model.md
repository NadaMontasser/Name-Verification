# Verification Name Model


### **a. How to build the docker image**
#### 1- Create a Dockerfile:
A Dockerfile is a text file that contains instructions on how to build a Docker image.With the dockerfile we can use base images that have pre-installed dependencies and code.

The bolw code clarifiy how we bild the dockerfile:
```
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY  ./ ./
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0" ]
```
#### 2- Build the Docker image:
After creating the dockerfile, we can build the docker image by using the following command in the same path.
```
docker build -t img_name .
```
To check the image, use the following command to see a list of all docker images.
```
docker images
```
**Note:** The **(.)** is required to specified the directory hold the dockerfile and any files 
 
 To run and startup the container based on the built image, we used the following command.
 ``` 
 docker run img_name
 ```

### **b. How to test your solution**
To test the solution, we used a collection of random test cases that include real and fake names, these names collected before data generation to verify the solution.

Here, some case the model succed to detect the between hig and low confidence:
نجيب مغيث سمير  is a real name with high confidence

باسمم1 وحيد السيد is a real name with low confidence

منة الله صلاح الدين محمد  is a real name with high confidence

باسمم وحد السد is a real name with low confidence

باسم وحيد السيد  is a real name with high confidence

ضائ غلي وسمي is a real name with low confidence 

حميل سوفي جملل is a real name with low confidence

محمود يحيي احمد  is a real name with high confidence

### **c. How to verify the result you claim**
After using test cases sometimes the model can classify the name correctly and some time failed to classify it, but overalll we can say the model cav verify and classify the name correct name or incorrect.


باسمم1 وحةد السد is a real name with low confidence 

هدي يوسف كمال  is a real name with high confidence

خدي ويسف كملج is a real name with low confidence 

يره عبحميد وسن  is a real name with low confidence














