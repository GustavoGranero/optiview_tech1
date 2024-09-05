from optview import db

class BaseMixin(object):

    @classmethod
    def add(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()
        return obj
    
    @classmethod
    def get_one(cls, **kw):
        return cls.query.filter_by(**kw).first()
    
    @classmethod
    def get_all(cls, **kw):
        return cls.query.filter_by(**kw).all()
    
    