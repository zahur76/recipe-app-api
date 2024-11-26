"""
Serilizers for recipe API
"""

from rest_framework import serializers

from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tags"""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe"""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ("id", "title", "time_minutes", "price", "link", "tags")
        read_only_fields = ["id"]

    def _get_or_create_tags(self, tags, recipe):
        """Handling getting of creaing tags as needed"""

        auth_user = self.context["request"].user
        for tag in tags:

            # will only create a new tag if does not already exist
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,  # same as name=tag["name"]
            )
            # will save all tags to recipe
            recipe.tags.add(tag_obj)
        return recipe

    def create(self, validated_data):
        """create a recipe"""

        tags = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update a recipe"""
        tags = validated_data.pop("tags", None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for Recipe details"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ("description",)
