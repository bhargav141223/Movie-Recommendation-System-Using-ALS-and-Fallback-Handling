"""
Export all user and rating data to CSV files.
Run: python export_to_csv.py
Output: Multiple CSV files in csv_exports/ folder
"""
import os
import django
import csv
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_recommendation.settings')
django.setup()

from django.contrib.auth.models import User
from recommender.models import Rating, PosterCache
from django.db.models import Count, Avg

def export_to_csv():
    # Create output directory
    output_dir = 'csv_exports'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Exporting data to CSV files in '{output_dir}/' folder...")
    
    # File 1: Statistics
    stats_file = os.path.join(output_dir, '1_statistics.csv')
    with open(stats_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Users', User.objects.count()])
        writer.writerow(['Total Ratings', Rating.objects.count()])
        writer.writerow(['Cached Posters', PosterCache.objects.count()])
        avg_rating = Rating.objects.aggregate(avg=Avg('rating'))['avg']
        writer.writerow(['Average Rating', round(avg_rating, 2) if avg_rating else 0])
        writer.writerow(['Export Date', datetime.now().strftime('%Y-%m-%d')])
        writer.writerow(['Export Time', datetime.now().strftime('%H:%M:%S')])
    print(f"  [OK] {stats_file}")
    
    # File 2: Users
    users_file = os.path.join(output_dir, '2_users.csv')
    users = User.objects.all()
    with open(users_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['User ID', 'Username', 'Email', 'First Name', 'Last Name', 
                        'Is Active', 'Is Staff', 'Is Superuser', 'Date Joined', 
                        'Last Login', 'Total Ratings'])
        for user in users:
            date_joined = user.date_joined.replace(tzinfo=None) if user.date_joined else ''
            last_login = user.last_login.replace(tzinfo=None) if user.last_login else ''
            writer.writerow([
                user.id,
                user.username,
                user.email or 'N/A',
                user.first_name or 'N/A',
                user.last_name or 'N/A',
                user.is_active,
                user.is_staff,
                user.is_superuser,
                date_joined,
                last_login,
                Rating.objects.filter(user=user).count()
            ])
    print(f"  [OK] {users_file}")
    
    # File 3: All Ratings
    ratings_file = os.path.join(output_dir, '3_all_ratings.csv')
    ratings = Rating.objects.select_related('user').all().order_by('-updated_at')
    with open(ratings_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rating ID', 'User ID', 'Username', 'Movie ID', 'Movie Title', 
                        'Rating (Stars)', 'Created At', 'Updated At'])
        for rating in ratings:
            created_at = rating.created_at.replace(tzinfo=None) if rating.created_at else ''
            updated_at = rating.updated_at.replace(tzinfo=None) if rating.updated_at else ''
            writer.writerow([
                rating.id,
                rating.user.id,
                rating.user.username,
                rating.movie_id,
                rating.movie_title,
                rating.rating,
                created_at,
                updated_at
            ])
    print(f"  [OK] {ratings_file}")
    
    # File 4: User Summary
    summary_file = os.path.join(output_dir, '4_user_summary.csv')
    with open(summary_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['User ID', 'Username', 'Total Ratings', 'Average Rating',
                        '5 Stars', '4 Stars', '3 Stars', '2 Stars', '1 Star',
                        'First Rating', 'Last Rating'])
        for user in users:
            user_ratings = Rating.objects.filter(user=user)
            if user_ratings.exists():
                first_rating = user_ratings.order_by('created_at').first()
                last_rating = user_ratings.order_by('-updated_at').first()
                first_created = first_rating.created_at.replace(tzinfo=None) if first_rating.created_at else ''
                last_updated = last_rating.updated_at.replace(tzinfo=None) if last_rating.updated_at else ''
                
                writer.writerow([
                    user.id,
                    user.username,
                    user_ratings.count(),
                    round(user_ratings.aggregate(avg=Avg('rating'))['avg'], 2),
                    user_ratings.filter(rating=5).count(),
                    user_ratings.filter(rating=4).count(),
                    user_ratings.filter(rating=3).count(),
                    user_ratings.filter(rating=2).count(),
                    user_ratings.filter(rating=1).count(),
                    first_created,
                    last_updated
                ])
    print(f"  [OK] {summary_file}")
    
    # File 5: Individual user files
    for user in users:
        user_ratings = Rating.objects.filter(user=user).order_by('-updated_at')
        if user_ratings.exists():
            user_file = os.path.join(output_dir, f'5_{user.username}_ratings.csv')
            with open(user_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Movie Title', 'Movie ID', 'Rating', 'Rated On', 'First Rated'])
                for rating in user_ratings:
                    updated_at = rating.updated_at.replace(tzinfo=None) if rating.updated_at else ''
                    created_at = rating.created_at.replace(tzinfo=None) if rating.created_at else ''
                    writer.writerow([
                        rating.movie_title,
                        rating.movie_id,
                        rating.rating,
                        updated_at,
                        created_at
                    ])
            print(f"  [OK] {user_file}")
    
    # File 6: Top Rated Movies
    top_movies_file = os.path.join(output_dir, '6_top_rated_movies.csv')
    movie_stats = Rating.objects.values('movie_id', 'movie_title').annotate(
        rating_count=Count('id'),
        avg_rating=Avg('rating')
    ).order_by('-rating_count', '-avg_rating')[:50]
    
    with open(top_movies_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Movie ID', 'Movie Title', 'Number of Ratings', 'Average Rating'])
        for movie in movie_stats:
            writer.writerow([
                movie['movie_id'],
                movie['movie_title'],
                movie['rating_count'],
                round(movie['avg_rating'], 2)
            ])
    print(f"  [OK] {top_movies_file}")
    
    print(f"\n[SUCCESS] All CSV files exported to: {os.path.abspath(output_dir)}")
    return output_dir

def display_csv_data(output_dir):
    print("\n" + "="*80)
    print("CSV FILES CREATED")
    print("="*80)
    
    import glob
    csv_files = sorted(glob.glob(os.path.join(output_dir, '*.csv')))
    
    for csv_file in csv_files:
        print(f"\n--- {os.path.basename(csv_file)} ---")
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            # Show header and first 5 data rows
            for i, row in enumerate(rows[:6]):
                print('  ' + ' | '.join(str(cell)[:30] for cell in row))
            if len(rows) > 6:
                print(f"  ... ({len(rows) - 1} total rows)")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("EXPORTING USER DATA TO CSV")
    print("="*80 + "\n")
    
    try:
        output_dir = export_to_csv()
        display_csv_data(output_dir)
        print("\n" + "="*80)
        print(f"[SUCCESS] All data exported to CSV files!")
        print(f"Location: {os.path.abspath(output_dir)}")
        print("="*80 + "\n")
    except Exception as e:
        print(f"\n[ERROR] Error during export: {e}")
        import traceback
        traceback.print_exc()
