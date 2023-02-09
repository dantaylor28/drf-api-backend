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

### Profiles App

My profiles app stores all data regarding all of the users profile information. Some of the fields present in my model include name, location, bio and an optional profile image. Like on the post model, if you choose not to upload your own image then a default profile image will be set for you. Also present in my Profile model is a create_profile function. What this function does is use django signals to see when a new User instance is created. When this happens, a new profile instance is automatically created as well so it is then associated with that user instance.

Within my serializers.py file, there are several extra Serializer and ReadOnly fields added. Three of these include num_of_posts/followers and following. These fields use the Count method in my views.py to add up the totals which can then be used on the frontend to display statistics to different users. Similar to my post serializer, there is also image validation present here to ensure profile_images meet the required dimensions and file size.

As profiles are created automatically using the create_profile function described above, my ProfileList is just a standard ListAPIView. I have added multiple ways to explore profiles here which include DjangoFilterBackend, searchFilter and orderingFilter. Profiles can be searched based upon usernames, profile names and even location. The filterset fields included here are as shown in the drf_api walkthrough. These were to show profiles that are following a selected user and profiles that are followed by the selected user. Lastly, my ProfileDetail view here is a retrieveUpdateDestroy and as usual the permission class only allows the profile user access to these functionalities.

### Followers App

This app contains all instances of a user that is following or is followed by another user. Fields present in the model include the user who is the follower, the user doing the following and the timestamp of when the follow was received. There are 2 foreign key fields here linking to User, therfore they use the related_name attribute to make sure django can tell them apart. Also in my Follower model is another function, which will raise an integrity error if a user attempts to follow his/her own profile.

My serializers.py contains a couple of extra readOnly fields just specifying the owner and the user who received the follow. The create function is present so users can succesfully create a follow and details of the Integrity error raised from self following is also present here. My views are very simple and contain minimal information also. The list view allows users to list and create followers and if you are the owner of a follow this can then be deleted in the FollowerDetail view.

### Pins App

Pin is the first of my own custom models, and it holds all data of when a user pins a post. M Pin model has two foreign keys, one to User and the other to Post. These are necessary to ensure the model can determine the user that is performing the pin and the post that they are perfoming it to. I have let users have the ability to pin their own posts as well as others. This is because pinned posts will be added to the current users board, and therefore users may wish to have their own posts displaying there too. I have included a unique together field which contains owner and post on my model also. This is present to stop users from pinning a post more than once, and an error will be raised if they attempt to do so.

My serializers file simply contains the fields from my models and the extra readOnly field, post_title. This just gets the title of the pinned post, to provide extra information to the user. The create function is here again, and raises a validation error with an appropriate error message if an attempt is made to pin a post more than once.

My PinListView is a ListCreateAPIView so it displays a form on the page to pin a post as long as you are logged in and authenticated. The pins can be filtered through by post title or the owner of the pins using DjangoFilterBackend. In my detail view, it is a retrieveDestroyAPIView as pins cannot be edited. If you are the owner of the pin, you can use the delete button on this page to remove them from the database.

### Comments App

The comments app stores all data relating to any comments left on a post. It stores data on the post, user, timestamp and the text commented. My model has two foreign key fields, one to User and one to Post. 

In my CommentSerializer, I have added some extra fields to give users more detail on the comment and user who left it. I have imported and used naturaltime to display the timestamps more appropriately for a comment for example, 1 day, 4 hrs ago. Num_of_comment_likes is another field that I have included here. This relates to my comment_likes app which is used for liking different user comments. This field will use the Count method on my views.py to display how many likes a specific comment has. A second commentDetailSerializer class has also been implemented here. It adds the post_id via a readOnly field and it is used in my CommentDetailView. The reason for this is that it will auto-fill the post of the comment a user is trying to edit. This will save the user time trying to find the post relating to the comment and therfore provides a better user experience overall. This piece of code is accredited to the drf_api walkthrough project.

In my views.py file, the list view is a ListCreateAPIView as normal and includes the annotate method which is used to calculate the num_of_comment_likes and display the results to the user. Comments can be filtered by owner and post, while ordering fields are also available to display comments in the order of creation via their timestamp. The detail view is a retrieveUpdateDestroy view and the only difference here is that the serializer class is set to CommentDetailSerializer as opposed to CommentSerializer so the post is auto-selected.

### Comment_likes App

This model stores all the data on comment likes. Similar to alot of my other models, it has two foreign key fields. One being User and the other Comment in this instance. There is a unique_together field between owner and comment, which is present to ensure a comment can only be liked by a specific user one time. 

The only extra field present in my serializer is comment_text which as the name suggests, shows the actual comment to the user. Also present in my serializer is the create function. As usual, it has a try/exceot block which attempts to create the like. If the user has already liked the comment then a validation error is raised along with an error message explaining the problem.

On my views.py file, my commentLikeListView is a listCreateAPIView. If signed in and authenticated, you can use the form at the bottom of the page to select a comment from the dropown list and press confirm to like it. I have used DjangFilterBackend which lets users filter the comment likes by a certain comment. Lastly, the detail view retrieves a specified like and if you are the owner of it, then it can be deleted from this page.

### Categories App

The Category model stores the names of a category that can be assigned to a post on the creation of it. Within the Post model, there is a category field present which is a foreignKey value linking to this model. The idea of this, is that the user will have access to a dropdown list of categories on the form in the frot-end that they can choose from and assign their post to. As well as assigning a category when creating a post, users can assign or change them when editing one of their posts also. 

In my CategorySerializer, the fields present in my model are listed here as well as one extra which adds up all the posts assigned to a specific category. In my views.py file here, I have assigned both the listView and the detailView the permission class of IsAdminOrReadOnly. This is because I want only an admin to have the ability to create new categories or delete exisiting ones. Search and ordering have been included here so users searching for a single category can be found or categories can be ordered based on their timestamp of creation.

### Admin Panel

One of the first steps taken in this project was to create my superuser and ensure that functionality was running as expected. Throughout the development process, I registered all of my apps in admin.py to ensure I can access these features there and test the functionality from the admin panel if necessary. This also made testing easier once I had deployed the application as it is difficult to test from the api deployed site unless its done through the admin panel.
Full CRUD functionality works as expected and any registered administrators can monitor all goings on from here.

The login for the superuser account is as follows - 

***Username - admin***\
***Password - esporta1993***

## Future Feature To Implement

- I would like to include a new app for comment_replies. I feel this would work well alongside the comment_likes that I have already included in this project.

- Signing in with social media is a feature I planned to include in the planning stages of this project. Unfortunately, I did not have the time to implement this before my submission date.

## Languages/Libraries Used

Below is a list of the requirements that were included to make this project

- Django
- Django Rest Framework
- Cloudinary
- Pillow
- Django allauth 
- Django filters
- Psycopg2 database
- SimpleJWT

The primary language used in the production of this api was Django and the django-rest-framework. Pillow is a library that is a required depenedency you have to install when using an imageField on any of your models. I used Cloudinary for my default image storage. This is because Django uses an ephemeral file system, so Cloudinary was a  great choice to prevent my image files being deleted after a certain amount of time has passed. Django filters was a library used to add the functionality to filter the data in my views.py files. It makes it extremly easy to add this functionality and improves the user experience considerably. To add token refreshing to my project, I used simpleJWT as shown in the drf_api walkthrough.