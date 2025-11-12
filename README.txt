================================================================================
CSV AUTO-EXPORT SYSTEM
================================================================================

These CSV files are AUTOMATICALLY UPDATED whenever:

1. A user logs in (via /login/)
2. A user rates a movie (via /rate/)

--------------------------------------------------------------------------------
CSV FILES:
--------------------------------------------------------------------------------

statistics.csv
  - Total users, ratings, and average rating
  - Last updated timestamp

all_users.csv
  - Complete user information
  - Login history and rating counts

all_ratings.csv
  - All movie ratings by all users
  - Sorted by most recent first

user_summary.csv
  - Per-user rating statistics
  - Rating distribution (5★, 4★, 3★, 2★, 1★)
  - First and last rating dates

<USERNAME>_ratings.csv (one file per user)
  - Individual user's complete rating history
  - All movies they've rated

--------------------------------------------------------------------------------
AUTO-UPDATE TRIGGERS:
--------------------------------------------------------------------------------

✓ User Login:
  When any user logs in at /login/, all CSV files are regenerated
  with the latest data.

✓ Rating Added/Updated:
  When a user rates a movie at /rate/ or updates an existing rating,
  all CSV files are immediately updated.

--------------------------------------------------------------------------------
MANUAL EXPORT:
--------------------------------------------------------------------------------

To manually export all data at any time:

  python export_to_csv.py

--------------------------------------------------------------------------------
LOCATION:
--------------------------------------------------------------------------------

  C:\Users\bharg\OneDrive\Desktop\SEM-V\BIG DATA\new_code\PROJECT_1\movie-recommendation-system-master\csv_exports\

--------------------------------------------------------------------------------
LAST UPDATED: Automatically on every login or rating event
================================================================================
