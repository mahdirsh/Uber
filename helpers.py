import math


def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371  
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c * 1000
    return round(distance, 2)


def find_nearest_drivers(customer_location, drivers, max_distance=2000):
    
    drivers_with_distance = []
    for driver in drivers:
        driver_location = (driver.location_latitude, driver.location_longitude)
        distance = calculate_distance(
            customer_location[0], customer_location[1],
            driver_location[0], driver_location[1]
        )
        if distance <= max_distance:
            drivers_with_distance.append((driver, distance))

    drivers_with_distance.sort(key=lambda x: x[1]) 
    
    nearest_drivers = []
    for driver, distance in drivers_with_distance:
        driver.distance_to_start_location = distance 
        nearest_drivers.append(driver)

    return nearest_drivers
    