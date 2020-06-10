from django import forms

from catalog.models import Product, ProductAttribute, PredefineAttributeValue


class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length=128, min_length=2, strip=True, widget=forms.TextInput(
        attrs={'class ': ''}))
    description = forms.CharField(
        strip=True, widget=forms.Textarea(attrs={'class ': ''}))
    stock_quantity = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': ''}))
    price = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': ''}))

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'stock_quantity',
            'price',
        ]


class ProductDetailsForm(forms.ModelForm):
    name = forms.CharField(max_length=128, min_length=2, strip=True, widget=forms.TextInput(
        attrs={'class ': ''}))
    description = forms.CharField(
        strip=True, widget=forms.Textarea(attrs={'class ': ''}))
    published = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': ''}))
    mark_as_new = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': ''}))
    not_returnable = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': ''}))
    show_on_homepage = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': ''}))
    featured = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': ''}))
    allow_reviews = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': ''}))
    vendor_comments = forms.CharField(
        strip=True, widget=forms.Textarea(attrs={'class ': ''}))

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'published',
            'mark_as_new',
            'not_returnable',
            'show_on_homepage',
            'featured',
            'allow_reviews',
            'vendor_comments'
        ]


class ProductStockForm(forms.ModelForm):
    stock_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={'class': ''}))
    sold = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={'class': ''}))

    class Meta:
        model = Product
        fields = [
            'stock_quantity',
            'sold',
        ]


class PriceForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': ''}))
    sales_rate = forms.FloatField(min_value=0.0, widget=forms.NumberInput(
        attrs={'class': '', 'step': "0.01"}))
    on_sale = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': ''}))
    is_free = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': ''}))
    call_for_price = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': ''}))

    class Meta:
        model = Product
        fields = [
            'price',
            'sales_rate',
            'on_sale',
            'call_for_price',
        ]


class DimensionForm(forms.ModelForm):
    weight = forms.DecimalField(max_digits=4, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': ''}))
    length = forms.DecimalField(max_digits=4, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': ''}))
    width = forms.DecimalField(max_digits=4, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': ''}))
    height = forms.DecimalField(max_digits=4, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': ''}))

    class Meta:
        model = Product
        fields = [
            'weight',
            'length',
            'width',
            'height',
        ]


class ProductAttributeForm(forms.ModelForm):

    attributes = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=PredefineAttributeValue.objects.all().order_by("attribute")
    )

    class Meta:
        model = Product
        fields = [
            'attributes',
        ]
