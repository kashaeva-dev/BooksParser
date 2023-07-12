logger_config = {
    'version': 1,
    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{',
            },
        },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'book_parser.log',
            'mode': 'a',
            'formatter': 'std_format',
            'level': 'DEBUG',
            },
        },
    'loggers': {
        'parse_tululu_category_logger': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'parse_tululu_logger': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
    },
}
