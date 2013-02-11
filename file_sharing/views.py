# Create your views here.
import json
import os
import magic

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseBadRequest, Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from file_sharing.models import Folders, File, UserData

MEDIA_ROOT = settings.MEDIA_ROOT

@login_required
def home(request, folder=0):
    if folder==0:
        root_folder = Folders.objects.get(user_id=request.user, level=0)
        folders = Folders.objects.filter(parent=root_folder).all()
        files = File.objects.filter(folder_id=root_folder.id).all()
    else:
        folders = Folders.objects.filter(parent_id=folder).all()
        files = File.objects.filter(folder_id=folder).all()
    
    storage, create = UserData.objects.get_or_create(user=request.user)
    ssize = storage.storage_size
    sused = storage.storage_usage
    storage = (sused*100)/ssize

      
    return render_to_response('file_sharing/index.html',
                              {'folders':folders,
                               'folder':folder,
                               'files': files,
                               'storage': storage,
                              }
                              )

def save_upload( uploaded, filename, raw_data ):
    try:
        from io import FileIO, BufferedWriter
        with BufferedWriter( FileIO( filename, "wb" ) ) as dest:

            if raw_data:
                foo = uploaded.read( 1024 )
                while foo:
                    dest.write( foo )
                    foo = uploaded.read( 1024 ) 
            # if not raw, it was a form upload so read in the normal Django chunks fashion
            else:
                for c in uploaded.chunks( ):
                    dest.write( c )
            return True
    except IOError:
        # could not open the file most likely
        return False

@csrf_exempt
@login_required
def upload(request):
    if request.method == "POST":
        if request.is_ajax( ):
            upload = request
            is_raw = True
            try:
                filename = request.GET[ 'qqfile' ]
            except KeyError: 
                return HttpResponseBadRequest( "AJAX request not valid" )
        else:
            is_raw = False
            if len( request.FILES ) == 1:
                upload = request.FILES.values( )[ 0 ]
            else:
                raise Http404( "Bad Upload" )
            filename = upload.name
        
        original_filename = filename
        #filename = create_filename(filename)
        #filename = "%s/file_sharing/temp/%s" % (MEDIA_ROOT, filename)
        base_dir = "%s/file_sharing" % MEDIA_ROOT
        
        folder_get = int(request.GET['folder'])
        user = request.user.username
        if folder_get != 0:
            folder = Folders.objects.get(id=folder_get)
            folder = str(folder.name).lower()
            target = "%s/%s" % (user, folder)
        else:
            target = "%s" % (user)
        
        full_target = "%s/%s" % (base_dir, target)
        if not os.path.exists(full_target):
            os.makedirs(full_target)
        
        filename = "%s/%s" % (full_target, filename)
        # save the file
        success = save_upload( upload, filename, is_raw )
        if success:
            file = File()
            file.name = original_filename
            file.target = target
            file.user = request.user
            file.size = os.path.getsize(filename)
            file.file_type = magic.from_file(filename, mime=True)
            if folder_get == 0:
                root_folder = Folders.objects.get(user=request.user, level=0)
                file.folder_id = root_folder.id
            else:
                file.folder_id = folder_get
            file.save()
        
        ret_json = {'success':success,'file':original_filename}
        return HttpResponse( json.dumps( ret_json ) )

