"""
Quick script to display user login and rating data from the Django database.
Run: python show_user_data.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_recommendation.settings')
django.setup()

from django.contrib.auth.models import User
from recommender.models import Rating, PosterCache

def show_all_users():
    print("\n" + "="*80)
    print("ALL USERS (Login Data)")
    print("="*80)
    users = User.objects.all()
    if not users:
        print("No users found in database.")
        return
    
    for user in users:
        print(f"\nUser ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"First Name: {user.first_name}")
        print(f"Last Name: {user.last_name}")
        print(f"Is Active: {user.is_active}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Date Joined: {user.date_joined}")
        print(f"Last Login: {user.last_login}")
        print("-" * 80)

def show_all_ratings():
    print("\n" + "="*80)
    print("ALL RATINGS (User Rating Data)")
    print("="*80)
    ratings = Rating.objects.select_related('user').all().order_by('-updated_at')
    if not ratings:
        print("No ratings found in database.")
        return
    
    for rating in ratings:
        print(f"\nRating ID: {rating.id}")
        print(f"User: {rating.user.username} (ID: {rating.user.id})")
        print(f"Movie ID: {rating.movie_id}")
        print(f"Movie Title: {rating.movie_title}")
        print(f"Rating: {rating.rating}/5 stars")
        print(f"Created At: {rating.created_at}")
        print(f"Updated At: {rating.updated_at}")
        print("-" * 80)

def show_user_profile(username):
    print("\n" + "="*80)
    print(f"USER PROFILE: {username}")
    print("="*80)
    try:
        user = User.objects.get(username=username)
        print(f"\nUser ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Full Name: {user.first_name} {user.last_name}")
        print(f"Date Joined: {user.date_joined}")
        print(f"Last Login: {user.last_login}")
        
        # Get user's ratings
        user_ratings = Rating.objects.filter(user=user).order_by('-updated_at')
        print(f"\nTotal Ratings: {user_ratings.count()}")
        
        if user_ratings.exists():
            print("\nRating History:")
            for idx, rating in enumerate(user_ratings, 1):
                print(f"  {idx}. {rating.movie_title} - {rating.rating}★ (Rated: {rating.updated_at.strftime('%Y-%m-%d %H:%M')})")
        else:
            print("  No ratings yet.")
            
    except User.DoesNotExist:
        print(f"User '{username}' not found.")

def show_statistics():
    print("\n" + "="*80)
    print("DATABASE STATISTICS")
    print("="*80)
    user_count = User.objects.count()
    rating_count = Rating.objects.count()
    poster_cache_count = PosterCache.objects.count()
    
    print(f"\nTotal Users: {user_count}")
    print(f"Total Ratings: {rating_count}")
    print(f"Cached Posters: {poster_cache_count}")
    
    if rating_count > 0:
        avg_rating = Rating.objects.aggregate(avg=django.db.models.Avg('rating'))['avg']
        print(f"Average Rating: {avg_rating:.2f}/5 stars")
        
        # Most active user
        from django.db.models import Count
        top_user = User.objects.annotate(num_ratings=Count('rating')).order_by('-num_ratings').first()
        if top_user:
            print(f"Most Active User: {top_user.username} ({top_user.rating_set.count()} ratings)")
    
    print("-" * 80)

if __name__ == "__main__":
    print("\n" + "#"*80)
    print("# MOVIE RECOMMENDATION SYSTEM - USER DATA VIEWER")
    print("#"*80)
    
    show_statistics()
    show_all_users()
    show_all_ratings()
    
    print("\n" + "="*80)
    print("To view a specific user profile, run:")
    print("  from show_user_data import show_user_profile")
    print("  show_user_profile('username')")
    print("="*80 + "\n")
