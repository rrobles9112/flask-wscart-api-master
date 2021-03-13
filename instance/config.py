import os



class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('FLASK_SECRET')
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@localhost:3306/%s' % (os.getenv('MYSQL_USER'),
                                                                   os.getenv('MYSQL_PASSWORD'),
                                                                   os.getenv('MYSQL_DATABASE_NAME'))
    """
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@localhost:3306/WSCartAPI' % (os.getenv('MYSQL_USER'),
    #                                                                       os.getenv('MYSQL_PASSWORD'))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    print(SQLALCHEMY_DATABASE_URI)


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing."""
    basedir = os.path.abspath(os.path.dirname(__file__))
    TESTING = True
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@localhost:3306/test_WSCartAPI' % (os.getenv('MYSQL_USER'),
                                                                          os.getenv('MYSQL_PASSWORD'))
                                                                          """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False



app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
