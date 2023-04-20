import os
import boto3
import random, json

s3 = boto3.client('s3')

# -------for creating the bucket in s3-----------
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

# response = s3.create_bucket(
#     ACL='private',  
#     Bucket='examplebucket',
#     CreateBucketConfiguration={
#         'LocationConstraint': 'eu-west-1',
#     },
# )


# default spot size as mentioned in the problem
spot_size = 96


class Parking_lot():
    
    def __init__(self, square_ft_size):
        self.sq_ft_size = square_ft_size
        self.cars_to_park = square_ft_size//spot_size
        self.parking = []

        for sp in range(1, self.cars_to_park + 1):
            self.parking.append({'spot' : sp, 'car' : ''})
    

    def create_and_upload_file_to_s3(self, _parking_lot):
        data = json.dumps(_parking_lot)
        filename = 'parking_lot_data.json'
        # creating a json file
        with open(filename, 'w') as fp:
            fp.write(data)
        
        file_path = os.path.join(os.getcwd(), filename)
        # uploading file to s3 bucket
        ## Please change the bucket name to your one.
        s3.upload_file(file_path, 'ballu-bucket-1', filename)
        
    


class Car():

    def __init__(self):
        self.parking_lot = []

    def magic(self, license_plate):
        self.license_plate = None
        if len(license_plate) == 7:
            self.license_plate = license_plate
            return True
        else:
            return False

    def park(self, parking_lot, spot):
        self.parking_lot = parking_lot
        for parked in self.parking_lot:
            if parked['spot'] == spot:
                if not parked['car']:
                    parked['car'] = self.license_plate
                    print('the car was parked successfully')
                    print(f'Car with license plate {self.license_plate} parked successfully in spot {spot}.\n')
                    return True
                else:
                    print('the car was not parked successfully - Already Occupied')
                    print(f'Car with license plate {self.license_plate} not parked successfully in spot {spot}.\n')
                    return False
    
    def check_parkinglot(self):
        for park in self.parking_lot:
            if not park['car']:
                break
        else:
            return True

        return False


if __name__ == '__main__':
    # num_cars = int(input('Enter number of cars you want to park : '))
    # cars = []
    # for ind in range(num_cars):
    #     data = input("Enter 7-digit lincense plate of car : ")
    #     cars.append(data)

    # parking_area_size = int(input('Enter the parking lot of size : '))



    # To take input fromthe user than refer to above commented code
    cars = [
        'AAD5532',
        'AAD1111',
        'AAD22222',
        'AAD3333',
        'AAD4444',
        'AAD5555',
        'AAD66666',
        'AAD7777',
        'AAD8888',
        'AAD9999',
        'AAD8989',
        'AAD5533',
        'AAD1234',
    ]

    parking_area_size = 1000

    p = Parking_lot(parking_area_size)
    car = Car()

    while len(cars) > 0:
        random_spot = random.randint(1, p.cars_to_park)

        if not car.magic(cars[0]):
            print(f"Car with license plate {cars[0]} not parked successfully in spot {random_spot} - Liccense Plate digit must be 7.\n")
            cars.pop(0)
            continue

        result = car.park(p.parking, random_spot)
        if not result:
            continue

        if car.check_parkinglot():
            print('parking lot is full')
            break

        cars.pop(0)
    
    # uplaoding to s3 bucket
    p.create_and_upload_file_to_s3(car.parking_lot)
