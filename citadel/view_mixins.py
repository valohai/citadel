from django.core.exceptions import ValidationError
from django.http import Http404
from django.views.generic import DetailView


class PKOrSlugDetailView(DetailView):
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        lookup_value = self.kwargs.get(self.pk_url_kwarg) or self.kwargs.get(self.slug_url_kwarg)

        if not lookup_value:
            raise AttributeError(
                f"Generic detail view {self.__class__.__name__} must be "
                f"called with either an object pk or a slug in the URLconf.",
            )

        try:
            return queryset.get(pk=lookup_value)
        except (queryset.model.DoesNotExist, ValidationError, ValueError):
            try:
                return queryset.get(**{self.slug_field: lookup_value})
            except queryset.model.DoesNotExist:
                raise Http404(f"No {queryset.model._meta.verbose_name} found matching the query")
