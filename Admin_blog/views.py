from django.shortcuts import render,redirect
from Blog.models import Blog_Category, Blog_Post
from django.shortcuts import render, redirect, get_object_or_404
 
 

def adminblog(request):
    blogs = Blog_Post.objects.all()
    return render(request, 'Adminpannel/blogadmin/Ad_blog.html', {'blogs': blogs})

 
def add_blog(request):
    categories_queryset = Blog_Category.objects.all() 
    if request.method == 'POST':
        # Extract form data from request.POST
        title = request.POST.get('title')
        content = request.POST.get('content')
        content_1 = request.POST.get('content_1')
        content_2 = request.POST.get('content_2')
        conclusion = request.POST.get('conclusion')
        author = request.POST.get('author')
        author_info = request.POST.get('author_info')
        category_ids = request.POST.getlist('category')  # Note the name attribute should match

        # Handle file uploads separately
        author_image= request.FILES.get('author_image')
        blog_image = request.FILES.get('blog_image')
        blog_image2 = request.FILES.get('blog_image2') if 'blog_image2' in request.FILES else None

        # Create a new Blog_Post object
        blog_post = Blog_Post.objects.create(
            title=title,
            content=content,
            content_1=content_1,
            content_2=content_2,
            conclusion=conclusion,
            author=author,
            author_info=author_info,
            author_image=author_image,
            blog_image=blog_image,
            blog_image2=blog_image2
        )

        # Add categories to the blog post
        for category_id in category_ids:
            category = Blog_Category.objects.get(pk=category_id)
            blog_post.categories.add(category)

        # Redirect to the detail view of the created post
        return redirect('adminblog')  # Adjust the URL name as needed
    else:
        # Render the add blog template with categories_queryset in the context
        return render(request, 'Adminpannel/blogadmin/add_blog.html', {'categories': categories_queryset})


from django.shortcuts import get_object_or_404

def edit_blog(request, id):
    # Retrieve the existing blog post object
    blog_post = get_object_or_404(Blog_Post, id=id)

    categories = Blog_Category.objects.all()  # Fetch all categories

    if request.method == 'POST':
        # Extract form data from request.POST
        blog_post.title = request.POST.get('title')
        blog_post.content = request.POST.get('content')
        blog_post.content_1 = request.POST.get('content_1')
        blog_post.content_2 = request.POST.get('content_2')
        blog_post.conclusion = request.POST.get('conclusion')
        blog_post.author = request.POST.get('author')
        blog_post.author_info = request.POST.get('author_info')

        # Handle category update
        category_id = request.POST.get('category')
        if category_id:
            category = get_object_or_404(Blog_Category, pk=category_id)
            blog_post.categories.set([category])

        if request.FILES.get('author_image'):
            blog_post.author_image = request.FILES['author_image']
        if request.FILES.get('blog_image'):
            blog_post.blog_image = request.FILES['blog_image']
        if request.FILES.get('blog_image2'):
            blog_post.blog_image2 = request.FILES['blog_image2']

        blog_post.save()
        return redirect('adminblog')  # Adjust the URL name as needed
    else:
        return render(request, 'Adminpannel/blogadmin/edit_blog.html', {'blog_post': blog_post, 'categories': categories})

def adblog_details(request):
    return render(request, 'Adminpannel/blogadmin/adblog_details.html')


def delete_blog(request, id):
    blog = Blog_Post.objects.get(id=id)
    blog.delete()
    return redirect('adminblog')