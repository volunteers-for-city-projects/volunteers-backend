from rest_framework import generics, viewsets

from content.models import News, PlatformAbout, Valuation, Feedback

from .serializers import (FeedbackSerializer,
                          NewsSerializer,
                          PreviewNewsSerializer,
                          PlatformAboutSerializer)


class PlatformAboutView(generics.RetrieveAPIView):
    serializer_class = PlatformAboutSerializer

    def get_object(self):
        platform_about = PlatformAbout.objects.latest('id')
        valuations = Valuation.objects.all()[:4]
        return {
            'about_us': platform_about.about_us,
            'platform_email': platform_about.platform_email,
            'valuations': valuations
        }


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PreviewNewsSerializer
        return NewsSerializer


class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
