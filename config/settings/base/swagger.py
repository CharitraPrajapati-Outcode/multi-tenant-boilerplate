# drf-yasg Swagger Settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    # 'LOGIN_URL': reverse_lazy('login'),
    # 'LOGOUT_URL': reverse_lazy('logout'),
    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'REFETCH_SCHEMA_ON_LOGOUT': True,
    
    # default api Info if none is otherwise given; should be an import string to an openapi.Info object
    'DEFAULT_INFO': 'my-project.swagger.swagger_info',
    
    # default API url if none is otherwise given
    'DEFAULT_API_URL': 'http://127.0.0.1:8000/',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'in': 'header',
            'name': 'Authorization',
            'type': 'apiKey',
            'description': 'Please pass token as Bearer {{token}}'
        },
        'SchemaName': {
            'type': 'apiKey',
            'name': 'X-Schema-Name',
            'in': 'header',
            'description': 'Pass schema name to use.'
        }
    },
    "DEFAULT_PAGINATOR_INSPECTORS": [
        # 'config.inspectors.UnknownPaginatorInspector',
        'drf_yasg.inspectors.DjangoRestResponsePagination',
        'drf_yasg.inspectors.CoreAPICompatInspector',
    ],
    
    # default inspector classes, see advanced documentation
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
    'DEFAULT_FIELD_INSPECTORS': [
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.InlineSerializerInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
    ]
}