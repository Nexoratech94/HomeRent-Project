from django.shortcuts import get_object_or_404, render
from Blog.models import Blog_Post, Blog_Category

def blog(request):
    # Retrieve all blog posts
    blog_posts = Blog_Post.objects.all()
    return render(request, 'blog.html', {'blog_posts': blog_posts})

def blog_details(request, blog_id):
    blog_post = Blog_Post.objects.get(id=blog_id)
    # Retrieve all categories
    all_categories = Blog_Category.objects.all()
    return render(request, 'blogdetails.html', locals())





from django.shortcuts import render, redirect
from django.http import Http404
from .models import Comment, Blog_Post

def leave_comment(request, blog_id):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Validate the data
        if name and email and message:
            try:
                # Retrieve the blog post
                blog_post = Blog_Post.objects.get(id=blog_id)
                
                # Create the Comment object and associate it with the blog post
                comment = Comment.objects.create(name=name, email=email, message=message)
                blog_post.comments.add(comment)  # Add the comment to the blog post
                
                # Redirect back to the blog details page with the correct blog_id
                return redirect('blogdetails', blog_id=blog_id)
            except Blog_Post.DoesNotExist:
                raise Http404("Blog post does not exist")
        else:
            raise Http404("All fields are required")
    
    # If the request method is not POST, raise an HTTP 404 error
    raise Http404("Page not found")
