from .models import User

def user_profile_image(request):
    # Initialize user variable
    user = None
    
    # Check if user ID is in the session
    if 'id' in request.session:
        try:
            # Fetch the user details from the database using the session 'id'
            user = User.objects.get(id=request.session['id'])
        except User.DoesNotExist:
            pass

    # Return a dictionary containing the user object to be available in templates
    return {'user': user}
