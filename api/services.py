from django.utils import timezone

def calculate_average_rating(truck, new_rating):
    review_count = truck.truckrating_set.count()
    current_average_rating = truck.average_rating

    # Check if truck has been rated yet, if not, just set the new rating to the average
    if current_average_rating == -1:
        new_average_rating = new_rating
    else:
        new_average_rating = (current_average_rating * review_count + new_rating) / (review_count + 1)

    return new_average_rating


def get_current_truck_location(truck, time=timezone.now()):
    """
    :param truck:
    :param time:
    :return coordinates:

    Returns coordinates if the truck is open at the given time.

    Otherwise it returns nothing
    """

    for post in truck.posts.all():
        if post.start_time <= time <= post.end_time:
            return {
                'latitude': post.latitude,
                'longitude': post.longitude
            }

    return None
