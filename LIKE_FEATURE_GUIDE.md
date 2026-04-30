# Like/Dislike Feature Implementation Guide

## Overview
A complete like/dislike feature has been implemented for blog posts with a clean, modern UI and smooth user interactions.

## Files Modified

### 1. **app/models.py** - Database Models
**Changes:**
- Added `PostLike` model to track user reactions (likes and dislikes)
- Added three helper methods to the `Post` model:
  - `get_like_count()` - Returns the number of likes
  - `get_dislike_count()` - Returns the number of dislikes
  - `get_user_reaction(user_id)` - Returns the current user's reaction ('like', 'dislike', or None)

**New Table Structure:**
```sql
post_like (
  id INTEGER PRIMARY KEY,
  post_id INTEGER (Foreign Key to post),
  user_id INTEGER (Foreign Key to user),
  is_like BOOLEAN (True for like, False for dislike),
  UNIQUE(post_id, user_id) -- One reaction per user per post
)
```

### 2. **app/routes/blog.py** - Backend Routes
**New Routes:**
- `POST /like/<post_id>` - Handle like/dislike actions
  - Accepts JSON: `{"is_like": true/false}`
  - Returns: like count, dislike count, and user's current reaction
  - Toggles reaction off if same reaction is submitted twice
  
- `GET /post/<post_id>/reactions` - Get current reaction counts
  - Returns: like count, dislike count, and user's reaction (if authenticated)

**Features:**
- Prevents duplicate reactions with unique constraint
- Allows users to switch between like and dislike
- Allows users to remove their reaction by clicking the same button twice

### 3. **app/templates/ShowBlog.html** - Frontend Template
**New Elements:**
- Like/Dislike section with thumbs up (👍) and thumbs down (👎) icons
- Real-time counter display for likes and dislikes
- Authentication check:
  - **Authenticated users:** Interactive buttons that toggle reactions
  - **Non-authenticated users:** View counts with a login prompt
- JavaScript functionality for smooth interactions without page reload

**Features:**
- Visual feedback showing user's current reaction
- Real-time count updates via AJAX
- Responsive design for all screen sizes

### 4. **app/static/showblog.css** - Styling
**New CSS Classes:**
- `.reaction-section` - Container for like/dislike section
- `.reaction-container` - Flex container for buttons
- `.reaction-btn` - Base style for like/dislike buttons
- `.reaction-btn.active` - Style for user's current reaction
- `.like-btn.active` - Green highlight for active like
- `.dislike-btn.active` - Red highlight for active dislike
- `.reaction-icon` - Emoji icon styling
- `.reaction-count` - Count display styling
- `.reaction-info` - Non-authenticated user view
- `.login-prompt` - Call-to-action for non-authenticated users

**Design Features:**
- Clean, modern gradient background for reaction section
- Smooth transitions and hover effects
- Icon-based design using emoji (no font icons needed)
- Color-coded active states (green for like, red for dislike)
- Responsive layout that adapts to mobile devices

## Database Migration

**Important:** You need to recreate the database to apply the new schema.

### Steps:
1. Delete the existing database file:
   ```powershell
   Remove-Item instance\blog.db
   ```

2. Restart your Flask application:
   ```powershell
   python run.py
   ```

3. Flask will automatically recreate the database with the new `PostLike` table.

## User Experience

### For Authenticated Users:
1. View a post - see the like/dislike buttons with current counts
2. Click 👍 to like the post
3. Click 👎 to dislike the post
4. Click the same button again to remove your reaction
5. Switch between like and dislike freely
6. All changes happen in real-time without page reload

### For Non-Authenticated Users:
1. View like/dislike counts for each post
2. See a "Login to like or dislike" prompt
3. Click the link to log in and start reacting

## UI/UX Details

### Visual Feedback:
- **Hover State:** Buttons lift up slightly with subtle shadow (translateY effect)
- **Active State:** 
  - Liked post: Green background (#dcfce7) with green border
  - Disliked post: Red background (#fee2e2) with red border
  - Both show colored text matching the action
- **Icon Size:** Appropriately sized at 1.3rem for visibility
- **Spacing:** Well-balanced gaps and padding for clean appearance

### Responsive Design:
- **Desktop:** Side-by-side buttons with plenty of space
- **Tablet:** Buttons adjust to 50% width layout
- **Mobile:** Stacked layout with responsive sizing
- **All sizes:** Touch-friendly button sizes and spacing

## Technical Highlights

### Database Integrity:
- Unique constraint prevents multiple reactions from same user on same post
- Cascading deletes ensure reactions are removed when posts are deleted

### Performance:
- Minimal database queries (2 queries per action)
- AJAX implementation prevents page reloads
- Query optimization with count operations

### Security:
- Login required for interactions (AJAX checks authentication)
- No direct database manipulation from frontend
- Server-side validation of reactions

## Example JSON Response

```json
{
  "success": true,
  "like_count": 25,
  "dislike_count": 3,
  "user_reaction": "like"
}
```

## Future Enhancements (Optional)
- Add comment system for discussions
- Show list of users who liked/disliked
- Add reaction analytics/trends
- Implement real-time updates with WebSockets
- Add emoji reactions beyond like/dislike
- Create reaction notifications
