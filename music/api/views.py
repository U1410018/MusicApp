from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, JsonResponse
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.models import Profile
from charts.models import Chart
from charts.api.serializers import ChartSerializer
from ..models import Playlist, Genre, Music, Album, Performer
from .serializers import PlaylistSerializers, GenreSerializer, MusicSerializer, AlbumSerializer, PerformerSerializer
from authentication.serializers import ProfileSerializer
from django.shortcuts import get_object_or_404


class PlayListCreate(APIView):
    http_method_names = ['post', ]
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
        serializer = PlaylistSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_music(request):
    if request.method == 'GET':
        music_id = request.GET.get('id', None)
        if music_id:
            music = get_object_or_404(Music, pk=music_id)
            music.number_of_views += 1
            music.save()
            return JsonResponse({'title':music.name, 'artist': music.artist.last().name, 'mp3': music.links, 'id': music.pk})
    return JsonResponse({'error': 'wrong parameters are sent'})


class GetUserLikedMusics(APIView):
    http_method_names = ['get', ]

    def get(self, request):
        musics = request.user.musics_liked.all()
        musics_serializers = MusicSerializer(musics, many=True)
        return Response(musics_serializers.data)


class TopPlaylists(APIView):
    http_method_names = ['post', ]

    def post(self, request):
        playlists = sorted(Playlist.objects.all(), key=lambda playlist: playlist.get_net_value, reverse=True)
        serializer = PlaylistSerializers(playlists, many=True)
        return Response(serializer.data)


class TopGenres(APIView):
    http_method_names = ['post', ]

    def post(self, request):
        genres = Genre.objects.all()[:10]
        serializers = GenreSerializer(genres, many=True)
        return Response(serializers.data)


class PlaylistDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise Http404

    def post(self, request):
        pk = request.data.get('pk', None)
        if pk:
            playlist = self.get_object(pk)
            if playlist:
                musics = playlist.musics.all()
                serializer = MusicSerializer(musics, many=True)

                return Response(serializer.data)
            return Response({'error': 'such playlist does not exist!'})
        return Response({'error': 'you should send pk field'})


class AlbumDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

    def post(self, request):
        pk = request.data.get('pk', None)
        if pk:
            album = self.get_object(pk)
            if album:
                musics = album.musics.all()
                serializer = MusicSerializer(musics, many=True)

                return Response(serializer.data)
            return Response({'error': 'such album does not exist!'})
        return Response({'error': 'you should send pk field'})


class GenreDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, genre_name):
        try:
            return Genre.objects.get(genre_name=genre_name)
        except Genre.DoesNotExist:
            raise Http404

    def post(self, request):
        genre_name = request.data.get('genre_name', None)
        if genre_name:
            genre = self.get_object(genre_name)
            if genre:
                musics = genre.all_music_in_genre.all()
                serializer = MusicSerializer(musics, many=True)

                return Response(serializer.data)
            return Response({'error': 'such album does not exist!'})
        return Response({'error': 'you should send pk field'})


class DeletePlaylist(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise Http404

    def post(self, request):
        pk = request.data.get('pk', None)
        if pk:
            playlist = self.get_object(pk)
            if playlist:
                if playlist.creator.username.__eq__(request.user.username):
                    playlist.delete()
                    return Response({'status': 'playlist successfully removed'})
                return Response({'status': 'you can not remove this playlist'})
            return Response({'status': 'such playlist does not exist!'})
        return Response({'status': 'you should send pk field'})


class Search(APIView):
    http_method_names = ['post', ]

    def post(self, request):
        search_query = request.data.get('q', None)
        if len(search_query) >= 2:
            music_results = Music.objects.filter(
                Q(name__icontains=search_query)
            )
            album_results = Album.objects.filter(
                Q(name__icontains=search_query)
            )
            playlist_results = Playlist.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
            user_results = Profile.objects.filter(
                Q(username__icontains=search_query)
            )
            chart_results = Chart.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
            performer_results = Performer.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

            music_serializer = MusicSerializer(music_results, many=True)
            playlist_serializer = PlaylistSerializers(playlist_results, many=True)
            album_serializer = AlbumSerializer(album_results, many=True)
            user_serializer = ProfileSerializer(user_results, many=True)
            chart_serializer = ChartSerializer(chart_results, many=True)
            performer_serializer = PerformerSerializer(performer_results, many=True)

            return Response({'music_results': music_serializer.data, 'album_results': album_serializer.data,
                             'playlist_results': playlist_serializer.data, 'query': search_query,
                             'user_results': user_serializer.data, 'chart_results': chart_serializer.data,
                             'performer_results': performer_serializer.data})
        else:
            return Response({'Minimum length must be 2 characters'})


class TopAlbums(APIView):
    http_method_names = ['get', ]

    def get(self, request):
        albums = sorted(Album.objects.all(), key=lambda album: album.get_net_value, reverse=True)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)


class UserPlaylists(APIView):
    http_method_names = ['get', ]

    def get(self, request):
        playlists = request.user.playlists.all()
        serializer = PlaylistSerializers(playlists, many=True)
        return Response(serializer.data)


class FollowPlaylist(APIView):
    http_method_names = ['post', ]

    def post(self, request):
        playlist_pk = request.data.get('playlist_pk')
        action = request.data.get('action')
        if playlist_pk and action:
            try:
                playlist = Playlist.objects.get(pk=playlist_pk)

                if action == 'follow':
                    playlist.followers.add(request.user)
                else:
                    playlist.followers.remove(request.user)
                return Response({'status': 'ok'})
            except Playlist.DoesNotExist:
                return Response({'status': 'ko'})
        return Response({'status': 'ko'})


class FollowedPlaylists(APIView):
    http_method_names = ['get', ]

    def get(self, request):
        playlists = request.user.followed_playlists.all()
        serializer = PlaylistSerializers(playlists, many=True)
        return Response(serializer.data)


class AddToPlaylist(APIView):
    http_method_names = ['post', ]

    def post(self, request):
        music_id = request.data.get('music_id')
        playlist_id = request.data.get('playlist_id')
        if music_id and playlist_id:
            music = get_object_or_404(Music, pk=music_id)
            playlist = get_object_or_404(Playlist, pk=playlist_id)
            playlist.musics.add(music)
            return Response({'status': 'ok'})
        return Response({'status': 'ko', 'error': 'music id or playlist id is missing'})


class MusicLike(APIView):
    http_method_names = ['post', ]

    def post(self, request):
        music_id = request.data.get('id')
        action = request.data.get('action')
        if music_id and action:
            try:
                music = Music.objects.get(id=music_id)
                if action == 'like':
                    music.users_like.add(request.user)
                else:
                    music.users_like.remove(request.user)
                return Response({'status': 'ok'})
            except:
                pass
        return Response({'status': 'ko'})
