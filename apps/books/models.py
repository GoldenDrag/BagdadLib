from django.db import models



class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Book(Base):
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True)
    # cover = models.ImageField()
    description = models.TextField()



class Chapter(Base):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    raw_content = models.JSONField("Content of the chapter")

    class Meta:
        unique_together = ('book', 'name',)


class Paragraph(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    content = models.JSONField()


    # BELOW IS FORUM PART OF THE APP
# class Post(Base):
#     paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
#     title = models.CharField(max_length=64)
#     text = models.TextField()
#     image = models.ImageField()
#     rating = models.IntegerField()



# class Comment(Base):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     text = models.TextField()
#     rating = models.IntegerField()