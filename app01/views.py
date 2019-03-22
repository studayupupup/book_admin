from django.shortcuts import render, redirect, HttpResponse
from app01 import models


# Create your views here.

def publisher_list(request):
    ret = models.Publisher.objects.all().order_by("id")  # order_by 排序
    return render(request, "../static/../templates/publisher_list.html", {"publisher_list": ret})


def add_publisher(request):
    if request.method == "POST":
        publisher_name = request.POST.get("publisher")
        models.Publisher.objects.create(name=publisher_name)
        return redirect("/publisher_list")
    return render(request, '../static/../templates/add_publisher.html')


def del_publisher(request):
    publisher_id = request.GET.get("id", None)
    if publisher_id:
        publisher_object = models.Publisher.objects.get(id=publisher_id)
        publisher_object.delete()
        return redirect("/publisher_list")
    else:
        return HttpResponse("要删除的数据不存在")


def edit_publisher(request):
    if request.method == "GET":
        publisher_id = request.GET.get("id")
        publisher_obj = models.Publisher.objects.get(id=publisher_id)
        return render(request, "../static/../templates/edit_publisher.html", {"publisher": publisher_obj})
    elif request.method == "POST":
        new_name = request.POST.get("publisher_name")
        id = request.POST.get("publisher_id")
        publisher_obj = models.Publisher.objects.get(id=id)
        publisher_obj.name = new_name
        publisher_obj.save()
        return redirect("/publisher_list")


def book_list(request):
    # 从后台对象
    all_book = models.Book.objects.all()
    # 渲染进前台页面
    return render(request, "book_list.html", {"all_book": all_book})


def add_book(request):
    if request.method == "POST":
        book_name = request.POST.get("book_name")
        publisher_id = request.POST.get("publisher_name")
        models.Book.objects.create(title=book_name, publisher_id_id=publisher_id)
        return redirect("/book_list")
    publisher_list = models.Publisher.objects.all()
    return render(request, "add_book.html", {"publisher_list": publisher_list})


def del_book(request):
    book_id = request.GET.get("id")
    if book_id:
        book_object = models.Book.objects.get(id=book_id)
        book_object.delete()
        return redirect("/book_list/")
    else:
        return HttpResponse("要删除的数据不存在")


def edit_book(request):
    if request.method == 'GET':
        # 拿到要编辑的书的ID值,找到书籍对象，一会把书籍名字和ID返回给前端
        edit_id = request.GET.get("id")
        edit_book_obj = models.Book.objects.get(id=edit_id)
        # 接收到要编辑的书籍的id 找到要编辑的对象
        publisher_list = models.Publisher.objects.all()
        return render(request, "edit_book.html", {"publisher_list": publisher_list, "edit_book_obj": edit_book_obj})
    else:
        # 从提交的数据里边取出要修改的书籍的id 书名 出版社
        book_id = request.POST.get("book_id")
        book_name = request.POST.get("book_name")
        publisher_id = request.POST.get("publisher_id")
        # 对书籍更新
        book_obj = models.Book.objects.get(id=book_id)
        book_obj.title = book_name  # 更新书名
        book_obj.publisher_id_id = publisher_id  # 更新书名关联的出版社
        book_obj.save()
        return redirect("/book_list/")


def author_list(request):
    author_list = models.Author.objects.all()
    # author_obj = models.Author.objects.get(id = 1) 找到作者表中ID为1的一条记录
    # print(author_obj.book)  作者表中 书跟书籍 是多对多的关系，所以author_obj.book表示的是多个书籍对象的列表
    # print(author_obj.book.all()) <QuerySet [<Book: Book object (22)>, <Book: Book object (23)>, <Book: Book object (24)>]>
    return render(request, "author_list.html", {"all_author": author_list})


def add_author(request):
    if request.method == "POST":
        author_name = request.POST.get("author_name")
        books = request.POST.getlist("book_id")  # getlist 获取列表,如多选的checkbox和多选的select
        new_author = models.Author.objects.create(name=author_name)
        new_author.book.set(books)
        return redirect("/author_list/")
    # 找到所有书籍 返回给前台页面，作者后边要有书籍
    all_book = models.Book.objects.all()
    return render(request, "add_author.html", {"all_book": all_book})


def del_author(request):
    author_id = request.GET.get("id", None)
    models.Author.objects.get(id=author_id).delete()
    return redirect("/author_list/")


def edit_author(request):
    if request.method == "POST":
        id = request.POST.get("author_id")
        name = request.POST.get("author_name")
        book = request.POST.getlist("book_id_list")
        print(id)
        print(book)
        print(name)
        edit_obj = models.Author.objects.get(id=id)
        edit_obj.name = name
        edit_obj.book.set(book)
        edit_obj.save()
        return redirect("/author_list/")
    # 从url取到要修改的作者的ID
    edit_author_id = request.GET.get("id")
    # 找到要编辑的作者的对象
    edit_author = models.Author.objects.get(id=edit_author_id)
    book_list = models.Book.objects.all() # 找到所有图书 传给模板
    return render(request, "edit_author.html", {"edit_author": edit_author, "book_list": book_list})
