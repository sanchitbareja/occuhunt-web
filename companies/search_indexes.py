import datetime
from haystack import indexes
from companies.models import Company


class CompanyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    website = indexes.CharField(model_attr='website', null=True)
    organization_type = indexes.CharField(model_attr='organization_type', null=True)
    company_description = indexes.CharField(model_attr='company_description', null=True)
    competitors = indexes.CharField(model_attr='competitors', null=True)
    location = indexes.CharField(model_attr='location', null=True)

    def get_model(self):
        return Company

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()