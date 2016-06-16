
from django.conf.urls import url, patterns
from ominicontacto_app import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^ajax/mensaje_recibidos/',
        'ominicontacto_app.views.mensajes_recibidos_view',
        name='ajax_mensaje_recibidos'),
    url(r'^$', 'ominicontacto_app.views.index_view', name='index'),
    url(r'^user/nuevo/$',
        login_required(views.CustomerUserCreateView.as_view()),
        name='user_nuevo',
        ),
    url(r'^user/list/$', login_required(views.UserListView.as_view()),
        name='user_list',
        ),
    url(r'^user/update/(?P<pk>\d+)/$',
        login_required(views.CustomerUserUpdateView.as_view()),
        name='user_update',
        ),
    url(r'^user/agenteprofile/nuevo/(?P<pk_user>\d+)/$',
        login_required(views.AgenteProfileCreateView.as_view()),
        name='agenteprofile_nuevo',
        ),
    url(r'^modulo/nuevo/$',
        login_required(views.ModuloCreateView.as_view()), name='modulo_nuevo',
        ),
    url(r'^modulo/list/$',
        login_required(views.ModuloListView.as_view()), name='modulo_list',
        ),
    url(r'^agente/list/$',
        login_required(views.AgenteListView.as_view()), name='agente_list',
        ),
    url(r'^user/agenteprofile/update/(?P<pk_agenteprofile>\d+)/$',
        login_required(views.AgenteProfileUpdateView.as_view()),
        name='agenteprofile_update',
        ),
    url(r'^grupo/nuevo/$',
        login_required(views.GrupoCreateView.as_view()), name='grupo_nuevo',
        ),
    url(r'^grupo/list/$',
        login_required(views.GrupoListView.as_view()), name='grupo_list',
        ),
)
