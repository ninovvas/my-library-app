from rest_framework.serializers import ModelSerializer

from MyLibrary.main.models import Book, Publisher, Author


#########
# Book
#########

class BookListSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('title','isbn10','isbn13', 'language', 'page_count', 'start_read_date',
                  'end_read_date', 'end_read_date', 'read', 'user_comment', 'description', 'image', 'authors',  'publisher' )


class BookFullSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'isbn10', 'isbn13', 'language', 'page_count', 'start_read_date',
                  'end_read_date', 'end_read_date', 'read', 'user_comment', 'description', 'image', 'authors',
                  'publisher')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

############
# Publisher
############

class PublisherListSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id','publisher_name', 'address', 'email', 'city', 'state_province', 'country', 'website', 'icon')


class PublisherFullSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('publisher_name', 'address', 'email', 'city', 'state_province', 'country', 'website', 'icon')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

###########
# Author
###########


class AuthorListSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('id','name', 'picture', 'email',)


class AuthorFullSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'picture', 'email',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)