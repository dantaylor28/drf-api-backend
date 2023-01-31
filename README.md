# Social Media Backend API

In this API, my goal was to implement the functionality to handle all the necessary data needed to create a fully functional social media platform. I loosely based this project on the popular picture sharing website Pinterest. The API has full CRUD(create,read,update and delete) functionality which lets registered users upload their own posts with the optional ability to include a title, caption and category. You can edit or delete posts as long as you are the owner of them which is ensured with the addition of authorisation in this project. In addition, signed in users can pin posts they would like to add to their boards, while also having the ability to comment on posts and liking others users comments.

Users can follow other profiles and you have the ability to customise your own by changing your profile picture, your location and adding a bio. When creating posts, you can optionally assign it to a category. If you do so, I plan to implement the functionality of searching for a specific category and having all posts associated with it displaying on the front end. Categories can also be added to posts later in time since that field is present and can be updated when editing a post.

## API Features

### drf_api app

The drf_api is my initial project app that contains the settings.py, my main urls.py and my permsissions.py files. To allow my api to use Cloudinary for its image file storage, the settings.py file contains all the relevant code to acheive this. Also in my settings.py is all code relating to the implementation of jwt refresh tokens, corsheaders and the list of all of my installed apps. The code to achieve most of this functionality was taken from the drf_api walkthrough project.

In my views.py file, there is a custom logout view that I have included to address a known logout error with dj-rest-auth that prevents users from logging out correctly. This code was also taken from the drf_api walkthrough as it was a suggestion to fix this error.

### Permissions 

My project requires different levels of permissions depending on what it is that the user is trying to accomplish. In my permissions.py file, I have defined two custom permissions and there is a default rest framework permission declared in my settings.py file. The default project wide permission I am using is IsAuthenticatedOrReadOnly. This allows anybody to read all parts of my api but you have to be an authenticated user to have the ability to create, update or delete any data.

My first custom permission is IsOwnerOrReadOnly. I have applied this to my DetailViews only. The permission checks the current user against the owner of the data trying to be accessed, and only lets you make changes to that data if you are the owner of it. This will prevent users editing or deleting other users posts/profiles and more.

The second custom permission I have created is IsAdminOrReadOnly. This permission has been used primarily to handle the creation and deletion of categories. I only want an admin user to have the ability to create categories as having that universally available will quickly result in an overabundance of them. As well as creating them, only an admin user can edit or delete them. Every user will be able to retrieve the list view of categories but the form to create new ones and the button to delete them will not be present unless the signed in user is an admin.

### Posts App

This app contains my post model and all of the associated files to ensure that the api has full CRUD functionality. My model contains all of the expected fields that are present on a modern day social media platform. Users can upload an image along with the post title, a caption and also assign the post into a category if they wish.

In the serializers.py file, there are a number of extra serializer method and read only fields that I have added. These include the is_owner and pinned_id fields along with the num_of_pins and num_of_comments fields. The num_of fields have been added from the views.py which used django Count to work out how many pins and comments each post has and then assined the num_of fields an integer value. Also present in my serializers file is a validation method, validate_post_image. This method ensures any images posted by users meets certain criteria. The method checks that the height and width does not exceed 4096px and that the overall file size is not bigger than 2mb. If any images do not meet this, then a validation error is raised and an appropriate error message is shown to the user without crashing the api. The validation is important for numerous reasons. Firstly, it makes image processing easier for the server to handle while also keeping network latency down and it also ensures that images will display properly on different screen sizes.

Like all of my views in this project, there are 2 that users can access. The first is a ListCreateApiView which displays all posts in this instance and and the second one being a RetrieveUpdateDestroyApiView where the user can request a specific one by adding a post's primary key to the end of the url. If you are authenticated, a form will appear at the bottom of the list view, letting users create a post. On the detail view, the post retrieved along with the post details will appear on a form at the bottom of the page also along with a delete button, but only if you are the owner of the post. On the queryset field is where I have used Count to tally up the total number of pins and comments which are added on the serializers file. I have used django-filters on the PostListView to allow users the ability to filter posts by owner, category, posts from users the selected user is following and posts that the selected user has pinned. You can also order posts according to the number of pins or the number of comments that they have as well as searching for a specific post using either the title or a username as search fields. The only permissions class i'v had to specify here is the IsOwnerOrReadOnly permission on the PostDetailView as the list view automatically uses IsAuthenticatedOrReadOnly as declared in the settings.py file. As outined above, this just ensures only the owner of a post can edit or delete it.

